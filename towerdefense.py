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

    def spawnEnemie(self):
        self.addEnemie(enemies.Enemie(config.Config.ENEMIE_SPAWNPOSITION,
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
        self._matrix = [[0 for aux in range(config.Config.MAP_DIMX)] for aux2 in range(config.Config.MAP_DIMY)]
        for i in range(config.Config.MAP_DIMX):
            for j in range(config.Config.MAP_DIMY):
                self._matrix[i][j] = 0
        self._matrix[9][0] = 1
        self._matrix[10][0] = 2
        self._matrix[11][0] = 1
        self._matrix[9][1] = 1
        self._matrix[10][1] = 4
        self._matrix[11][1] = 1
        self._matrix[9][2] = 1
        self._matrix[10][2] = 4
        self._matrix[11][2] = 1
        self._matrix[9][3] = 1
        self._matrix[10][3] = 4
        self._matrix[11][3] = 1
        self._matrix[9][4] = 1
        self._matrix[10][4] = 4
        self._matrix[11][4] = 1
        self._matrix[9][5] = 1
        self._matrix[9][6] = 1
        self._matrix[10][5] = 5
        self._matrix[10][6] = 1
        self._matrix[11][5] = 4
        self._matrix[11][6] = 1
        self._matrix[12][5] = 4
        self._matrix[12][6] = 1
        self._matrix[13][5] = 4
        self._matrix[13][6] = 1
        self._matrix[12][4] = 1
        self._matrix[13][4] = 1
        self._matrix[12][5] = 4
        self._matrix[13][5] = 4
        self._matrix[14][4] = 1
        self._matrix[14][5] = 4
        self._matrix[14][6] = 1
        self._matrix[15][4] = 1
        self._matrix[15][5] = 4
        self._matrix[15][6] = 1
        self._matrix[16][4] = 1
        self._matrix[16][5] = 4
        self._matrix[16][6] = 1
        self._matrix[17][4] = 1
        self._matrix[17][5] = 5
        self._matrix[18][4] = 1
        self._matrix[18][5] = 1
        self._matrix[18][6] = 1
        self._matrix[17][6] = 4
        self._matrix[18][7] = 1
        self._matrix[17][7] = 4
        self._matrix[18][8] = 1
        self._matrix[17][8] = 4
        self._matrix[18][9] = 1
        self._matrix[17][9] = 4
        self._matrix[18][10] = 1
        self._matrix[17][10] = 4
        self._matrix[18][11] = 1
        self._matrix[17][11] = 4
        self._matrix[18][12] = 1
        self._matrix[17][12] = 4
        self._matrix[18][13] = 1
        self._matrix[17][13] = 4
        self._matrix[18][14] = 1
        self._matrix[17][14] = 4
        self._matrix[18][15] = 1
        self._matrix[17][15] = 4
        self._matrix[18][16] = 1
        self._matrix[17][16] = 4
        self._matrix[18][17] = 1
        self._matrix[17][17] = 5
        self._matrix[18][18] = 1
        self._matrix[17][18] = 1
        self._matrix[16][17] = 4
        self._matrix[16][18] = 1
        self._matrix[15][17] = 4
        self._matrix[15][18] = 1
        self._matrix[14][17] = 4
        self._matrix[14][18] = 1
        self._matrix[13][17] = 4
        self._matrix[13][18] = 1
        self._matrix[12][17] = 5
        self._matrix[12][18] = 4
        self._matrix[13][19] = 1
        self._matrix[12][19] = 4
        self._matrix[13][20] = 1
        self._matrix[12][20] = 4
        self._matrix[13][21] = 1
        self._matrix[12][21] = 4
        self._matrix[13][22] = 1
        self._matrix[12][22] = 4
        self._matrix[13][23] = 1
        self._matrix[12][23] = 4
        self._matrix[13][24] = 1
        self._matrix[12][24] = 4
        self._matrix[13][25] = 1
        self._matrix[12][25] = 4
        self._matrix[13][26] = 1
        self._matrix[12][26] = 4
        self._matrix[13][27] = 1
        self._matrix[12][27] = 4
        self._matrix[13][28] = 1
        self._matrix[12][28] = 4
        self._matrix[13][29] = 1
        self._matrix[12][29] = 3
        self._matrix[16][7] = 1
        self._matrix[16][8] = 1
        self._matrix[16][9] = 1
        self._matrix[16][10] = 1
        self._matrix[16][11] = 1
        self._matrix[16][12] = 1
        self._matrix[16][13] = 1
        self._matrix[16][14] = 1
        self._matrix[16][15] = 1
        self._matrix[16][16] = 1
        self._matrix[15][16] = 1
        self._matrix[14][16] = 1
        self._matrix[13][16] = 1
        self._matrix[12][16] = 1
        self._matrix[11][16] = 1
        self._matrix[11][17] = 1
        self._matrix[11][18] = 1
        self._matrix[11][19] = 1
        self._matrix[11][20] = 1
        self._matrix[11][21] = 1
        self._matrix[11][22] = 1
        self._matrix[11][23] = 1
        self._matrix[11][24] = 1
        self._matrix[11][25] = 1
        self._matrix[11][26] = 1
        self._matrix[11][27] = 1
        self._matrix[11][28] = 1
        self._matrix[11][29] = 1









