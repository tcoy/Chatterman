import json
import sys
import chatterman

CONFIG_FILENAME = 'config.json'
MEMORY_FILENAME = 'memory.json'

def load_memory():
	with open(MEMORY_FILENAME, 'r') as memory_file:
		try:
			return json.load(memory_file)
		except json.JSONDecodeError:
			return {}

chatterman.phrase_step = 2
chatterman.memory = load_memory()

while True:
	print(chatterman.reply(input()))