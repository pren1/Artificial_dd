# -*- coding: utf-8 -*-
"""“Predict Danmaku with Cloud TPUs and Keras”

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TSXNQ3IXjvLE2daqFVmdZvHDYn7Xzgkd

##### Copyright 2018 The TensorFlow Hub Authors.
"""
## Predict vtuber danmaku with Cloud TPUs and Keras
#### Modified from "Predict Shakespeare with Cloud TPUs and Keras"
'Author github ID: pren1, coco401, simon3000, Afanyiyu'
from process_prepare import process_prepare
from model_builder import model_structure_loader
from generating_text import text_generator
from input_data import input_data
import pdb
import _thread
import tensorflow as tf
from multiprocessing.pool import ThreadPool
import json
import copy
import threading
from flask import Flask
from flask import jsonify
from flask import request
from flask import copy_current_request_context

class model_process(object):
	def __init__(self, BATCH_SIZE):
		'load in model at this part'
		'the character should occur this much time if they wanna to be taken into account'
		self.context_vector_length = 100
		self.BATCH_SIZE = BATCH_SIZE
		self.PREDICT_LEN = 15
		self.model_folder = 'tmp'
		# Multi-thread version
		self.data_list = []
		self.totalAdded = 0
		self.lock = threading.Lock()

		# To limit the new thread running, run 1 at a time
		self.new_thread_lock = threading.Lock()
		self.run_a_new_thread = True

		self.pool = ThreadPool(processes=1)

	def prepare_for_generator(self):
		'prepare for the whole process'
		self.preparer = process_prepare(target_path_folder='content')
		'Save custom dict to txt file: custom_dict.txt'
		self.preparer.create_custom_dict()
		'Work around for keras model multi-threading'
		self.sess = tf.Session()
		self.graph = tf.get_default_graph()
		with self.graph.as_default():
			with self.sess.as_default():
				model_builder = model_structure_loader(characters=self.preparer.characters,
				                                       embedding_matrix=self.preparer.embedding_matrix,
				                                       context_vector_length=self.context_vector_length)
				_, encoder_model, _ = model_builder.lstm_model(seq_len=1, batch_size=self.BATCH_SIZE, stateful=True)
				encoder_model.load_weights('./{}/encoder.h5'.format(self.model_folder))
				decoder_model = model_builder.get_stand_alone_decoder(seq_len=1, batch_size=self.BATCH_SIZE, stateful=True)
				decoder_model.load_weights('./{}/decoder.h5'.format(self.model_folder))
		# self.graph = tf.get_default_graph()
		tf.keras.backend.set_session(self.sess)

		self.generator = text_generator(encoder_model, decoder_model, self.BATCH_SIZE, self.PREDICT_LEN, self.preparer)

	def feed_in_data(self, data_seq, room_id_label):
		'read in the data'
		assert len(data_seq) > 0, "Empty data, something wrong here~"
		print(f">> {data_seq}")
		# Save the obtained_input at this list
		obtained_input = sum(copy.deepcopy(self.data_list), [])
		if len(obtained_input) >= self.context_vector_length:
			'Print input data'
			# print("read in data:")
			# for data in self.data_list:
			# 	print(f">>{data}")
			'Run prediction automatically'
			# obtained_input = sum(self.data_list, [])
			assert len(obtained_input) >= self.context_vector_length, "Logic error"
			threading.Thread(target=self.DeleteDataList).start()
			print(f"create a new thread to generate text, has obtained {len(obtained_input)} inputs")
			if True:
				# self.new_thread_lock.acquire()
				'We do not allow anyone run a new thread at here'
				self.run_a_new_thread = False
				async_result = self.pool.apply_async(self.generator.predict_interface, (self.preparer.transform(obtained_input[-100:]), room_id_label, self.graph, self.sess))
				return_val = async_result.get()
				self.run_a_new_thread = True
				# self.new_thread_lock.release()
				return return_val
			else:
				return []
		'Cut the string and add tokens'
		data_seq = self.preparer.cut_target_seq(data_seq)
		# self.data_list.append(data_seq)
		threading.Thread(target=self.AddToDataList, args=(data_seq,)).start()
		return []

	def AddToDataList(self, meg):
		self.lock.acquire()
		self.data_list.append(meg)
		self.totalAdded += 1
		self.lock.release()
		print("debugLog: totalAdded: {}, datalist length: {}".format(self.totalAdded, len(self.data_list)))

	def DeleteDataList(self):
		self.lock.acquire()
		del self.data_list[:]
		self.lock.release()
		print("debugLog: datalist deleted. datalist length: {}".format(len(self.data_list)))

# if __name__ == '__main__':
# 	room_id_mapping = './content/room_id_mapping.json'
# 	with open(room_id_mapping, encoding='UTF-8') as json_file:
# 		id_mapping_dict = json.load(json_file, encoding='UTF-8')
# 	print(f"mapping_id_res: {id_mapping_dict}")
# 	'Initialize'
# 	mp = model_process(BATCH_SIZE = 100)
# 	'Create a generator, load in the trained model'
# 	mp.prepare_for_generator()
# 	new_txt, new_label = mp.preparer.load_in_texts()
# 	# with open('msg.json') as f:
# 	# 	data = json.load(f)
# 	# pdb.set_trace()
# 	'We assume we have the following inputs'
# 	# data = input_data().return_example_input_list()
# 	# input_data().show_input_data()
# 	'Use a loop to iterate the data'
# 	input_text, input_label = mp.preparer.clip_text(700, new_txt, new_label, start_pos_type=152)
# 	pdb.set_trace()
# 	for single_data in input_text:
# 		'Everytime there is a new message available, feed in the data'
# 		returned_result = mp.feed_in_data(single_data, room_id_label=input_label)
# 		# if len(returned_result) > 0:
# 		# 	pdb.set_trace()

room_id_mapping = './content/room_id_mapping.json'
with open(room_id_mapping, encoding='UTF-8') as json_file:
	id_mapping_dict = json.load(json_file, encoding='UTF-8')

for single in id_mapping_dict:
	print(f"mapping_id_res: {single}, {id_mapping_dict[single]}")

mp = model_process(BATCH_SIZE = 100)
mp.prepare_for_generator()
app = Flask(__name__)

@app.route('/', methods=['POST'])
def processjson():
	data = request.get_json()
	enerated_message = mp.feed_in_data(data['message'], room_id_label=data['room_id'])
	
	if len(generated_message) == 0:
		return jsonify({'result': "not enough input messages"})
	else:
		return jsonify({'result': generated_message})
	
if __name__ == '__main__':
# 	room_id_mapping = './content/room_id_mapping.json'
# 	with open(room_id_mapping, encoding='UTF-8') as json_file:
# 		id_mapping_dict = json.load(json_file, encoding='UTF-8')
# 	for single in id_mapping_dict:
# 		print(f"mapping_id_res: {single}, {id_mapping_dict[single]}")
	
# 	'Initialize'
# 	mp = model_process(BATCH_SIZE = 100)
# 	'Create a generator, load in the trained model'
# 	mp.prepare_for_generator()
# 	app = Flask(__name__)
# 	'do not know why...'
# 	@app.route('/', methods=['POST'])
# 	def processjson():
# 		data = request.get_json()
# 		# pdb.set_trace()
# 		generated_message = mp.feed_in_data(data['message'], room_id_label=data['room_id'])
# 		print(f"read in data message: {data['message']}, with room_id: {data['room_id']} from {id_mapping_dict[str(data['room_id'])]}")
# 		if len(generated_message) == 0:
# 			return jsonify({'result': "not enough input messages"})
# 		else:
# 			return jsonify({'result': generated_message})
	app.run(host='127.0.0.1')
