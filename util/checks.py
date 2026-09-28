from discord.ext import commands
from constants import DEV_IDS

def is_dev():
  async def predicate(ctx: commands.Context):
    return ctx.author.id in DEV_IDS

  return commands.check(predicate)