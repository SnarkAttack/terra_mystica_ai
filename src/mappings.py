from enum import Enum

class Terrain(Enum):
    NONE = -1
    PLAINS = 0
    SWAMP = 1
    LAKES = 2
    FOREST = 3
    MOUNTAINS = 4
    WASTELAND = 5
    DESERT = 6

class Cults(Enum):
    NONE = -1
    FIRE = 0
    WATER = 1
    EARTH = 2
    AIR = 3

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