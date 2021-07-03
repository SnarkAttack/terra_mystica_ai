from enum import Enum, IntEnum

class Terrains(IntEnum):
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

class Structures(IntEnum):
    NONE = 0
    DWELLING = 1
    TRADING_POST = 2
    STRONGHOLD = 3
    TEMPLE = 4
    SANCTUARY = 5

class Factions(IntEnum):
    NONE = 0
    ALCHEMISTS = 1
    AUREN = 2
    CHAOS_MAGICIANS = 3
    CULTISTS = 4
    DARKLINGS = 5
    DWARVES = 6
    ENGINEERS = 7
    FAKIR = 8
    GIANTS = 9
    HALFLINGS = 10
    MERMAIDS = 11
    NOMADS = 12
    SWARMLINGS = 13
    WITCHES = 14

class BoardType(Enum):
    NONE = 0
    ORIGINAL = 1

class GamePhase(Enum):
    UNKNOWN = 0
    SETUP = 1
    INCOME = 2
    ACTION = 3
    CULT_BONUSES = 4
    CLEANUP = 5

class MoveType(Enum):
    NONE = 0
    ACTION = 1
    SIPHON_POWER = 2
    PLACE_DWELLING = 3