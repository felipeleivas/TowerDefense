import rectangle
import abc
import config
import pygame
import effects

class Trap(rectangle.Rectangle):
    _mouseCircleSurface = pygame.Surface(config.Config.MOUSE_CIRCLE_SURFACE)

    def __init__(self, position, width, height, image, damage, price):
        super(Trap, self).__init__(position, width, height, image)
        self._damage = damage
        self._reloadTime = 2.0
        self._price = price

    def getFirstClass(self):
        return "Trap"

    @abc.abstractmethod
    def getClass(self):
        return

    @abc.abstractmethod
    def newCopy(self):
        return

    def getDamage(self):
        return self._damage

    def setDamage(self, damage):
        self._damage = damage

    def getPrice(self):
        return self._price

    def setPrice(self, price):
        self._price = price

    def doublePrice(self):
        self._price = self._price * 2

    def decReloadTime(self):
        self._reloadTime -= 2.0

    def resetReloadTime(self):
        self._reloadTime = 3
    #print self._reloadTime

    def shotEnemies(self, enemies, towerDefense):
        if self._reloadTime <= 0:
            for enemieAux in enemies:
                if self.collide(enemieAux):
                    self.shot(enemieAux)
                    self.resetReloadTime()
                    break

    def paintRange(self, gameDisplay, color):
        self._mouseCircleSurface.fill(config.Config.CK)
        self._mouseCircleSurface.set_colorkey(config.Config.CK)
        pygame.draw.circle(self._mouseCircleSurface, color, self.getCenter(), 16, 16)
        self._mouseCircleSurface.set_alpha(150)
        gameDisplay.blit(self._mouseCircleSurface, (0, 0))

    def paintAtributes(self, gameDisplay):
        font = pygame.font.SysFont(None, 25, True, False)
        text = font.render("Damage:%d" % self._damage, True, (0, 0, 0))
        gameDisplay.blit(text, (497, 177))

class FireTrap(Trap):
    def __init__(self, position):
        super(FireTrap, self).__init__(position,
                                           config.Config.FIRETRAP_WIDTH,
                                           config.Config.FIRETRAP_HEIGHT,
                                           config.Config.FIRETRAP_IMAGE,
                                           config.Config.FIRETRAP_DAMAGE,
                                           config.Config.FIRETRAP_PRICE)

    def getClass(self):
        return "FireTrap"

    def newCopy(self):
        return FireTrap(self._position)

    def shot(self, enemie):
        burnEffect = effects.BurnEffect(enemie)
        enemie.setBurn(burnEffect)


class FireTrapBuyer(Trap):
    def __init__(self, position):
        super(FireTrapBuyer, self).__init__(position,
                                            config.Config.FIRETRAP_WIDTH,
                                            config.Config.FIRETRAP_HEIGHT,
                                            config.Config.FIRETRAP_IMAGE,
                                            config.Config.FIRETRAP_DAMAGE,
                                            config.Config.FIRETRAP_PRICE)

    def getClass(self):
        return "FireTrapBuyer"

    def newCopy(self):
        return FireTrapBuyer(self._position)

class IceTrap(Trap):
    def __init__(self, position):
        super(IceTrap, self).__init__(position,
                                       config.Config.ICETRAP_WIDTH,
                                       config.Config.ICETRAP_HEIGHT,
                                       config.Config.ICETRAP_IMAGE,
                                       config.Config.ICETRAP_DAMAGE,
                                       config.Config.ICETRAP_PRICE)

    def getClass(self):
        return "IceTrap"

    def newCopy(self):
        return IceTrap(self._position)

    def shot(self, enemie):
        iceEffect = effects.IceEffect(enemie)
        enemie.setIce(iceEffect)


class IceTrapBuyer(Trap):
    def __init__(self, position):
        super(IceTrapBuyer, self).__init__(position,
                                           config.Config.ICETRAP_WIDTH,
                                           config.Config.ICETRAP_HEIGHT,
                                           config.Config.ICETRAP_IMAGE,
                                           config.Config.ICETRAP_DAMAGE,
                                           config.Config.ICETRAP_PRICE)

    def getClass(self):
        return "IceTrapBuyer"

    def newCopy(self):
        return IceTrapBuyer(self._position)
