from ..utilities.mappings import Factions, Cults

class CultTrack(object):

    def __init__(self):
        self._progress_track = [
            [], [], [], [], [], [], [], [], [], [], []
        ]
        self._order_sites_usage = [
            Factions.NONE, Factions.NONE, Factions.NONE, Factions.NONE
        ]
        self._order_sites_value = [
            3, 2, 2, 2
        ]

    def get_faction_location(self, faction):
        for i in range(len(self._progress_track)):
            if faction in self._progress_track[i]:
                return i
        return 0

    def increase_faction_on_cult(self, faction, inc_val):
        curr_location = self.get_faction_location(faction)
        self._progress_track[curr_location].remove(faction)
        self._progress_track[curr_location+inc_val].append(faction)

    def add_faction_to_track(self, faction):
        self._progress_track[0].append(faction)

    def add_priest_to_track(self, faction):
        first_unused = 0
        for i, faction_space in enumerate(self._order_sites_usage):
            if faction_space == Factions.NONE:
                first_unused = i
                break
        self._order_sites_usage[first_unused] = faction
        return self._order_sites_value[first_unused]


class CultBoard(object):

    def __init__(self):
        self._tracks = {
            Cults.FIRE: CultTrack(),
            Cults.WATER: CultTrack(),
            Cults.EARTH: CultTrack(),
            Cults.AIR: CultTrack(),
        }

    def play_priest(self, cult, faction):
        track = self._tracks[cult]
        priest_val = track.add_priest_to_track(faction)
        track.increase_faction_on_cult(faction, priest_val)

    def increase_cult_track(self, cult, faction, inc_val):
        track = self._tracks[cult]
        track.increase_faction_on_cult(faction, inc_val)

    def add_faction_to_cult_board(self, faction):
        for track in self._tracks.values():
            track.add_faction_to_track(faction)

    def get_faction_location_on_cult_track(self, cult, faction):
        track = self._tracks[cult]
        return track.get_faction_location(faction)


