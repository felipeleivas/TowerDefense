import rectangle
import config


class Enemie(rectangle.Rectangle):
    def __init__(self, position, width, height, image, health, speed, earnCash, lifesWillTook):
        super(Enemie, self).__init__(position, width, height, image)
        self._health = health
        self._speed = speed
        self._earnCash = earnCash
        self._lifesWillTook = lifesWillTook
        self._flagSubir = False
        self._flagDescer = False
        self._flagDireita = True
        self._flagEsquerda = False

    def getHealth(self):
        return self._health

    def setHealth(self, health):
        self._health = health

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

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

    def despawn(self, towerDefense):
        towerDefense.delEnemie(self)

    def insideRectPosition(self, rectMap):
        for i in range(0, rectMap.getDimension()[0]):
            for j in range(0, rectMap.getDimension()[1]):
                if rectMap.getMap()[i][j][1].isInside(self.getCenter()):
                    return i, j

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

        if mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_DESPAWN:
            self.despawn(towerDefense)
        else:
            if self._flagDireita:
                if mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH \
                        or mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    self.moveRigth()
                elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    if mapMatrixPrevRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                        self._flagSubir = True
                        self._flagDescer = False
                        self._flagDireita = False
                        self._flagEsquerda = False
                    elif mapMatrixNextRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                        self._flagDescer = True
                        self._flagSubir = False
                        self._flagDireita = False
                        self._flagEsquerda = False
            elif self._flagDescer:
                if mapMatrixNextRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH \
                        or mapMatrixNextRow == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    self.moveDown()
                elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    if mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                        self._flagEsquerda = False
                        self._flagDireita = True
                        self._flagDescer = False
                        self._flagSubir = False
                    elif mapMatrixPrevColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                        self._flagEsquerda = True
                        self._flagDireita = False
                        self._flagDescer = False
                        self._flagSubir = False
            elif self._flagSubir:
                if mapMatrixPrevRow == config.Config.MAP_NUMBMATRIX_CENTRALPATH \
                        or mapMatrixPrevRow == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    self.moveUp()
                elif mapMatrixPosition == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    if mapMatrixNextColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                        self._flagEsquerda = False
                        self._flagDireita = True
                        self._flagDescer = False
                        self._flagSubir = False
                    elif mapMatrixPrevColumn == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                        self._flagEsquerda = True
                        self._flagDireita = False
                        self._flagDescer = False
                        self._flagSubir = False

    def moveRigth(self):
        positionX = self._position[0]
        positionY = self._position[1]
        positionX += self._speed
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
