__author__ = 'Matias Estrada'
__version__ = '0.1.0'

import re
import pdb
from collections import Counter

from gensim import corpora, models, similarities, parsing

DATASET_PATH = '/Users/matias/data/inf414/datasets/aan/aan/release/2012/'
ACL_META = 'acl-metadata.txt'

stoplist = set('for a of the and to in with its be can an on from using'.split())

stemmer = parsing.porter.PorterStemmer()


def wrap_documents(lines):
	to_yield = tuple()

	for line in lines:
		line = line.strip()
		# if line == '' and to_yield:
		# 	yield to_yield
		# 	to_yield = None
		if 'id =' in line:
			to_yield += (line.split('=')[1].strip().strip('{}'), )

		if 'title =' in line:
			# yield stemmer.stem_sentence(line.split('=')[1].strip().strip('{}'))
			to_yield += (line.split('=')[1].strip().strip('{}'), )
			yield to_yield
			to_yield = tuple()



def tokenize(str_in):

	texts = [word for word in str_in.lower().split() if word not in stoplist]

	#texts = [[word for word in text if word not in tokens_once] for text in texts]

	return texts


def get_doc_topic(lsi_ins, doc):

	try:
		doc_td = dictionary.doc2bow(tokenize(doc))
		doc_tfidf = tfidf[doc_td]
		# print doc_tfidf

		doc_topic = lsi_ins[doc_tfidf]
		return sorted(doc_topic, key=lambda x: x[1], reverse=True)[0][0]
	except UnicodeDecodeError:
		return -1
	except IndexError:
		return -1


with open(DATASET_PATH + ACL_META, 'r') as acl_meta_file:
	lines = acl_meta_file.readlines()
	# print 'processing docs'
	documents = wrap_documents(lines)
	documents = list(documents)

	# remove common words and tokenize
	texts = [[word for word in document.lower().split() if word not in stoplist]
	         for document in map(lambda x: x[1], documents)]

	# remove words that appear only once
	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

	texts = [[word for word in text if word not in tokens_once] for text in texts]

	dictionary = corpora.Dictionary(texts)
	corp = [dictionary.doc2bow(text) for text in texts]

	# extract 20 LSI topics; use the default one-pass algorithm
	lsi = models.lsimodel.LsiModel(corpus=corp, id2word=dictionary, num_topics=200)

	tfidf = models.tfidfmodel.TfidfModel(corp)

	# doc_to_process = 'Better Punctuation Prediction with Dynamic Conditional Random Fields'

	# print stemmer.stem_sentence(doc_to_process.lower())
	# print get_doc_topic(lsi, stemmer.stem_sentence(doc_to_process.lower()))
	# print stemmer.stem_sentence(doc_to_process.lower())
	# print get_doc_topic(lsi, doc_to_process.lower())
	for doc_id, doc in documents:
		print doc_id, get_doc_topic(lsi, doc.lower())

	# pdb.set_trace()
