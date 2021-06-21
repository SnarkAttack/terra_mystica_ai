from enum import Enum, IntEnum

class Terrain(IntEnum):
    NONE = 0
    PLAINS = 1
    SWAMP = 2
    LAKES = 3
    FOREST = 4
    MOUNTAINS = 5
    WASTELAND = 6
    DESERT = 7
    RIVER = 8

class Cults(Enum):
    NONE = 0
    FIRE = 1
    WATER = 2
    EARTH = 3
    AIR = 4

class Buildings(Enum):
    NONE = 0
    DWELLING = 1
    TRADING_POST = 2
    STRONGHOLD = 3
    TEMPLE = 4
    SANCTUARY = 5

class Factions(Enum):
    ALCHEMISTS = 0
    AUREN = 1
    CHAOS_MAGICIANS = 2
    CULTISTS = 3
    DARKLINGS = 4
    DWARVES = 5
    ENGINEERS = 6
    FAKIR = 7
    GIANTS = 8
    HALFLINGS = 9
    MERMAIDS = 10
    NOMADS = 11
    SWARMLINGS = 12
    WITCHES = 13

class BoardType(Enum):
    ORIGINAL = 0