'use this class to generate new txts'
import pdb
import numpy as np
import time
from scipy.special import softmax

class text_generator(object):
	def __init__(self, encoder_model, decoder_model, BATCH_SIZE, PREDICT_LEN, preparer):
		self.encoder_model = encoder_model
		self.decoder_model = decoder_model
		self.BATCH_SIZE = BATCH_SIZE
		self.PREDICT_LEN = PREDICT_LEN
		self.preparer = preparer
		'will only consider the messages that has more log prob than -2.0'
		self.prob_thres = -2.0
		self.generate_message_number = 20

	def predict_interface(self, seed):
		start_time = time.time()
		self.predict(seed)
		self.generate_text()
		print("---generation process cost %s seconds ---" % (time.time() - start_time))

	def predict(self, seed):
		'given the input seed, process it'
		seed = np.repeat(np.expand_dims(seed, 0), self.BATCH_SIZE, axis=0)
		# Encode the input as state vectors.
		state_and_output = self.encoder_model.predict(seed)
		states_value = state_and_output[:4]
		encoder_output = state_and_output[-1]
		# Solve decoder things
		self.predictions = [np.array([[7010]] * self.BATCH_SIZE, dtype=np.int32)]
		self.predictions_prob = []
		for i in range(self.PREDICT_LEN):
			last_word = self.predictions[-1]
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
		prob_part = softmax([float(x) for x in res[:, 0]])
		danmaku_list = res[:, 1]
		fin_res = np.random.choice(danmaku_list, self.generate_message_number, p=prob_part)
		for generated in fin_res:
			print(generated)
			# print("with prob: {}, generated: {}".format(this_batch_prob, generated))
