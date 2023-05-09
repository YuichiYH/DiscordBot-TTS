import asyncio
import discord
import gtts
from discord.ext import commands
from discord import FFmpegPCMAudio
import json
import os
from os.path import exists
import gtts



# Get configuration.json
with open("configuration.json", "r") as config: 
	data = json.load(config)
	token = data["token"]
	prefix = data["prefix"]
	owner_id = data["owner_id"]

ffmpeg = "C:/ffmpeg/bin/ffmpeg.exe"
botctx = False

class Greetings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self._last_member = None

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.messages = True
# The bot
bot = commands.Bot(prefix, intents = intents, owner_id = owner_id)

@bot.event
async def on_ready():
	print(f"We have logged in as {bot.user}")
	print(discord.__version__)
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name =f"{bot.command_prefix}help"))

@bot.event
async def on_message(message):	
	if message.author.id == bot.user.id:
		return
	
	if message.content[0] != "|":
		if channels[str(message.guild.id)] == str(message.channel.id):
			tts = gtts.gTTS(text = message.content, lang="pt-br")
			tts.save("tts/tts.mp3")
			message.guild.voice_client.play(FFmpegPCMAudio(executable=ffmpeg, source="tts/tts.mp3"))
	await bot.process_commands(message)

@bot.command(name = "channel")
async def channel(ctx):
	read_channel = ctx.message.channel

	channels[str(ctx.guild.id)] = str(read_channel.id)
	with open(r'json\channel.json', 'w') as f:
		json.dump(channels, f, indent=4)

	await ctx.send(f"{read_channel} selected for tts")

@bot.command(name = "connect", aliases=["enter","join"])
async def connect(ctx):

	print("connected")

	channel = ctx.author.voice.channel

	await channel.connect()

if not(exists(r'json\channel.json')):
	with open(r'json\channel.json', 'x') as f:
		json.dump({}, f)

if not(exists(r'json\user.json')):
	with open(r'json\user.json', 'x') as f:
		guilds = {}

with open(r'json\channel.json', 'r') as f:
	channels = json.load(f)

with open(r'json\user.json', "r") as f:
	users = json.load(f)



bot.run(token)