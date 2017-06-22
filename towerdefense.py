# coding=utf-8
import pygame

import config
import map
import towers
import traps
import enemies


# Classe TowerDefense:
# A classe principal. É aqui que todas as interações do jogador com
# a partida são realizadas. Por exemplo eventos de estar comprando uma torre,
# estar dando upgrade, estar parado, controle de inimigos, controle das torres,
# printar na tela esses devidos objetos, etc...
class TowerDefense:
    I, J = 0, 0
    selectedObject = 0

    def __init__(self, player):
        self._towerList = []
        self._enemiesList = []
        self._trapList = []
        self._purchasingTower = False
        self._purchasingTrap = False
        self._clickedInTowerOrTrap = False
        self._matrix = 0
        self.inicializeMatrix()
        self._rectMap = map.Map(config.Config.MAP_DIMS, config.Config.RECT_DIMS_px, self._matrix)
        self._towerMenuBackground = pygame.image.load(config.Config.MENUTOWERS_IMAGE)
        self._buyingTowers = [towers.ClassicTowerBuyer(config.Config.CLASSICTOWER_BUYER_POS),
                              towers.BlueTowerBuyer(config.Config.BLUETOWER_BUYER_POS)]
        self._buyingTraps = [traps.FireTrapBuyer(config.Config.FIRETRAP_BUYER_POS),
                             traps.IceTrapBuyer(config.Config.ICETRAP_BUYER_POS)]
        self._FPS = False
        self._shift = False
        self._cash = config.Config.PLAYER_CASH
        self._player = player
        self._timer = 0
        self._enemieTimer = 1

    def addTower(self, newTower):
        self._towerList.append(newTower)

    def getTowers(self):
        return self._towerList
    
    def addTrap(self, newTrap):
        self._trapList.append(newTrap)
        
    def getTraps(self):
        return self._trapList

    def addEnemie(self, newEnemie):
        self._enemiesList.append(newEnemie)

    def squarePosToPixel(self, pos):
        return (config.Config.RECT_DIMX_px * pos[1], config.Config.RECT_DIMY_px * pos[0]) #TODO: @Vinicius, Can you understand why reversed 0 and 1 ?

    def getEnemySpawnPosition(self):
        try:
            for i in range(len(self._matrix)):
                for j in range(len(self._matrix[0])):
                    if self._matrix[i][j] == config.Config.MAP_NUMBMATRIX_SPAWN:
                        return (self.squarePosToPixel([i,j]))
        except IndexError:
            print("Failed to acess matrix line")
            raise

    def spawnEnemie(self):
        self.addEnemie(enemies.Enemie(self.getEnemySpawnPosition(),
                                      config.Config.ENEMIE_WIDTH,
                                      config.Config.ENEMIE_HEIGHT,
                                      config.Config.ENEMIE_IMAGE,
                                      config.Config.ENEMIE_HEALTH,
                                      config.Config.ENEMIE_SPEED,
                                      config.Config.ENEMIE_EARNCASH,
                                      config.Config.ENEMIE_LIFESWILLTOOK))
        self._enemieTimer = 1

    def delEnemie(self, enemie):
        self._enemiesList.remove(enemie)

    def getEnemies(self):
        return self._enemiesList

    def turnOnPurchasingTower(self):
        self._purchasingTower = True

    def turnOffPurchasingTower(self):
        self._purchasingTower = False

    def isPurchasingTower(self):
        return self._purchasingTower

    def turnOnPurchasingTrap(self):
        self._purchasingTrap = True

    def turnOffPurchasingTrap(self):
        self._purchasingTrap = False

    def isPurchasingTrap(self):
        return self._purchasingTrap

    def turnOnClickedInTowerOrTrap(self):
        self._clickedInTowerOrTrap = True

    def turnOffClickedInTowerOrTrap(self):
        self._clickedInTowerOrTrap = False

    def isClickedInTowerOrTrap(self):
        return self._clickedInTowerOrTrap

    def executePurchasingTower(self, gameDisplay, mousePosition):
        for i in range(0, self.getRectMap().getDimension()[0]):
            for j in range(0, self.getRectMap().getDimension()[1]):
                currentMapRect = self.getRectMap().getMap()[i][j][1]
                if currentMapRect.isInside(mousePosition):
                    self.selectedObject.setPosition(currentMapRect.getPosition())
                    self.selectedObject.paint(gameDisplay)
                    collide = False
                    for towerAux in self.getTowers():
                        if towerAux.collide(self.selectedObject):
                            collide = True
                    if not collide:
                        if self.isInsidePath(self.selectedObject):
                            collide = True
                    if collide:
                        self.selectedObject.paintRange(gameDisplay, config.Config.COLLIDE_COLOR)
                    else:
                        self.selectedObject.paintRange(gameDisplay, config.Config.NOT_COLLIDE_COLOR)

    def executePurchasingTrap(self, gameDisplay, mousePosition):
        for i in range(0, self.getRectMap().getDimension()[0]):
            for j in range(0, self.getRectMap().getDimension()[1]):
                currentMapRect = self.getRectMap().getMap()[i][j][1]
                if currentMapRect.isInside(mousePosition):
                    self.selectedObject.setPosition(currentMapRect.getPosition())
                    self.selectedObject.paint(gameDisplay)
                    collide = False
                    if not collide:
                        for trapAux in self.getTraps():
                            if trapAux.collide(self.selectedObject):
                                collide = True
                    if not collide:
                        if not self.isInsideCentralPath(self.selectedObject):
                            collide = True
                    if collide:
                        self.selectedObject.paintRange(gameDisplay, config.Config.COLLIDE_COLOR)
                    else:
                        self.selectedObject.paintRange(gameDisplay, config.Config.NOT_COLLIDE_COLOR)

    def executeClickedInTowerOrTrap(self, gameDisplay):
        self.selectedObject.paintRange(gameDisplay, config.Config.GREEN)
        self.selectedObject.paintAtributes(gameDisplay)

    def getRectMap(self):
        return self._rectMap

    def mousePress(self, mousePosition, gameDisplay):

        if self.isPurchasingTower():
            if self.isInsideRect(mousePosition): #EFEITO COLATERAL - arrumar
                newTower = self.selectedObject
                newTower.setPosition(self.getRectMap().getMap()[self.I][self.J][1].getPosition())
                newTowerColliding = False
                for towerAux in self.getTowers():
                    if towerAux.collide(newTower):
                        newTowerColliding = True
                if not newTowerColliding:
                    newTowerColliding = self.isInsidePath(newTower)
                if not newTowerColliding:
                    if self._player.haveCashToBuy(newTower.getPrice()):
                        self.addTower(newTower)
                        self._player.purchaseObject(newTower.getPrice())
                        if self.isShiftOn():
                            self.selectedObject = self.selectedObject.newCopy()
                        else:
                            self.turnOffPurchasingTower()
                    else:
                        self.turnOffPurchasingTower()
                        self.paintHaveNoCashMess(gameDisplay, mousePosition)
                        self._timer = 3
        elif self.isPurchasingTrap():
            if self.isInsideRect(mousePosition):
                newTrap = self.selectedObject
                newTrap.setPosition(self.getRectMap().getMap()[self.I][self.J][1].getPosition())
                newTrapColliding = False
                for trapAux in self.getTraps():
                    if trapAux.collide(newTrap):
                        newTrapColliding = True
                if not newTrapColliding:
                    if self.isInsideCentralPath(newTrap):
                        newTrapColliding = False
                    else:
                        newTrapColliding = True
                if not newTrapColliding:
                    if self._player.haveCashToBuy(newTrap.getPrice()):
                        self.addTrap(newTrap)
                        self._player.purchaseObject(newTrap.getPrice())
                        if self.isShiftOn():
                            self.selectedObject = self.selectedObject.newCopy()
                        else:
                            self.turnOffPurchasingTrap()
                    else:
                        self.turnOffPurchasingTrap()
                        self.paintHaveNoCashMess(gameDisplay, mousePosition)
                        self._timer = 3
        elif self.isInsideTowerOrTrap(mousePosition):
            self.turnOnClickedInTowerOrTrap()
        elif self.isClickedInTowerOrTrap():
            self.turnOffClickedInTowerOrTrap()
        elif self.isInsideBuying(mousePosition): #EFEITO COLATERAL - arrumar
            if self.selectedObject.getFirstClass() == "Tower":
                self.turnOnPurchasingTower()
            elif self.selectedObject.getFirstClass() == "Trap":
                self.turnOnPurchasingTrap()

    def isInsideRect(self, mousePosition):
        for i in range(0, self.getRectMap().getDimension()[0]):
            for j in range(0, self.getRectMap().getDimension()[1]):
                if self.getRectMap().getMap()[i][j][1].isInside(mousePosition):
                    self.I = i
                    self.J = j
                    return True
        return False

    def isInsideTowerOrTrap(self, mousePosition):
        return self.isInsideTower(mousePosition) or self.isInsideTrap(mousePosition)

    def isInsideTower(self, mousePosition):
        if mousePosition[0] > 480:
            return False
        else:
            for towerAux in self.getTowers():
                if towerAux.isInside(mousePosition):
                    self.selectedObject = towerAux
                    return True
        return False

    def isInsideTrap(self, mousePosition):
        if mousePosition[0] > 480:
            return False
        else:
            for trapAux in self.getTraps():
                if trapAux.isInside(mousePosition):
                    self.selectedObject = trapAux
                    return True
        return False

    def isInsideBuying(self, mousePosition):
        if mousePosition[0] < 480:
            return False
        else:
            for i in range(0, 2):
                if self._buyingTowers[i].isInside(mousePosition):
                    towerClass = self._buyingTowers[i].getClass()
                    if towerClass == "ClassicTowerBuyer":
                        self.selectedObject = towers.ClassicTower((0, 0))
                    elif towerClass == "BlueTowerBuyer":
                        self.selectedObject = towers.BlueTower((0, 0))
                    return True
            for i in range(0, 2):
                if self._buyingTraps[i].isInside(mousePosition):
                    trapClass = self._buyingTraps[i].getClass()
                    if trapClass == "FireTrapBuyer":
                        self.selectedObject = traps.FireTrap((0, 0))
                    elif trapClass == "IceTrapBuyer":
                        self.selectedObject = traps.IceTrap((0, 0))
                    return True
        return False

    def isInsidePath(self, object):
        rectMap = self.getRectMap().getMap()
        for i in range(0, self.getRectMap().getDimension()[0]):
            for j in range(0, self.getRectMap().getDimension()[1]):
                if rectMap[i][j][0] != 0:
                    if rectMap[i][j][1].collide(object):
                        return True
        return False

    def isInsideCentralPath(self, object):
        rectMap = self.getRectMap().getMap()
        for i in range(0, self.getRectMap().getDimension()[0]):
            for j in range(0, self.getRectMap().getDimension()[1]):
                rectID = rectMap[i][j][0]
                if rectID == config.Config.MAP_NUMBMATRIX_CENTRALPATH\
                        or rectID == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    if rectMap[i][j][1].collide(object):
                        return True
        return False

    def paintAllStuff(self, gameDisplay, mousePosition):
        self.paintRectMap(gameDisplay)
        self.paintTowers(gameDisplay)
        self.paintTraps(gameDisplay)
        if self.isPurchasingTower():
            self.executePurchasingTower(gameDisplay, mousePosition)
        elif self.isPurchasingTrap():
            self.executePurchasingTrap(gameDisplay, mousePosition)
        self.paintTowerMenuBackground(gameDisplay)
        if self.isClickedInTowerOrTrap():
            self.executeClickedInTowerOrTrap(gameDisplay)
        self.paintBuyingTowers(gameDisplay)
        self.paintBuyingTraps(gameDisplay)
        self.paintCash(gameDisplay)
        self.paintLife(gameDisplay)
        self.paintName(gameDisplay)
        if self.getTimer() > 0:
            self.paintHaveNoCashMess(gameDisplay, mousePosition)
        if self._enemieTimer == 0:
            self.spawnEnemie()
        self.paintShots(gameDisplay)
        self.paintEnemies(gameDisplay)


    def paintTowers(self, gameDisplay):
        for towerAux in self.getTowers():
            towerAux.paint(gameDisplay)

    def paintTraps(self, gameDisplay):
        for trapAux in self.getTraps():
            trapAux.paint(gameDisplay)

    def paintEnemies(self, gameDisplay):
        for enemiesAux in self.getEnemies():
            enemiesAux.move(self._matrix, self._rectMap, self)
            enemiesAux.paint(gameDisplay)

    def paintShots(self, gameDisplay):
        for towerAux in self.getTowers():
            towerAux.shotEnemies(self.getEnemies())
            towerAux.moveShots(gameDisplay, self.getEnemies(), self)
        for trapAux in self.getTraps():
            trapAux.shotEnemies(self.getEnemies(), self)


    def paintRectMap(self, gameDisplay):
        for i in range(0, self.getRectMap().getDimension()[0]):
            for j in range(0, self.getRectMap().getDimension()[1]):
                self.getRectMap().getMap()[i][j][1].paint(gameDisplay)

    def paintTowerMenuBackground(self, gameDisplay):
        gameDisplay.blit(self._towerMenuBackground, (480, 0))

    def paintBuyingTowers(self, gameDisplay):
        for buyingTower in self._buyingTowers:
            buyingTower.paint(gameDisplay)

    def paintBuyingTraps(self, gameDisplay):
        for buyingTrap in self._buyingTraps:
            buyingTrap.paint(gameDisplay)

    def paintCash(self, gameDisplay):
        font = pygame.font.SysFont(None, 25)
        text = font.render("CASH: %d" % self._player.getCash(), True, (0, 0, 0))
        gameDisplay.blit(text, (495, 425))

    def paintHaveNoCashMess(self, gameDisplay, mousePosition):
        font = pygame.font.SysFont(None, 30, True, False)
        text = font.render("Not enougth cash!", True, (255, 255, 0))
        gameDisplay.blit(text, mousePosition)

    def paintLife(self, gameDisplay):
        font = pygame.font.SysFont(None, 25)
        text = font.render("LIFE: %d" % self._player.getLife(), True, (0, 0, 0))
        gameDisplay.blit(text, (585, 425))

    def paintName(self, gameDisplay):
        font = pygame.font.SysFont(None, 30)
        text = font.render("%s" % self._player.getName(), True, (0, 0, 0))
        gameDisplay.blit(text, (495, 402))

    def turnOnShift(self):
        self._shift = True

    def turnOffShift(self):
        self._shift = False

    def isShiftOn(self):
        return self._shift

    def decTimer(self):
        self._timer -= 1
        self._enemieTimer -= 1
        for towerAux in self.getTowers():
            towerAux.decReloadTime()

        for trapAux in self.getTraps():
            trapAux.decReloadTime()

    #def decTimerDecisegundo(self):
     #   for towerAux in self.getTowers():
      #      towerAux.decReloadTime()

    def getTimer(self):
        return self._timer

    def inicializeMatrix(self):
        f = open("maps/map3.map")

        self._matrix = []
        for line in f.readlines():
            self._matrix.append([int(x) for x in line.strip('[]\n').split(',')])