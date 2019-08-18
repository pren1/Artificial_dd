'prepare for the whole process'
import pdb
import pickle
import numpy as np
import json
from tqdm import tqdm
import copy
import random

class process_prepare(object):
	def __init__(self, target_path_folder):
		'load in characters, and embedding matrix'
		with open('./{}/glove-512-words.pkl'.format(target_path_folder), 'rb') as f:
			self.characters = pickle.load(f)
			'also add end part, and beginning part'
			self.characters[-1] = 'eos'
			self.characters[0] = '\n'
		self.preprocessed_TXT = './{}/new_filtered_data.json'.format(target_path_folder)
		self.embedding_matrix = np.load('./{}/glove-512.npy'.format(target_path_folder))

		'define transfer things'
		self.char_to_n = {char: n for n, char in enumerate(self.characters)}
		self.n_to_char = {n: char for n, char in enumerate(self.characters)}

	def transform(self, txt):
		return np.asarray([self.char_to_n[c] for c in txt], dtype=np.int32)

	def load_in_texts(self):
		'get some real text inputs'
		with open(self.preprocessed_TXT, encoding='UTF-8') as json_file:
			data = json.load(json_file, encoding='UTF-8')
			'process the data'
			txt = []
			for single_meg in data:
				single_meg.insert(0, 'eos')
				single_meg.append('\n')
				txt.extend(single_meg)
			'remove that does not belongs to characters...'
			new_txt = []
			for sing in tqdm(txt):
				sing = sing.lower()
				if sing != '鸨儿':
					new_txt.append(sing)
			print("updated txt, remove from {} to {}, examples: {}".format(len(txt), len(new_txt), new_txt[:20]))
			return new_txt

	def delete_EOS(self, input: list) -> list:
		while 'eos' in input:
			input.remove('eos')
		str1 = "".join(input)
		res = str1.split('\n')
		del res[-1]
		for single in res:
			print(single)
		return res

	def clip_text(self, txt_length, new_txt):
		'a good way to show the input text'
		start_index = random.randint(0, len(new_txt) - txt_length)
		clipped_txt_for_test = new_txt[start_index:start_index + txt_length]
		self.delete_EOS(copy.deepcopy(clipped_txt_for_test))
		return clipped_txt_for_test

