import discord

from discord.ext import commands

def create_help_view(bot: commands.Bot, command: str = None):
  command = command.lower() if command else None
  title = f"Info for command `{command}`" if command else "Available commands"
  cmd = bot.get_command(command) if command else None
  if command and not cmd:
    return None

  view = discord.ui.LayoutView()

  container = discord.ui.Container(
    discord.ui.TextDisplay(f"### {title}"),
    discord.ui.Separator(),
    accent_color = discord.Color(0xEE92D5)
  )

  if not cmd:
    cmds = bot.commands
    for cmd in cmds:
      if not cmd.hidden:
        container.add_item(discord.ui.Separator(visible = False))
        container.add_item(discord.ui.TextDisplay(f"**`{cmd.extras.get('syntax')}`**"))
        container.add_item(discord.ui.TextDisplay(f"- {cmd.description}"))

    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay(f"-# `hato help <command>` for detailed info"))
  else:
    container.add_item(discord.ui.TextDisplay(f"**`{cmd.extras.get('syntax')}`**"))
    params = cmd.extras.get("args")
    if params is not None:
      container.add_item(discord.ui.TextDisplay(f"> {params}"))

    container.add_item(discord.ui.Separator())
    container.add_item(discord.ui.TextDisplay(f"-# Slash version is also available: `/{cmd.name}`"))

  view.add_item(container)
  return view