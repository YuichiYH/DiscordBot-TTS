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

	if not(exists(r'json\channel.json')):
		with open(r'json\channel.json', 'x') as f:
			json.dump({}, f, indent= 4)

	if not(exists(r'json\user.json')):
		with open(r'json\user.json', 'x') as f:
			users = {}
			print(bot.guilds)
			for guild in bot.guilds:
				users[str(guild.id)] = []

			json.dump(users, f, indent= 4)

@bot.event
async def on_message(message):	
	with open(r'json\channel.json', 'r') as f:
		channels = json.load(f)
	if message.author.id == bot.user.id:
		return
	with open(r'json\user.json', "r") as f:
		users = json.load(f)

	print(str(message.author))
	print(str(message.author.id))
	print(str(message.guild.id))
	print(str(users[str(message.guild.id)]))

	if message.content[0] != prefix:
		if (channels[str(message.guild.id)] == str(message.channel.id)):
			if (("<@" + str(message.author.id) + ">") in users[str(message.guild.id)]) or (len(users[str(message.guild.id)]) == 0):
				tts = gtts.gTTS(text = message.content, lang="pt-br")
				tts.save("tts/tts.mp3")
				message.guild.voice_client.play(FFmpegPCMAudio(executable=ffmpeg, source="tts/tts.mp3"))
	await bot.process_commands(message)

@bot.command(name = "channel")
async def channel(ctx):
	with open(r'json\channel.json', 'r') as f:
		channels = json.load(f)
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

@bot.command(name = "disconnect", aliases=["leave","exit"])
async def disconnect(ctx):
	await ctx.voice_client.disconnect()

@bot.command(name = "adduser")
async def adduser(ctx, user):
	with open(r'json\user.json', "r") as f:
		users = json.load(f)
	users[str(ctx.guild.id)].append(user)
	
	with open(r'json\user.json', 'w') as f:
		json.dump(users, f, indent= 4)
	
	await ctx.send("added " + user + "to the list")

@bot.command(name = "removeuser", aliases = ["ruser", "remuser"])
async def removeuser(ctx, user):
	with open(r'json\user.json', "r") as f:
		users = json.load(f)
	
	try:
		users[str(ctx.guild.id)].remove(user)
	except:
		await ctx.send("")

	with open(r'json\user.json', 'w') as f:
		json.dump(users, f, indent= 4)
	
	await ctx.send("removed " + user + "from the list")

async def main():
	await bot.start(token)

asyncio.run(main())