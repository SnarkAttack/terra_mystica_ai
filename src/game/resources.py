
class ResourceGroup(object):

    def __init__(self, coins=0, workers=0, priests=0, power=0, vps=0):
        self._coins = coins
        self._workers = workers
        self._priests = priests
        self._power = power
        self._vps = vps

    def get_coins(self):
        return self._coins

    def get_workers(self):
        return self._workers

    def get_priests(self):
        return self._priests

    def get_power(self):
        return self._power

    def get_vps(self):
        return self._vps

    def __add__(self, o):
        return ResourceGroup(
            coins=self._coins + o.get_coins(),
            workers=self._workers + o.get_workers(),
            priests=self._priests + o.get_priests(),
            power=self._power + o.get_power(),
            vp=self._vp + o.get_vp()
        )

    def __sub__(self, o):
        return ResourceGroup(
            coins=self._coins - o.get_coins(),
            workers=self._workers - o.get_workers(),
            priests=self._priests - o.get_priests(),
            power=self._power - o.get_power(),
            vp=self._vp - o.get_vp()
        )

class ResourceRequirements(ResourceGroup):

    def __init__(self, coins=0, workers=0, priests=0, power=0, vp=0):
        super().__init__(coins, workers, priests, power, vp)