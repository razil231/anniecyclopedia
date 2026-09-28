from discord.ext import commands
from views.help import create_help_view

class HelpCog(commands.Cog):
  def __init__(self, bot: commands.Bot):
    self.bot = bot
    
  @commands.hybrid_command(name = "help", description = "shows all commands", extras = {"syntax": "`hato help <command>`", "args": "`<command>` : command name, *optional*"})
  async def help(self, ctx: commands.Context, *, command: str = None):  
    view = create_help_view(self.bot, command)
    if view:
      await ctx.reply(view = view)
    else:
      await ctx.reply("`Command not found`")


async def setup(bot: commands.Bot):
  await bot.add_cog(HelpCog(bot))