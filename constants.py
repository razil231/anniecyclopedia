from enum import Enum

### Development
DEV_IDS = {
    614436287377571840,
}

### Constants
TOKEN = "TOKEN"
PREFIX = "hato "
ICON = "<:annie:1553723701973749911>"
IMAGE_HOST = "https://wangsi231.x02.me/i"

### Classes
class Critter(Enum):
    FISH = "fish"
    BIRDS = "birds"
    INSECTS = "insects"

class Weather(Enum):
    SUNNY = "Sunny"
    RAINY = "Rainy"
    RAINBOW = "Rainbow"
    METEOR = "Meteor"
    SNOW = "Snow"
    HARSH = "Harsh Sunlight"

class Time(Enum):
    DAWN = "Dawn"
    DAY = "Day"
    DUSK = "Dusk"
    NIGHT = "Night"