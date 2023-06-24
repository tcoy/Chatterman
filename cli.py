import json
import sys
import chatterman

CONFIG_FILENAME = 'config.json'
MEMORY_FILENAME = 'memory.json'

def load_config():
	global config
	try:
		with open(CONFIG_FILENAME) as config_file:
			config = json.load(config_file)
		return True
	except FileNotFoundError:
		return False
	
def load_memory():
	with open(MEMORY_FILENAME, 'w+') as memory_file:
		try:
			return json.load(memory_file)
		except json.JSONDecodeError:
			return {}

def save_memory():
	with open(MEMORY_FILENAME, 'w+') as memory_file:
			memory_file.write(json.dumps(chatterman.memory))
			print("Memory saved")

if not load_config():
	sys.exit("Failed to load cli.py config!")

chatterman.phrase_step = config.get('phrase_step', 1)
chatterman.memory = load_memory()

while True:
	print(chatterman.reply(input()))