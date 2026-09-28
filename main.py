import discord
import os
import importlib
import aiohttp

from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from util.checks import is_dev

import constants
import util.helpers
import views.help

load_dotenv()
token = os.getenv(constants.TOKEN)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix = constants.PREFIX, intents = intents)
bot.remove_command("help")

### ------ HELPER FUNCTIONS START ------ ###
def init_helpers():
  try:
    importlib.reload(constants)
    importlib.reload(util.helpers)
    importlib.reload(views.help)
    print("Helpers loaded")
    return True
  except Exception as e:
    print(f"Helpers load failed: {e}")
    return False

def init_data():
  util.helpers.load_data()
  print("Data loaded")
### ------ HELPER FUNCTIONS START ------ ###


### ------ BOT EVENTS START ------ ###
@bot.event
async def on_ready():
  activity = discord.Activity(type = discord.ActivityType.listening, name = "hato help")
  await bot.change_presence(status = discord.Status.online, activity = activity)

  for cog in util.helpers.load_cogs():
    try:
      await bot.load_extension(cog)
      print(f"Loaded {cog}")
    except Exception as e:
      print(f"Failed to load {cog}: {e}")

  if init_helpers():
    init_data()

  print("Anniecyclopedia is online")

@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
  if isinstance(error, commands.CommandNotFound):
    await ctx.reply("`Not a command`", mention_author = False)
  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.reply(f"Argument missing, please check the correct syntax in `{constants.PREFIX}help [command]`", mention_author = False)
  else:
    await ctx.reply("`Exception caught!`", mention_author = False)
    print(f"Exception: {error}")

@bot.event
async def setup_hook():
  bot.session = aiohttp.ClientSession()

@bot.event
async def close():
  await bot.session.close()
  await super(type(bot), bot).close()
### ------ BOT EVENTS END ------ ###

### ------ BOT COMMANDS START ------ ###
@bot.command(hidden = True)
@is_dev()
async def sync(ctx: commands.Context):
  await bot.tree.sync()
  await ctx.reply("`Commands synced`")

@bot.command(hidden = True)
@is_dev()
async def reload_cog(ctx: commands.Context, cog: str):
  try:
    if cog in bot.extensions:
      await bot.reload_extension(cog)
      await ctx.reply(f"`Extension reloaded: {cog}`")
    else:
      await bot.load_extension(cog)
      util.helpers.save_cog(cog)
      await ctx.reply(f"`Extension loaded: {cog}`")

    if init_helpers():
      init_data()
  except Exception as e:
    await ctx.reply("`Exception caught!`")
    print(f"Exception: {e}")

@bot.command(hidden = True)
@is_dev()
async def reload_helpers(ctx: commands.Context):
  if init_helpers():
    init_data()
    await ctx.reply("`Helpers reloaded`")

@bot.command(hidden = True)
@is_dev()
async def reload_data(ctx: commands.Context):
  init_data()
  await ctx.reply("`Data reloaded`")
### ------ BOT COMMANDS END ------ ###


bot.run(token)