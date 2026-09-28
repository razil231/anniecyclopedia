import discord
import os
import json
import hashlib
import aiohttp
import constants

from io import BytesIO
from PIL import Image

COGS_FILE = "cogs.json"
FISH_FILE = "data/fish.json"
BIRDS_FILE = "data/birds.json"
INSECTS_FILE = "data/insects.json"
FISH_DATA = {}
BIRDS_DATA = {}
INSECTS_DATA = {}
IMAGE_CACHE = {}
IMAGE_CACHE_DIR = "cache/images"
IMAGE_CACHE_MAX = 100

def load_cogs():
  if not os.path.exists(COGS_FILE):
    return []

  with open(COGS_FILE, "r", encoding = "utf-8") as f:
    data = json.load(f)
    return data.get("cogs", [])

def save_cog(cog: str):
  data = {"cogs": []}

  if os.path.exists(COGS_FILE):
    with open(COGS_FILE, "r", encoding = "utf-8") as f:
      data = json.load(f)

  if cog not in data["cogs"]:
    data["cogs"].append(cog)

    with open(COGS_FILE, "w", encoding = "utf-8") as f:
      json.dump(data, f, indent = 4)

def unsave_cog(cog: str):
  if not os.path.exists(COGS_FILE):
    return

  with open(COGS_FILE, "r", encoding = "utf-8") as f:
    data = json.load(f)

  if cog in data["cogs"]:
    data["cogs"].remove(cog)

    with open(COGS_FILE, "w", encoding = "utf-8") as f:
      json.dump(data, f, indent = 4)

def load_data():
  global FISH_DATA, BIRDS_DATA, INSECTS_DATA
  if not os.path.exists(FISH_FILE):
    return
  with open(FISH_FILE, "r", encoding = "utf-8") as f:
    FISH_DATA = json.load(f)
    
  if not os.path.exists(BIRDS_FILE):
    return
  with open(BIRDS_FILE, "r", encoding = "utf-8") as f:
    BIRDS_DATA = json.load(f)
    
  if not os.path.exists(INSECTS_FILE):
    return
  with open(INSECTS_FILE, "r", encoding = "utf-8") as f:
    INSECTS_DATA = json.load(f)

def get_cache(path: str):
  filename = f"{hashlib.md5(path.encode()).hexdigest}.webp"
  return os.path.join(IMAGE_CACHE_DIR, filename)

async def get_image_file(url: str):
  async with aiohttp.ClientSession() as s:
    async with s.get(url) as res:
      if res.status != 200:
        # raise Exception("Failed to fetch image")
        print("Failed to fetch image")
        return

      data = await res.read()

  img = Image.open(BytesIO(data))
  img = img.convert("RGBA")

  output = BytesIO()
  img.save(output, format = "PNG")
  return output.getvalue()

async def get_image(name: str):
  global IMAGE_CACHE
  img = None

  filename = name.lower().replace(" ", "_").replace("'", "")
  key = f"{filename}.webp"
  if key in IMAGE_CACHE:
    img = IMAGE_CACHE[key]
  else:
    disk = get_cache(key)
    if os.path.exists(disk):
      with open(disk, "rb") as f:
        img = f.read()

      IMAGE_CACHE[key] = img

  if img is None:
    img = await get_image_file(f"{constants.IMAGE_HOST}/{key}")
    if img is None:
      return None

    IMAGE_CACHE[key] = img

    with open(disk, "wb") as f:
      f.write(img)

  if len(IMAGE_CACHE) > IMAGE_CACHE_MAX:
    IMAGE_CACHE.pop(next(iter(IMAGE_CACHE)))

  return discord.File(fp = BytesIO(img), filename = "image.png")