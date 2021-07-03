from ..utilities.mappings import Structures, Factions


class Structure(object):

    def __init__(self, location=None, faction=Factions.NONE, struct_type=Structures.NONE):
        self._location = location
        self._faction = faction
        self._type = struct_type
        self._value = 0

    def get_location(self):
        return self._location

    def get_faction(self):
        return self._faction

    def get_type(self):
        return self._type

    def get_value(self):
        return self._value


class Dwelling(Structure):

    def __init__(self, location, faction):
        super().__init__(location, faction, Structures.DWELLING)
        self._value = 1


class TradingPost(Structure):

    def __init__(self, location, faction):
        super().__init__(location, faction, Structures.TRADING_POST)
        self._value = 2


class Stronghold(Structure):

    def __init__(self, location, faction):
        super().__init__(location, faction, Structures.STRONGHOLD)
        self._value = 3


class Temple(Structure):

    def __init__(self, location, faction):
        super().__init__(location, faction, Structures.TEMPLE)
        self._value = 2


class Sanctuary(Structure):

    def __init__(self, location, faction):
        super().__init__(location, faction, Structures.SANCTUARY)
        self._value = 3