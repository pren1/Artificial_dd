'prepare for the whole process'
import pdb
import pickle
import numpy as np
import json
from tqdm import tqdm
import copy
import random
import jieba
jieba.set_dictionary("./dict.txt")
jieba.initialize()

class process_prepare(object):
	def __init__(self, target_path_folder):
		'load in characters, and embedding matrix'
		with open('./{}/glove-512-words.pkl'.format(target_path_folder), 'rb') as f:
			self.characters = pickle.load(f)
			'also add end part, and beginning part'
			self.characters[-1] = 'eos'
			self.characters[-2] = '\n'
		self.preprocessed_TXT = './{}/pure_live_512.json'.format(target_path_folder)
		self.embedding_matrix = np.load('./{}/glove-512.npy'.format(target_path_folder))

		'define transfer things'
		self.char_to_n = {char: n for n, char in enumerate(self.characters)}
		self.n_to_char = {n: char for n, char in enumerate(self.characters)}

	def transform(self, txt):
		return np.asarray([self.char_to_n[c] for c in txt], dtype=np.int32)

	def create_custom_dict(self):
		with open('custom_dict.txt', 'w',encoding='UTF-8') as f:
			for item in self.characters[1:]:
				f.write("%s\n" % item)

	def cut_target_seq(self, target_data):
		# jieba.load_userdict("./custom_dict.txt")
		word_list = jieba.lcut(target_data)
		'after we cut this part, apply a filter'
		res = []
		for single_word in word_list:
			if single_word in self.characters:
				res.append(single_word)
		# pdb.set_trace()
		'this part should be uncommented'
		res.insert(0, 'eos')
		res.append('\n')
		return res

	def load_in_texts(self):
		with open(self.preprocessed_TXT, encoding='UTF-8') as json_file:
			data = json.load(json_file, encoding='UTF-8')
			'process the data'
			txt = []
			label_part = []
			for single_meg in tqdm(data):
				single_meg[0].insert(0, 'eos')
				single_meg[0].append('\n')
				label = [single_meg[1]] * len(single_meg[0])
				txt.extend(single_meg[0])
				label_part.extend(label)

			'remove that does not belongs to characters...'
			new_txt = []
			new_label_part = []
			for (single, label) in tqdm(zip(txt, label_part)):
				if single not in ['口呆口', 'magnet']:
					new_txt.append(single)
					new_label_part.append(label)
			print("updated txt, remove from {} to {}, examples: {}".format(len(txt), len(new_txt), new_txt[:20]))
			return new_txt, new_label_part

	def delete_EOS(self, input: list) -> list:
		while 'eos' in input:
			input.remove('eos')
		str1 = "".join(input)
		res = str1.split('\n')
		del res[-1]
		for single in res:
			print(single)
		return res

	def clip_text(self, txt_length, new_txt, new_label, start_pos_type=0):
		proposed_start_index = new_label.index(start_pos_type)
		'Currently, we only support 355 vtubers'
		proposed_end_index = new_label.index(min(start_pos_type + 1, 355))
		start_index = random.randint(proposed_start_index, proposed_end_index - txt_length)
		clipped_txt_for_test = new_txt[start_index:start_index + txt_length]
		clipped_labels_for_test = new_label[start_index:start_index + txt_length]
		self.delete_EOS(copy.deepcopy(clipped_txt_for_test))
		return clipped_txt_for_test, clipped_labels_for_test[0]