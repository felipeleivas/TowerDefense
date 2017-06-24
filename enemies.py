import rectangle
import config


class Enemie(rectangle.Rectangle):
    def __init__(self, position, width, height, image, health, speed, earnCash, lifesWillTook, firstDir):
        super(Enemie, self).__init__(position, width, height, image)
        self._health = health
        self._speed = speed
        self._originalSpeed = speed
        self._earnCash = earnCash
        self._lifesWillTook = lifesWillTook
        self._specialEffects = []
        self._upFlag = False
        self._downFlag = False
        self._rightFlag = False
        self._leftFlag = False
        self._setInitialFlags(firstDir)

    def getHealth(self):
        return self._health

    def setHealth(self, health):
        self._health = health

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def refreshSpeed(self):
        self._speed = self._originalSpeed

    def getEarnCash(self):
        return self._earnCash

    def setEarnCash(self, earnCash):
        self._earnCash = earnCash

    def getLifesWillTook(self):
        return self._lifesWillTook

    def setLifesWillTook(self, lifesWillTook):
        self._lifesWillTook = lifesWillTook

    def hit(self, damage, towerDefense):
        if damage >= self._health:
            self.despawn(towerDefense)
        else:
            self._health = self._health - damage

    def slow(self, slow):
        self._speed -= slow

    def setBurn(self, burnEffect):
        if not self.isBurned():
            self._specialEffects.append(burnEffect)

    def isBurned(self):
        for effectAux in self._specialEffects:
            if effectAux.getName() == "Burn":
                return True
        return False

    def setIce(self, iceEffect):
        if not self.isIced():
            self._specialEffects.append(iceEffect)
            self.slow(iceEffect.getSlow())

    def isIced(self):
        for effectAux in self._specialEffects:
            if effectAux.getName() == "Ice":
                return True
        return False

    def delEffect(self, effect):
        if effect.getName() == "Ice":
            self.refreshSpeed()
        self._specialEffects.remove(effect)

    def executeEffects(self, towerDefense):
        for effectAux in self._specialEffects:
            if effectAux.getName() == "Burn":
                self.hit(effectAux.getDamagePerSecond(), towerDefense)
            effectAux.decDuration()

    def despawn(self, towerDefense):
        towerDefense.delEnemie(self)

    def insideRectPosition(self, rectMap):
        for i in range(0, rectMap.getDimension()[0]):
            for j in range(0, rectMap.getDimension()[1]):
                if rectMap.getMap()[i][j][1].isInside(self.getCenter()):
                    return i, j

    def _setInitialFlags(self, firstDir):
        if firstDir[0] == "U":
            self._upFlag = True
        elif firstDir[0] == "D":
            self._downFlag = True
        elif firstDir[0] == "R":
            self._rightFlag = True
        elif firstDir[0] == "L":
            self._leftFlag = True

    def _setFlags(self, up, down, left, right):
        self._upFlag = up
        self._downFlag = down
        self._leftFlag = left
        self._rightFlag = right

    # Logica pros bichinhos andarem em qualquer mapa criado desde que ele
    # nao volte pra esquerda nenhuma vez. Ainda vou acabar a ultima parte
    # pro mapa poder voltar ( mapas em espiral )
    def move(self, mapMatrix, rectMap, towerDefense):

        rectPosition = self.insideRectPosition(rectMap)
        rectPositionI = rectPosition[0]
        rectPositionJ = rectPosition[1]
        mapMatrixNextColumn = mapMatrix[rectPositionI][rectPositionJ + 1]
        mapMatrixPrevColumn = mapMatrix[rectPositionI][rectPositionJ - 1]
        mapMatrixNextRow = mapMatrix[rectPositionI + 1][rectPositionJ]
        mapMatrixPrevRow = mapMatrix[rectPositionI - 1][rectPositionJ]
        mapMatrixPosition = mapMatrix[rectPositionI][rectPositionJ]

        if mapMatrixPosition == config.Config.MAP_NUMBMATRIX_DESPAWN:
            self.despawn(towerDefense)
        else:
            if self._rightFlag:
                self.executeRightFlag(mapMatrixNextColumn, mapMatrixPosition, mapMatrixPrevRow, mapMatrixNextRow)

            elif self._leftFlag:
                self.executeLeftFlag(mapMatrixPrevColumn, mapMatrixPosition, mapMatrixPrevRow, mapMatrixNextRow)

            elif self._downFlag:
                self.executeDownFlag(mapMatrixPrevColumn, mapMatrixPosition, mapMatrixNextColumn, mapMatrixNextRow)

            elif self._upFlag:
                self.executeUpFlag(mapMatrixPrevColumn, mapMatrixPosition, mapMatrixNextColumn, mapMatrixPrevRow)

    def executeRightFlag(self, mapMatrixNextColumn, mapMatrixPosition, mapMatrixPrevRow, mapMatrixNextRow):
        if self.isContinueMoving(mapMatrixNextColumn, mapMatrixNextColumn, mapMatrixNextColumn):
            self.moveRight()
        elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
            if mapMatrixPrevRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(True, False, False, False)
            elif mapMatrixNextRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(False, True, False, False)

    def executeLeftFlag(self, mapMatrixPrevColumn, mapMatrixPosition, mapMatrixPrevRow, mapMatrixNextRow):
        if self.isContinueMoving(mapMatrixPrevColumn, mapMatrixPrevColumn, mapMatrixPrevColumn):
            self.moveLeft()
        elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
            if mapMatrixPrevRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(True, False, False, False)
            elif mapMatrixNextRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(False, True, False, False)

    def executeDownFlag(self, mapMatrixPrevColumn, mapMatrixPosition, mapMatrixNextColumn, mapMatrixNextRow):
        if self.isContinueMoving(mapMatrixNextRow, mapMatrixNextRow, mapMatrixNextRow):
            self.moveDown()
        elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
            if mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(False, False, False, True)
            elif mapMatrixPrevColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(False, False, True, False)

    def executeUpFlag(self, mapMatrixPrevColumn, mapMatrixPosition, mapMatrixNextColumn, mapMatrixPrevRow):
        if self.isContinueMoving(mapMatrixPrevRow, mapMatrixPrevRow, mapMatrixPrevColumn):
            self.moveUp()
        elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
            if mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(False, False, False, True)
            elif mapMatrixPrevColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                self._setFlags(False, False, True, False)

    def isContinueMoving(self, firstCondition, secondCondition, thirdCondition):
        return firstCondition == config.Config.MAP_NUMBMATRIX_CENTRALPATH \
               or secondCondition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION \
               or thirdCondition == config.Config.MAP_NUMBMATRIX_DESPAWN

    def moveRight(self):
        positionX = self._position[0]
        positionY = self._position[1]
        positionX += self._speed
        self.setPosition((positionX, positionY))

    def moveLeft(self):
        positionX = self._position[0]
        positionY = self._position[1]
        positionX -= self._speed
        self.setPosition((positionX, positionY))

    def moveDown(self):
        positionX = self._position[0]
        positionY = self._position[1]
        positionY += self._speed
        self.setPosition((positionX, positionY))

    def moveUp(self):
        positionX = self._position[0]
        positionY = self._position[1]
        positionY -= self._speed
        self.setPosition((positionX, positionY))
