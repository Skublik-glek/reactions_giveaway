import discord
from discord.ext import commands

intents = discord.Intents().default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)
bot.remove_command('help')