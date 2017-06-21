# coding=utf-8
import rectangle
import config

# Classe Map:
# Define o mapa do jogo (os quadradinhos verdes).
# Varia em função do número de quadradinhos na altura e largura,
# e da altura e da larguda dos quadradinhos em pixels.
class Map:
    def __init__(self, mapDimension, rectDimensionPx, matrix, mode=None):
        self._dimension = mapDimension
        self._rectWidth = rectDimensionPx[0]
        self._rectHeight = rectDimensionPx[1]
        self._map = [[0 for aux in range(self._dimension[0])] for aux2 in range(self._dimension[1])]
        self.inicializeMap(matrix, mode)

    def getDimension(self):
        return self._dimension

    def setDimension(self, dimension):
        self._dimension = dimension

    def getRectWidth(self):
        return self._rectWidth

    def getRectHeight(self):
        return self._rectHeight

    def getMap(self):
        return self._map

    def inicializeMap(self, matrix, mode=None):
        if mode == 'creation':
            grassImg = config.Config.GRASS_IMAGE
            regPathImg = config.Config.REGULAR_PATH_IMAGE
            spawnImg = config.Config.SPAWN_IMAGE
            desPawnImg = config.Config.DESPAWN_IMAGE
            centralPathImg = config.Config.CENTRAL_PATH_IMAGE
            changeDirImg = config.Config.CHANGEDIR_IMAGE
        else:
            grassImg = config.Config.GRASS_IMAGE
            regPathImg = config.Config.REGULAR_PATH_IMAGE
            spawnImg = config.Config.REGULAR_PATH_IMAGE
            desPawnImg = config.Config.REGULAR_PATH_IMAGE
            centralPathImg = config.Config.REGULAR_PATH_IMAGE
            changeDirImg = config.Config.REGULAR_PATH_IMAGE

        x, y = 0, 0
        for i in range(0, self._dimension[0]):
            x = 0
            for j in range(0, self._dimension[1]):
                if matrix[i][j] == config.Config.MAP_NUMBMATRIX_GRASS:
                    self._map[i][j] = (0, rectangle.Rectangle((x, y), self.getRectWidth(), self.getRectHeight(), grassImg))

                elif matrix[i][j] == config.Config.MAP_NUMBMATRIX_PATH:
                    self._map[i][j] = (1, rectangle.Rectangle((x, y), self.getRectWidth(), self.getRectHeight(), regPathImg))

                elif matrix[i][j] == config.Config.MAP_NUMBMATRIX_SPAWN:
                    self._map[i][j] = (2, rectangle.Rectangle((x, y), self.getRectWidth(), self.getRectHeight(), spawnImg))

                elif matrix[i][j] == config.Config.MAP_NUMBMATRIX_DESPAWN:
                    self._map[i][j] = (3, rectangle.Rectangle((x, y), self.getRectWidth(), self.getRectHeight(), desPawnImg))

                elif matrix[i][j] == config.Config.MAP_NUMBMATRIX_CENTRALPATH:
                    self._map[i][j] = (4, rectangle.Rectangle((x, y), self.getRectWidth(), self.getRectHeight(), centralPathImg))

                elif matrix[i][j] == config.Config.MAP_NUMBMATRIX_CHANGEDIRECTION:
                    self._map[i][j] = (5, rectangle.Rectangle((x, y), self.getRectWidth(), self.getRectHeight(), changeDirImg))

                x += self.getRectWidth()
            y += self.getRectHeight()
