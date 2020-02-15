import re
from sklearn.metrics.pairwise import cosine_similarity
import torch
import pickle
import numpy as np
from pytorch_pretrained_bert import BertTokenizer, BertModel
from nltk.stem import WordNetLemmatizer

from WordNet_Lookup import WN_lookup

class BERT:

	def __init__(self):

		print('Initializing tokenizer')
		self.tokenizer = BertTokenizer.from_pretrained('bert-large-uncased')

		print('Loading pretrained model')
		self.model = BertModel.from_pretrained('bert-large-uncased')
		self.model.eval()

		self.model.to(torch.device("cpu"))

class BERT_pred:
	sense_number_map = {'N': 1, 'V': 2, 'J': 3, 'R': 4}

	def __init__(self, emb_pickle_file):
		print('Creating BERT model...')
		self.Bert_Model = BERT()

		print('Loading embeddings')
		self.lemmatizer = WordNetLemmatizer()
		self.word_sense_emb = self.load_embeddings(
			emb_pickle_file)

		print('Ready!')

	def apply_bert_tokenizer(self, word):
		return self.Bert_Model.tokenizer.tokenize(word)

	def predict(self, sentence, word, k = 1):
		# parse / clean sentence
		sentence = re.findall(r"[\w']+|[.,!?;]", sentence)

		index = sentence.index(word)
		indices = [0] * len(sentence)
		indices[index] = 1

		bert_tokens = self.collect_bert_tokens(sentence)

		final_layer = self.get_bert_embeddings(bert_tokens)

		count, tag, nn_sentences = 1, [], []

		sense_emb, sentence_maps, sense_word_map, word_sense_map = self.create_word_sense_maps()

		for idx, j in enumerate(zip(indices, sentence)):
			word = j[1]

			# predict this word?
			if j[0] != 0:

				_temp_tag = 0
				max_score = -99
				nearest_sent = 'NONE'

				embedding = np.mean(
					final_layer[count:count + len(self.apply_bert_tokenizer(word))], 0)

				min_span = 10000

				if word in word_sense_map:
					concat_senses = []
					concat_sentences = []
					index_maps = {}
					_reduced_sense_map = []

					if len(_reduced_sense_map) == 0:
						_reduced_sense_map = list(word_sense_map[word])

					for sense_id in _reduced_sense_map:
						index_maps[sense_id] = {}
						index_maps[sense_id]['start'] = len(concat_senses)

						concat_senses.extend(sense_emb[sense_id])
						concat_sentences.extend(sentence_maps[sense_id])

						index_maps[sense_id]['end'] = len(
							concat_senses) - 1
						index_maps[sense_id]['count'] = 0

						if min_span > (index_maps[sense_id]['end'] - index_maps[sense_id]['start'] + 1):

							min_span = (index_maps[sense_id][
										'end'] - index_maps[sense_id]['start'] + 1)

					min_nearest = min(min_span, k)

					concat_senses = np.array(concat_senses)

					simis = cosine_similarity(
						embedding.reshape(1, -1), concat_senses)[0]
					nearest_indexes = simis.argsort(
					)[-min_nearest:][::-1]

					for idx1 in nearest_indexes:

						for sense_id in _reduced_sense_map:

							if index_maps[sense_id]['start'] <= idx1 and index_maps[sense_id]['end'] >= idx1:
								index_maps[sense_id]['count'] += 1

								score = index_maps[sense_id]['count']

								if score > max_score:
									max_score = score
									_temp_tag = sense_id
									nearest_sent = concat_sentences[idx1]

				tag.append(_temp_tag)
				nn_sentences.append(nearest_sent)

			count += len(self.apply_bert_tokenizer(word))

		res = []
		for t in tag:
			res.append(WN_lookup(t))

		return res

	def get_bert_embeddings(self, tokens):

		_ib = self.Bert_Model.tokenizer.convert_tokens_to_ids(tokens)
		_st = [0] * len(_ib)

		_t1, _t2 = torch.tensor([_ib]), torch.tensor([_st])

		with torch.no_grad():

			_encoded_layers, _ = self.Bert_Model.model(
				_t1, _t2, output_all_encoded_layers=True)

			_e1 = _encoded_layers[-4:]

			_e2 = torch.cat((_e1[0], _e1[1], _e1[2], _e1[3]), 2)

			_final_layer = _e2[0].numpy()

		return _final_layer

	def collect_bert_tokens(self, _sent, lemma=False):

		_bert_tokens = ['[CLS]', ]

		if lemma:

			for idx, j in enumerate(_sent):

				_sent[idx] = self.lemmatizer.lemmatize(_sent[idx])
				_tokens = self.apply_bert_tokenizer(_sent[idx])
				_bert_tokens.extend(_tokens)

		else:

			for idx, j in enumerate(_sent):

				_tokens = self.apply_bert_tokenizer(_sent[idx])

				_bert_tokens.extend(_tokens)

		_bert_tokens.append('[SEP]')

		return _bert_tokens

	def load_embeddings(self, pickle_file):
		with open(pickle_file, 'rb') as h:
			_x = pickle.load(h)

			print("EMBEDDINGS FOUND")
			return _x

	def create_word_sense_maps(self):

		_sense_emb = {}
		_sentence_maps = {}
		_sense_word_map = {}
		_word_sense_map = {}

		for i in self.word_sense_emb:

			if i not in _word_sense_map:
				_word_sense_map[i] = []

			for j in self.word_sense_emb[i]:

				if j not in _sense_word_map:
					_sense_word_map[j] = []

				_sense_word_map[j].append(i)
				_word_sense_map[i].append(j)

				if j not in _sense_emb:
					_sense_emb[j] = []
					_sentence_maps[j] = []

				_sense_emb[j].extend(self.word_sense_emb[i][j]['embs'])
				_sentence_maps[j].extend(self.word_sense_emb[i][j]['sentences'])

		return _sense_emb, _sentence_maps, _sense_word_map, _word_sense_map