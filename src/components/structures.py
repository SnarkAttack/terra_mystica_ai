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

    @classmethod
    def create_structure(cls, struct_type, location_code, faction):
        if struct_type == Structures.DWELLING:
            return Dwelling(location_code, faction)
        elif struct_type == Structures.TRADING_POST:
            return TradingPost(location_code, faction)
        elif struct_type == Structures.STRONGHOLD:
            return Stronghold(location_code, faction)
        elif struct_type == Structures.TEMPLE:
            return Temple(location_code, faction)
        elif struct_type == Structures.SANCTUARY:
            return Sanctuary(location_code, faction)
        else:
            raise ValueError("Trying to create unknown structure type")


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