import string
import re
import random
import nltk
import unicodedata
import sys
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.corpus import names

memory = {}
phrase_step = 1

def _is_name(word):
	return word.title() in names.words('male.txt') or word.title() in names.words('female.txt')

def _interest_words(s):
	words = set(item for sublist in _tokenize(s) for item in sublist)
	stops = set(stopwords.words('english'))
	return words - stops

def _interest_tokens(s):
	interest_words = _interest_words(s)
	interest_tokens = {}
	for word in interest_words:
		for k, v in memory.items():
			if word in k.split():
				interest_tokens[k] = v
	return interest_tokens

def _weighted_choice(tokens):
	if tokens:
		weights = [v['weight'] for v in tokens.values()]
		keys = [*tokens.keys()]
		if any(w > 0 for w in weights):
			return random.choices(keys, weights = weights, k = 1)[0]
		else:
			return random.choice(keys)
	return None

def _token_left(response):
	words = response.split()
	left = words[0] # get the first word in the phrase
	related = {}
	for k, v in memory.items():
		if left in v['related_words']:
			related[k] = v
	while (choice := _weighted_choice(related)) is not None and choice in response:
		related.pop(choice) # remove any related tokens already included in the response
	if choice is not None:
		return choice.split()[-1]
	return None

def _token_right(response):
	words = response.split()
	right = ' '.join(words[-phrase_step:])
	token = memory.get(right)
	if token:
		related = token['related_words']
		choices = []
		if len(related) > 0:
			weights = []
			for w in related:
				words.append(w) # prepare the word to test
				next_phrase = ' '.join(words[-phrase_step:])
				if next_phrase not in response:
					if w not in choices:
						choices.append(w)
						weights.append(0)
					if (next_token := memory.get(next_phrase)) is not None:
						weights[choices.index(w)] += next_token['weight']
					else:
						weights[choices.index(w)] += token['weight']			
				words.pop()
			if any(w > 0 for w in weights):
				return random.choices(choices, weights = weights, k = 1)[0]
			elif len(choices) > 0: # possible all related words were popped
				return random.choice(choices)
	return None

def _pick_start_token(s):
	interest_tokens = _interest_tokens(s)
	population = interest_tokens if len(interest_tokens) > 0 else memory # use interest tokens if avaiable, else use anything from memory
	return _weighted_choice(population)
	
def _generate_response(s):
	phrase = _pick_start_token(s)
	print('start: ' + phrase)
	response = phrase

	while (right := _token_right(response)) is not None:
		response = response + ' ' + right # append left
		if (left := _token_left(response)) is not None:
			response = left + ' ' + response

	return response

def _has_corpa():
	try:
		nltk.find('tokenizers/punkt')
		nltk.find('corpora/stopwords')
		nltk.find('corpora/names')
		return True
	except LookupError:
		return False
	
unikeys = dict.fromkeys(i for i in range(sys.maxunicode)
                      if unicodedata.category(chr(i)).startswith('P'))

def _sanitize_input(s):
	return s.lower().translate(str.maketrans('', '', string.punctuation)).translate(unikeys)

def _tokenize(s):
	return list(map(word_tokenize, list(map(_sanitize_input, sent_tokenize(s)))))

def read(s):
	sents = _tokenize(s)

	for words in sents:
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
			weight = 4 if any(_is_name(w) for w in phrase.split()) else 1
			if token == None:
				token = {}
				token['weight'] = weight
				token['related_words'] = []
			else:
				token['weight'] += weight

			if related_word not in token['related_words']:
				token['related_words'].append(related_word)
			memory[phrase] = token
	
def reply(s):
	if not _has_corpa():
		return '🙈' # error!
	
	has_memory = len(memory) > 0
	response = '🙊' # no response
	
	if has_memory:
		response = _generate_response(s)
		if random.randint(1, 10)==10: response += ' ' + random.choice(['🥵','😊','🥺','🙈','🙉','🙊','😈','😏','😄','🤢','😬'])

	read(s)

	return response