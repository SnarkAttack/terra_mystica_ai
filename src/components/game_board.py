from ..mappings import Terrain

class GameBoard(object):
     def __init__(self):
         self._locations = []
         self._components = []

class OriginalGameBoard(GameBoard):
    def __init__(self):
        self._locations = [
            [Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.FOREST, Terrain.LAKES, Terrain.DESERT, Terrain.WASTELAND, Terrain.PLAINS, Terrain.SWAMP, Terrain.WASTELAND, Terrain.FOREST, Terrain.LAKES, Terrain.WASTELAND, Terrain.SWAMP],
            [Terrain.DESERT, Terrain.RIVER, Terrain.RIVER, Terrain.PLAINS, Terrain.SWAMP, Terrain.RIVER, Terrain.RIVER, Terrain.DESERT, Terrain.SWAMP, Terrain.RIVER, Terrain.RIVER, Terrain.DESERT],
            [Terrain.RIVER, Terrain.RIVER, Terrain.SWAMP, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.FOREST, Terrain.RIVER, Terrain.FOREST, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.RIVER],
            [Terrain.FOREST, Terrain.LAKES, Terrain.DESERT, Terrain.RIVER, Terrain.RIVER, Terrain.WASTELAND, Terrain.LAKES, Terrain.RIVER, Terrain.WASTELAND, Terrain.RIVER, Terrain.WASTELAND, Terrain.PLAINS],
            [Terrain.SWAMP, Terrain.PLAINS, Terrain.WASTELAND, Terrain.LAKES, Terrain.SWAMP, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.DESERT, Terrain.RIVER, Terrain.RIVER, Terrain.FOREST, Terrain.SWAMP, Terrain.LAKES],
            [Terrain.MOUNTAINS, Terrain.FOREST, Terrain.RIVER, Terrain.RIVER, Terrain.DESERT, Terrain.FOREST, Terrain.RIVER, Terrain.RIVER, Terrain.RIVER, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.PLAINS],
            [Terrain.RIVER, Terrain.RIVER, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.WASTELAND, Terrain.RIVER, Terrain.FOREST, Terrain.RIVER, Terrain.DESERT, Terrain.SWAMP, Terrain.LAKES, Terrain.DESERT],
            [Terrain.DESERT, Terrain.LAKES, Terrain.PLAINS, Terrain.RIVER, Terrain.RIVER, Terrain.RIVER, Terrain.LAKES, Terrain.SWAMP, Terrain.RIVER, Terrain.MOUNTAINS, Terrain.PLAINS, Terrain.MOUNTAINS],
            [Terrain.WASTELAND, Terrain.SWAMP, Terrain.MOUNTAINS, Terrain.LAKES, Terrain.WASTELAND, Terrain.FOREST, Terrain.DESERT, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.RIVER, Terrain.LAKES, Terrain.FOREST, Terrain.WASTELAND]
        ]
