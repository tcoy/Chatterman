import json
import sys
import chatterman
import discord
import atexit
import signal

CONFIG_FILENAME = './config.json'
MEMORY_FILENAME = './memory.json'

def load_config():
	global config
	try:
		with open(CONFIG_FILENAME) as config_file:
			config = json.load(config_file)
		return True
	except FileNotFoundError:
		return False
	
def load_memory():
	with open(MEMORY_FILENAME, 'r') as memory_file:
		try:
			return json.load(memory_file)
		except json.JSONDecodeError:
			return {}

def save_memory():
	with open(MEMORY_FILENAME, 'w+') as memory_file:
			memory_file.write(json.dumps(chatterman.memory))
			print("Memory saved")

def sig_handler(signo, frame):
    sys.exit(0)

if not load_config():
	sys.exit("Failed to load bot.py config!")

chatterman.phrase_step = config.get('phrase_step', 1)
chatterman.memory = load_memory()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
	print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
	if message.author.bot:
		return

	if client.user.mention in message.content:
		response = chatterman.reply(message.content.replace(client.user.mention, ''))
		out = message.author.mention + " " + response
		await message.channel.send(out)

atexit.register(save_memory)
signal.signal(signal.SIGTERM, sig_handler)
client.run(config['token'])