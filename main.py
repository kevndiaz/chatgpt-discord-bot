import discord
import os 
from dotenv import load_dotenv
import openai

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
openai.api_key = os.getenv("OPENAI_API_KEY")


@client.event
async def on_ready():
	print(f'{client.user} connected to server')


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if str(client.user.id) not in message.content:
		return

	n = len(str(client.user.id)) + 3
	msg = message.content[n:]

	response = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=[{"role": "user", "content": msg}],
		temperature=0,
	)

	await message.channel.send(response['choices'][0]['message']['content'])

client.run(TOKEN)
