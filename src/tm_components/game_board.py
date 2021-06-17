from ..mappings import Terrain

class GameBoard(object):
     def __init__(self):
         self._locations = []
         self._components = []

class OriginalGameBoard(object):
    def __init__(self):
        self._locations = [
            [Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.FOREST, Terrain.LAKES, Terrain.DESERT, Terrain.WASTELAND, Terrain.PLAINS, Terrain.SWAMP, Terrain.WASTELAND, Terrain.FOREST, Terrain.LAKES, Terrain.WASTELAND, Terrain.SWAMP],
            [Terrain.DESERT, Terrain.PLAINS, Terrain.SWAMP, Terrain.DESERT, Terrain.SWAMP, Terrain.DESERT],
            [Terrain.SWAMP, Terrain.MOUNTAINS, Terrain.FOREST, Terrain.FOREST, Terrain.MOUNTAINS],
            [Terrain.FOREST, Terrain.LAKES, Terrain.DESERT, Terrain.WASTELAND, Terrain.LAKES, Terrain.WASTELAND, Terrain.WASTELAND, Terrain.PLAINS],
            [Terrain.SWAMP, Terrain.PLAINS, Terrain.WASTELAND, Terrain.LAKES, Terrain.SWAMP, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.DESERT, Terrain.FOREST, Terrain.SWAMP, Terrain.LAKES],
            [Terrain.MOUNTAINS, Terrain.FOREST, Terrain.DESERT, Terrain.FOREST, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.PLAINS],
            [Terrain.MOUNTAINS, Terrain.WASTELAND, Terrain.FOREST, Terrain.DESERT, Terrain.SWAMP, Terrain.LAKES, Terrain.DESERT],
            [Terrain.DESERT, Terrain.LAKES, Terrain.PLAINS, Terrain.LAKES, Terrain.SWAMP, Terrain.MOUNTAINS, Terrain.PLAINS, Terrain.MOUNTAINS],
            [Terrain.WASTELAND, Terrain.SWAMP, Terrain.MOUNTAINS, Terrain.LAKES, Terrain.WASTELAND, Terrain.FOREST, Terrain.DESERT, Terrain.PLAINS, Terrain.MOUNTAINS, Terrain.LAKES, Terrain.FOREST, Terrain.WASTELAND]
        ]
