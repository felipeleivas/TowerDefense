import pygame

# Classe Rectangle:
# Unidade da tela do jogo, de onde todas as outras derivam.F
class Rectangle(object):
    def __init__(self, position, width, height, image):
        self._position = position # top left
        self._width = width
        self._height = height
        self._image = pygame.image.load(image)
        self._imageString = image

    def collide(self, rectTwo):
        rectTwoPos = rectTwo.getPosition()
        rectTwoWidth, rectTwoheight = rectTwo.getDims()
        position1 = (rectTwoPos[0] + 1, rectTwoPos[1]+1)
        position2 = (rectTwoPos[0] + rectTwoWidth - 1, rectTwoPos[1] + 1)
        position3 = (rectTwoPos[0] + rectTwoWidth - 1, rectTwoPos[1] + rectTwoheight - 1)
        position4 = (rectTwoPos[0] + 1, rectTwoPos[1] + rectTwoheight - 1)
        if self.isInside(position1) or self.isInside(position2) or self.isInside(position3) or self.isInside(position4):
            return True
        return False

    def calcCenter(self):
        xPosition, yPosition = self._position
        xCenter, yCenter = xPosition + .5 * self._width, yPosition + .5 * self._height
        return int(xCenter), int(yCenter)

    def getImage(self):
        return self._image

    def getImageString(self):
        return self._imageString

    def setImage(self, image):
        self._image = pygame.image.load(image)

    def getPosition(self):
        return self._position

    def setPosition(self, position):
        self._position = position
        self.calcCenter()

    def getCenter(self):
        return self.calcCenter()

    def getWidth(self):
        return self._width

    def setWidth(self, width):
        self._width = width
        self.calcCenter()

    def getheight(self):
        return self._height

    def setheight(self, height):
        self._height = height
        self.calcCenter()

    def getDims(self):
        return self.getWidth(), self.getheight()

    def paint(self, surface):
        surface.blit(self._image, self._position)

    def isInside(self, position):
        if self._position[0] <= position[0] < self._position[0] + self._width:
            if self._position[1] <= position[1] < self._position[1] + self._height:
                return True
        return False
