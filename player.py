import config

# Classe Player:
# Classe que define a profile do jogador atual, assim como os
# atributos que ele tem da partida atual.
class Player:
    def __init__(self, name):
        self._name = name
        self._cash = config.Config.PLAYER_CASH
        self._life = config.Config.PLAYER_LIFE

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def getCash(self):
        return self._cash

    def setCash(self, cash):
        self._cash = cash

    def purchaseObject(self, objectPrice):
        self._cash = self._cash - objectPrice

    def haveCashToBuy(self, towerPrice):
        if towerPrice > self._cash:
            return False
        else:
            return True

    def getLife(self):
        return self._life

    def setLife(self, life):
        self._life = life

    def decLife(self):
        self._life -= 1

    def getName(self):
        return self._name