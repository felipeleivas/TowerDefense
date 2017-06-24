import config

class Effect:
    def __init__(self, name, duration, enemie):
        self._name = name
        self._duration = duration
        self._enemie = enemie

    def getName(self):
        return self._name

    def getDuration(self):
        return self._duration

    def decDuration(self):
        if self._duration == 0:
            self.destroy()
        else:
            self._duration -= 1

    def getEnemie(self):
        return self._enemie

    def destroy(self):
        self._enemie.delEffect(self)

class BurnEffect(Effect):
    def __init__(self, enemie):
        super(BurnEffect, self).__init__(config.Config.BURNEFFECT_NAME, config.Config.BURNEFFECT_DURATION, enemie)
        self._damagePerSecond = config.Config.BURNEFFECT_DAMAGEPERSECOND

    def getDamagePerSecond(self):
        return self._damagePerSecond

class IceEffect(Effect):
    def __init__(self, enemie):
        super(IceEffect, self).__init__(config.Config.ICEEFFECT_NAME, config.Config.ICEEFFECT_DURATION, enemie)
        self._slow = config.Config.ICEEFFECT_SLOW

    def getSlow(self):
        return self._slow
