import rectangle

class Shot(rectangle.Rectangle):
    def __init__(self, position, width, height, image, speed, targetPosition, damage):
        super(Shot, self).__init__(position, width, height, image)
        self._speed = speed
        self._direction = self.calculateDirection(targetPosition)
        self._damage = damage

    def getSpeed(self):
        return self._speed

    def setSpeed(self, speed):
        self._speed = speed

    def getDamage(self):
        return self._damage

    def calculateDirection(self, targetPosition):
        vector = targetPosition[0] - self._position[0], targetPosition[1] - self._position[1]
        vector = vector[0] / 4, vector[1] / 4
        return vector

    def move(self):
        newPositionX = self._position[0] + self._direction[0]
        newPositionY = self._position[1] + self._direction[1]
        self.setPosition((newPositionX, newPositionY))

    def destroy(self, tower):
        tower.delShot(self)


