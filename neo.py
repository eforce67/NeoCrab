#!/usr/bin/env python3
import asyncio
import re

import discord
import msgspec

import model

config = model.parse_config('./resources/config.yml')
MAX_USERS = config.get('max_limit', 99999)
DISCORD_TOKEN = config.get('token', None)
CONVERSATION_PATH = config.get('conv_folder', './resources/conversation/')

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

in_session = []

@client.event
async def on_ready():
    print(f'The discord client ({client.user}) is now ready...')

@client.event
async def on_message(message):
    authorID = str(message.author.id)
    if message.content.startswith(client.user.mention) and authorID != str(client.user.id):
        if authorID in in_session:
            await message.reply('Please wait as I\'m still responding to your previous question...')
        else:
            if MAX_USERS >= len(in_session):
                client_mention = re.escape(client.user.mention)
                pattern = rf"{client_mention}\s*|\s+"
                content = re.sub(pattern, ' ', message.content).strip()
                in_session.append(authorID)
                
                async with message.channel.typing():
                    try:
                        with open(f"{CONVERSATION_PATH}{authorID}.json", "rb") as memory_file:
                            memory = msgspec.json.decode(memory_file.read())
                            if len(memory) == 0:
                                memory = {}
                    except FileNotFoundError:
                        memory = {}
                    # Use asyncio.sleep() to keep typing until the bot finishes generating the answer
                    await asyncio.sleep(2.5)  # Adjust the sleep duration as needed
                    response = await client.loop.run_in_executor(None, model.generation, content, memory, authorID)
                    await message.reply(response)
                    in_session.remove(authorID)

async def change_client_status():
    await client.wait_until_ready()

    while not client.is_closed():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{len(in_session)} messages!'))
        await asyncio.sleep(25)
client.loop.create_task(change_client_status())

if __name__ == '__main__':
    client.run(DISCORD_TOKEN)
