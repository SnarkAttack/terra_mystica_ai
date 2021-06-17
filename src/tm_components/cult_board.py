from ..mappings import Terrain

class CultTrack(object):

    def __init__(self):
        self._progress_track = [
            [], [], [], [], [], [], [], [], [], []
        ]
        self._order_sites_usage = [
            Terrain.None, Terrain.None, Terrain.None, Terrain.None
        ]
        self._order_sites_value = [
            3, 2, 2, 2
        ]


class CultBoard(object):

    def __init__(self):
        tracks = {
            "fire": CultTrack(),
            "water": CultTrack(),
            "earth": CultTrack(),
            "air": CultTrack(),
        }