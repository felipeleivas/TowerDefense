# coding=utf-8
import config
import rectangle
import pygame
import abc
import shot


# Classe Tower estende de Rectangle:
# Essa classe define as Torres do jogo, tanto as que serão postas no mapa,
# como as que ficam na aba de compras.
class Tower(rectangle.Rectangle, metaclass=abc.ABCMeta):
    _mouseCircleSurface = pygame.Surface(config.Config.MOUSE_CIRCLE_SURFACE)

    def __init__(self, position, width, height, image, range, damage, fireRate, price):
        super(Tower, self).__init__(position, width, height, image)
        self._range = range
        self._damage = damage
        self._fireRate = fireRate
        self._reloadTime = 1 / fireRate
        self._price = price
        self._shotList = []

    def getFirstClass(self):
        return "Tower"

    @abc.abstractmethod
    def getClass(self):
        return

    @abc.abstractmethod
    def newCopy(self):
        return

    def getRange(self):
        return self._range

    def setRange(self, range):
        self._range = range

    def getDamage(self):
        return self._damage

    def setDamage(self, damage):
        self._damage = damage

    def getFireRate(self):
        return self._fireRate

    def setFireRate(self, fireRate):
        self._fireRate = fireRate

    def getPrice(self):
        return self._price

    def setPrice(self, price):
        self._price = price

    def getShotList(self):
        return self._shotList

    def doublePrice(self):
        self._price *= 2

    def decReloadTime(self):
        self._reloadTime -= 1.0

    def resetReloadTime(self):
        self._reloadTime = 1.0 / self._fireRate
        #print self._reloadTime

    def shotEnemies(self, enemies):
        if self._reloadTime <= 0:
            for enemieAux in enemies:
                if self.isInsideRange(enemieAux.getPosition()):
                    self.shot(enemieAux)
                    self.resetReloadTime()
                    break

    def shot(self, enemie):
        self._shotList.append(shot.Shot(self.getPosition(), 8, 8, "imagens/shot.png", 0.5, enemie.getPosition(), 10))

    def moveShots(self, gameDisplay, enemieList, towerDefense):
        for shotAux in self._shotList:
            shotAux.move()
            for enemieAux in enemieList:
                if enemieAux.collide(shotAux):
                    enemieAux.hit(shotAux.getDamage(), towerDefense)
                    shotAux.destroy(self)
        self.paintShots(gameDisplay)

    def delShot(self, shot):
        try:
            self._shotList.remove(shot) #Dar uma olhada aqui
        except:
            pass

    def paintShots(self, gameDisplay):
        for shotAux in self._shotList:
            shotAux.paint(gameDisplay)

    def isInsideRange(self, position):
        center = self.getCenter()
        if center[0] - self._range <= position[0] < center[0] + self._range:
            if center[1] - self._range <= position[1] < center[1] + self._range:
                return True
        return False

    def paintRange(self, gameDisplay, color):
        self._mouseCircleSurface.fill(config.Config.CK)
        self._mouseCircleSurface.set_colorkey(config.Config.CK)
        pygame.draw.circle(self._mouseCircleSurface, color, self.getCenter(), self._range, self._range)
        self._mouseCircleSurface.set_alpha(150)
        gameDisplay.blit(self._mouseCircleSurface, (0, 0))

    def paintAtributes(self, gameDisplay):
        font = pygame.font.SysFont(None, 25, True, False)
        text = font.render("Damage:%d" % self._damage, True, (0, 0, 0))
        gameDisplay.blit(text, (497, 177))
        text = font.render("Range:%d" % self._range, True, (0, 0, 0))
        gameDisplay.blit(text, (497, 197))
        text = font.render("Fire Rate:%.2f" % self._fireRate, True, (0, 0, 0))
        gameDisplay.blit(text, (497, 217))


class ClassicTower(Tower):
    def __init__(self, position):
        super(ClassicTower, self).__init__(position,
                                           config.Config.CLASSICTOWER_WIDTH,
                                           config.Config.CLASSICTOWER_HEIGHT,
                                           config.Config.CLASSICTOWER_IMAGE_small,
                                           config.Config.CLASSICTOWER_RANGE,
                                           config.Config.CLASSICTOWER_DAMAGE,
                                           config.Config.CLASSICTOWER_FIRERATE,
                                           config.Config.CLASSICTOWER_PRICE)

    def getClass(self):
        return "ClassicTower"

    def newCopy(self):
        return ClassicTower(self._position)



class ClassicTowerBuyer(Tower):
    def __init__(self, position):
        super(ClassicTowerBuyer, self).__init__(position,
                                                config.Config.CLASSICTOWER_WIDTH * 2,
                                                config.Config.CLASSICTOWER_HEIGHT * 2,
                                                config.Config.CLASSICTOWER_IMAGE_big,
                                                config.Config.CLASSICTOWER_RANGE,
                                                config.Config.CLASSICTOWER_DAMAGE,
                                                config.Config.CLASSICTOWER_FIRERATE,
                                                config.Config.CLASSICTOWER_PRICE)

    def getClass(self):
        return "ClassicTowerBuyer"

    def newCopy(self):
        return ClassicTowerBuyer(self._position)


class BlueTower(Tower):
    def __init__(self, position):
        super(BlueTower, self).__init__(position,
                                        config.Config.BLUETOWER_WIDTH,
                                        config.Config.BLUETOWER_HEIGHT,
                                        config.Config.BLUETOWER_IMAGE_small,
                                        config.Config.BLUETOWER_RANGE,
                                        config.Config.BLUETOWER_DAMAGE,
                                        config.Config.BLUETOWER_FIRERATE,
                                        config.Config.BLUETOWER_PRICE)

    def getClass(self):
        return "BlueTower"

    def newCopy(self):
        return BlueTower(self._position)


class BlueTowerBuyer(Tower):
    def __init__(self, position):
        super(BlueTowerBuyer, self).__init__(position,
                                             config.Config.BLUETOWER_WIDTH * 2,
                                             config.Config.BLUETOWER_HEIGHT * 2,
                                             config.Config.BLUETOWER_IMAGE_big,
                                             config.Config.BLUETOWER_RANGE,
                                             config.Config.BLUETOWER_DAMAGE,
                                             config.Config.BLUETOWER_FIRERATE,
                                             config.Config.BLUETOWER_PRICE)

    def getClass(self):
        return "BlueTowerBuyer"

    def newCopy(self):
        return BlueTowerBuyer(self._position)
