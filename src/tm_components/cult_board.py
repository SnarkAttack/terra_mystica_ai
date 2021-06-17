from ..mappings import Terrain, Cults

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
            Cults.FIRE: CultTrack(),
            Cults.WATER: CultTrack(),
            Cults.EARTH: CultTrack(),
            Cults.AIR: CultTrack(),
        }