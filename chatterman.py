import string
import re
import random

import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

memory = {}
phrase_step = 1

def _get_phrases_of_interest(str):
	phrases = []
	sents = sent_tokenize(str)

	for sent in sents:
		words = [word for word in word_tokenize(
			re.sub('[' + string.punctuation + ']', '', sent)) if word.lower() not in stopwords.words('english')]

		for word in words:
			for phrase in memory:
				token = memory[phrase]
				if word in token['related_words'] and phrase not in phrases:
					phrases.append(phrase)

	return phrases

def _has_corpa():
	try:
		nltk.find('tokenizers/punkt')
		nltk.find('corpora/stopwords')
		return True
	except LookupError:
		return False
	
def read(str):
	sents = sent_tokenize(str.lower())

	for sent in sents:
		words = word_tokenize(
			re.sub('[' + string.punctuation + ']', '', sent))

		if len(words) <= phrase_step:
			continue

		for i in range(0, len(words)):
			phrase = ' '.join(words[i:i + phrase_step:1])
			related_word = None

			if i + phrase_step < len(words):
				related_word = words[i + phrase_step]
			else:
				break

			token = memory.get(phrase)

			if token == None:
				token = {}
				token['weight'] = 0
				token['related_words'] = []
			else:
				token['weight'] += 1

			token['related_words'].append(related_word)
			memory[phrase] = token
	
def reply(str):
	if not _has_corpa():
		return '\U0001F648' # error!
	
	str = str.lower()
	has_memory = len(memory) > 0
	response = '\U0001F64A' # no response
	
	if has_memory:
		phrases_of_interest = _get_phrases_of_interest(str)

		start_phrase = random.choice(list(phrases_of_interest)) if len(
			phrases_of_interest) > 0 else random.choice(list(memory))
		current_phrase = start_phrase
		current_token = memory[current_phrase]
		response = current_phrase
		used_phrases = [current_phrase]
		while len(current_token['related_words']) > 0:
			next_word = random.choice(current_token['related_words'])
			response += ' ' + next_word
			full_phrase = word_tokenize(current_phrase)
			full_phrase.append(next_word)
			next_phrase = ' '.join(full_phrase[len(full_phrase) - phrase_step::])

			if next_phrase not in memory or next_phrase in used_phrases:
				break

			current_phrase = next_phrase
			current_token = memory[current_phrase]
			used_phrases.append(current_phrase)

	read(str)

	return response