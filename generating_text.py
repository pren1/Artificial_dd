'use this class to generate new txts'
import pdb
import numpy as np
import time
from scipy.special import softmax
from heapq import nlargest
import tensorflow as tf
import os
import _thread
import pexpect
import sched, time

class text_generator(object):
	def __init__(self, encoder_model, decoder_model, BATCH_SIZE, PREDICT_LEN, preparer):
		self.encoder_model = encoder_model
		self.decoder_model = decoder_model
		self.BATCH_SIZE = BATCH_SIZE
		self.PREDICT_LEN = PREDICT_LEN
		self.preparer = preparer
		'will only consider the messages that has more log prob than -2.0'
		self.prob_thres = -2.5
		self.generate_message_number = 40
		self.push_service = pexpect.spawn('node ./bilibili-live-danmaku-api/stdio.js')

	def predict_interface(self, seed, graph, sess):
		self.start_time = time.time()
		self.predict(seed, graph, sess)
		# self.predict_beam_search(seed, graph, sess)
		generated = self.generate_text()
		print("---generation process cost %s seconds ---" % (time.time() - self.start_time))
		return generated

	def predict_beam_search(self, seed, graph, sess, top_k=5, temperature=1.0):

		# self.encoder_model.reset_states()
		# self.decoder_model.reset_states()
		seed = np.repeat(np.expand_dims(seed, 0), self.BATCH_SIZE, axis=0)
		with graph.as_default():
			with sess.as_default():
				state_and_output = self.encoder_model.predict(seed)
		states_value = state_and_output[:4]
		encoder_output = state_and_output[-1]
		self.predictions = [np.array([[7010]] * self.BATCH_SIZE, dtype=np.int32)]
		self.predictions_prob = []
		'If the stop batch value is True, skip that part'
		self.stop_batch_list = [False] * self.BATCH_SIZE
		for i in range(self.PREDICT_LEN):
			'First, run the prediction on all the batches'
			last_word = self.predictions[-1]
			with graph.as_default():
				with sess.as_default():
					next_probits, h, c, h1, c1 = self.decoder_model.predict([last_word] + states_value + [encoder_output])
			# print("---generation process cost %s seconds ---" % (time.time() - self.start_time))
			'(500, 7011)'
			next_probits = next_probits[:, 0, :]
			'For each batch...'
			current_whole_batch_prediction = []
			current_whole_batch_prob = []
			for batch_index in range(len(next_probits)):
				if self.stop_batch_list[batch_index] == True:
					'Simply stop calculating the useless probability'
					last_token = 7010
				else:
					if top_k == 1:
						last_token = next_probits[batch_index].argmax(axis=-1)
					else:
						'j is the index of each word'
						probs = [(prob, j) for j, prob in enumerate(next_probits[batch_index])]
						probs = nlargest(top_k, probs)
						indices, probs = list(map(lambda x: x[1], probs)), list(map(lambda x: x[0], probs))
						'apply softmax here...'
						# probs = np.array(probs) / temperature
						# probs = probs - np.max(probs)
						# probs = np.exp(probs)
						# probs = probs / np.sum(probs)
						probs = softmax(probs)
						last_token = np.random.choice(indices, p=probs)
					if last_token in [0, 7010]:
						self.stop_batch_list[batch_index] = True
				current_whole_batch_prediction.append(last_token)
				current_whole_batch_prob.append(next_probits[batch_index][last_token])
			self.predictions.append(np.asarray(current_whole_batch_prediction))
			self.predictions_prob.append(np.asarray(current_whole_batch_prob))
			states_value = [h, c, h1, c1]  #######NOTICE THE ADDITIONAL HIDDEN STATES

	def predict(self, seed, graph, sess):
		'given the input seed, process it'
		seed = np.repeat(np.expand_dims(seed, 0), self.BATCH_SIZE, axis=0)
		# Encode the input as state vectors.
		with graph.as_default():
			with sess.as_default():
				state_and_output = self.encoder_model.predict(seed)
		states_value = state_and_output[:4]
		encoder_output = state_and_output[-1]
		# Solve decoder things
		self.predictions = [np.array([[7010]] * self.BATCH_SIZE, dtype=np.int32)]
		self.predictions_prob = []
		for i in range(self.PREDICT_LEN):
			last_word = self.predictions[-1]
			with graph.as_default():
				with sess.as_default():
					next_probits, h, c, h1, c1 = self.decoder_model.predict([last_word] + states_value + [encoder_output])
			next_probits = next_probits[:, 0, :]
			# sample from our output distribution
			next_idx = [
				np.random.choice(len(self.preparer.characters), p=next_probits[i])
				for i in range(self.BATCH_SIZE)
			]
			'build the prob case'
			prob = []
			for batch_id in range(self.BATCH_SIZE):
				prob.append(next_probits[batch_id][next_idx[batch_id]])
			self.predictions_prob.append(np.asarray(prob))
			self.predictions.append(np.asarray(next_idx, dtype=np.int32))
			# Update states
			states_value = [h, c, h1, c1]  #######NOTICE THE ADDITIONAL HIDDEN STATES

	def generate_text(self):
		generated_whole_list = []
		for i in range(self.BATCH_SIZE):
			# print('PREDICTION %d\n\n' % i)
			p = [self.predictions[j][i] for j in range(self.PREDICT_LEN)]
			p_prob = [self.predictions_prob[j][i] for j in range(self.PREDICT_LEN)]
			current_list = []
			'one sentence for one batch'
			this_batch_prob = 0.
			for index in range(len(p)):
				'just get the character generated'
				val = p[index]
				cur_prob = np.log(p_prob[index])
				if index == 0:
					val = val[0]
				current_char = self.preparer.n_to_char[val]
				current_list.append(current_char)
				this_batch_prob += cur_prob
				if current_char == '\n':
					break
			'we also wanna the average prob here'
			this_batch_prob /= len(current_list)
			current_list.remove('eos')
			if len(current_list) > 0 and this_batch_prob > self.prob_thres:
				generated = ''.join(current_list)  # Convert back to text
				generated_whole_list.append([this_batch_prob, generated])
		res = sorted(generated_whole_list, key=lambda tup: tup[0], reverse=True)
		res = np.asarray(res)
		# pdb.set_trace()
		prob_part = softmax([float(x) for x in res[:, 0]])
		danmaku_list = res[:, 1]
		fin_res = np.random.choice(danmaku_list, self.generate_message_number, p=prob_part)
		fin_res = self.danmaku_filter(fin_res)
		time_range = list(range(len(fin_res)))
		# s = sched.scheduler(time.time, time.sleep)
		# for (time_stamp, single_meg) in zip(time_range, fin_res):
		# 	print(f"time_stamp: {time_stamp}, meg: {single_meg}")
		# 	s.enter(float(time_stamp), 1, self.print_target_message, (single_meg,))
		for generated in fin_res:
			print(f"Generated message: {generated}")
			# self.print_target_message(generated)
			# _thread.start_new_thread(self.print_target_message, (generated,))
			# print("with prob: {}, generated: {}".format(this_batch_prob, generated))
		return fin_res

	def danmaku_filter(self, fin_res):
		new_res = []
		for single in fin_res:
			if self.not_removed(single):
				new_res.append(single)
		return new_res

	def not_removed(self, single):
		char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
		             'u', 'v', 'w', 'x', 'y', 'z']
		number_list = ['1', '4', '5', '6', '7', '9']
		use_this_one = False
		single = single.lower()
		for character in single:
			if (character not in char_list) and (character not in number_list):
				use_this_one = True
		if single in ['kksk', 'awsl', 'rua']:
			use_this_one = True
		return use_this_one

	def print_target_message(self, meg):
		# self.push_service.sendline(f'e5217f3b%2C1571553645%2Cfecaa191 b367826c1b0c5a56b1448e5f3e99c83e 711307 {meg}')
		random_int = np.random.randint(3, size=1)
		if random_int == 0:
			_thread.start_new_thread(os.system, (f"node ./bilibili-live-danmaku-api/stdio.js e5217f3b%2C1571553645%2Cfecaa191 b367826c1b0c5a56b1448e5f3e99c83e 711307 {meg}",))
			# os.system(f"node ./bilibili-live-danmaku-api/stdio.js e5217f3b%2C1571553645%2Cfecaa191 b367826c1b0c5a56b1448e5f3e99c83e 711307 {meg}")
		elif random_int == 1:
			_thread.start_new_thread(os.system, (f"node ./bilibili-live-danmaku-api/stdio.js 4a97f2ef%2C1571683732%2C8d5a1791 4bde0a8146c3be858c827350f05dbe37 711307 {meg}",))
			# os.system(f"node ./bilibili-live-danmaku-api/stdio.js 4a97f2ef%2C1571683732%2C8d5a1791 4bde0a8146c3be858c827350f05dbe37 711307 {meg}")
		elif random_int == 2:
			_thread.start_new_thread(os.system, (
			f"node ./bilibili-live-danmaku-api/stdio.js fec803e5%2C1571684349%2C00527891 1b32662e3c6eba51fd90b8d281ffd06a 711307 {meg}",))
		# elif random_int == 3:
		# 	_thread.start_new_thread(os.system, (
		# 	f"node ./bilibili-live-danmaku-api/stdio.js 4a97f2ef%2C1571683732%2C8d5a1791 4bde0a8146c3be858c827350f05dbe37 711307 {meg}",))
