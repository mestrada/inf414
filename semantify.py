__author__ = 'Matias Estrada'
__version__ = '0.1.0'

import re

from collections import Counter

from gensim import corpora, models, similarities

DATASET_PATH = '/home/matias/devel/inf414/datasets/aan/aan/release/2012/'
ACL_META = 'acl-metadata.txt'


def wrap_documents(lines):
	to_yield = None

	for line in lines:
		line = line.strip()
		# if line == '' and to_yield:
		# 	yield to_yield
		# 	to_yield = None
		if 'title' in line:
			yield line.split('=')[1].strip().strip('{}')


with open(DATASET_PATH + ACL_META, 'r') as acl_meta_file:
	lines = acl_meta_file.readlines()
	print 'processing docs'
	documents = wrap_documents(lines)

	# remove common words and tokenize
	stoplist = set('for a of the and to in with its be can an on from using'.split())
	texts = [[word for word in document.lower().split() if word not in stoplist]
	         for document in documents]

	# remove words that appear only once
	all_tokens = sum(texts, [])
	tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)

	texts = [[word for word in text if word not in tokens_once] for text in texts]

	dictionary = corpora.Dictionary(texts)
	corp = [dictionary.doc2bow(text) for text in texts]

	# extract 400 LSI topics; use the default one-pass algorithm
	lsi = models.lsimodel.LsiModel(corpus=corp, id2word=dictionary, num_topics=400)

	# print the most contributing words (both positively and negatively) for each of the first ten topics
	print 'Printing topics'
	print lsi.print_topics(10)