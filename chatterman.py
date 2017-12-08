import discord
import asyncio
import json

from chatterbrain.chatterbrain import ChatterBrain

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


config = {}

if load_config():
    print('Config loaded.')
else:
    print('Failed to load config')
    exit()

client = discord.Client()
brain = ChatterBrain(phrase_step=config.get('phrase_step', 1))

try:
    with open(MEMORY_FILENAME) as memory_file:
        brain.load(memory_file)
        print('Memory loaded')
except FileNotFoundError:
    print('Could not load memory, no file found')

while True:
    line = input()

    if line == 'end':
        with open(MEMORY_FILENAME, "w+") as memory_file:
            brain.save(memory_file)
        break

    brain.learn(line)
    response = brain.get_response(line)

    if response is not None:
        print(response)
