import discord
import constants
import util.helpers

from collections import defaultdict

def create_critter_view(result, query):
  if len(result) == 1:
    data = result[0]["data"]
    category = result[0]["category"]
    title = f"**{data.get('name', '')}**"

    val = data.get("weather", [])
    weather = ""
    if constants.Weather.SUNNY in val:
      weather += "☀️ Sunny\n"
    if constants.Weather.RAINY in val:
      weather += "🌧️ Rainy\n"
    if constants.Weather.RAINBOW in val:
      weather += "🌈 Rainbow\n"

    val = data.get("time", [])
    time = ""
    if constants.Time.DAWN in val:
      time += f"{constants.Time.DAWN}\n"
    if constants.Time.DAY in val:
      time += f"{constants.Time.DAY}\n"
    if constants.Time.DUSK in val:
      time += f"{constants.Time.DUSK}\n"
    if constants.Time.NIGHT in val:
      time += f"{constants.Time.NIGHT}\n"
  else:
    return