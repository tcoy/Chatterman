import discord
import asyncio
import json
import sys

from chatterbrain.chatterbrain import ChatterBrain
from chatterbrain.teachers.reddit import RedditTeacher

CONFIG_FILENAME = 'config.json'
MEMORY_FILENAME = 'memory.json'

client = discord.Client()
config = {}


def load_config():
    global config
    try:
        with open(CONFIG_FILENAME) as config_file:
            config = json.load(config_file)
        return True
    except FileNotFoundError:
        return False


if load_config():
    print('Config loaded.')
else:
    print('Failed to load config')
    exit()

brain = ChatterBrain(phrase_step=config.get('phrase_step', 1))
reddit_teacher = RedditTeacher(brain)


def save_brain():
    global brain
    with open(MEMORY_FILENAME, 'w+') as memory_file:
        brain.save(memory_file)
        print("Saved memory")


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if client.user.mention in message.content:
        if message.author.id in config["authority"]:
            if 'die' in message.content:
                await client.send_message(message.channel, "x_x")
                save_brain()
                client.logout()
                sys.exit()
                return
            elif '.reddit' in message.content:
                cmd = message.content.split()
                if len(cmd) > 1:
                    response = message.author.mention + ' '

                    if reddit_teacher.teach(cmd[2]):
                        response += 'ok'
                    else:
                        response += 'i cant'

                    await client.send_message(
                        message.channel, response)
                return

        response = brain.get_response(message.content)

        if response is not None:
            out = message.author.mention + " " + response
            await client.send_message(message.channel, out)

    brain.learn(message.content.replace(client.user.mention, ''))
try:
    with open(MEMORY_FILENAME) as memory_file:
        brain.load(memory_file)
        print('Memory loaded')
except FileNotFoundError:
    print('Could not load memory, no file found')

client.run(config['token'])
