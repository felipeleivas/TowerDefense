import config
import pygame
import sys
import map
import rectangle

class MapCreator:
	def __init__(self):
		self._conf = config.Config()
		self._screen = pygame.display.set_mode(self._conf.DISPLAY_SIZE)
		self._matrix = [[0 for aux in range(self._conf.MAP_DIMX)] for aux2 in range(self._conf.MAP_DIMY)]
		self._rectMap = map.Map(self._conf.MAP_DIMS, self._conf.RECT_DIMS_px, self._matrix)
		self._towerMenuBackground = pygame.image.load(self._conf.CREATIONMODE_IMAGE)

	def getConf(self):
		return self._conf

	def getRectMap(self):
		return self._rectMap

	def getMatrix(self):
		return self._matrix

	def getScreen(self):
		return self._screen

	def setMatrix(self, matrix):
		self._matrix = matrix

	def setRectMap(self, rectMap):
		self._rectMap = rectMap

	def setMatrixElement(self,coords,value=0):
		try:
			if self._isValidValue(value):
				x = coords[1]
				y = coords[0]
				self._matrix[x][y] = value
			else:
				raise ValueError("Invalid value !")
		except IndexError:
			print("Not valid X or Y coords !")
			raise
		except TypeError:
			pass

	def getMatrixElement(self,x,y):
		pass

	def setWindowCaption(self, string):
		pygame.display.set_caption(string)

	def getClickedSquare(self, pxPosition): #TODO: Nao deixar ser maior ou menor que MAP_DIMS
		xPos = int(pxPosition[0]/self.getConf().RECT_DIMX_px)
		yPos = int(pxPosition[1]/self.getConf().RECT_DIMX_px)
		if xPos < self.getConf().MAP_DIMX and yPos < self.getConf().MAP_DIMY:	
			return (xPos, yPos)
		pass

	def _isValidValue(self,value):
		if value in self._conf.MAP_NUMBMATRIX_VALUES:
			return True
		return False

	def _updateRectMap(self):
		self.setRectMap(map.Map(self._conf.MAP_DIMS, self._conf.RECT_DIMS_px, self._matrix))
		for i in range(0, self.getRectMap().getDimension()[0]):
			for j in range(0, self.getRectMap().getDimension()[1]):
				self.getRectMap().getMap()[i][j][1].paint(self.getScreen())

	def _updateScreenBuffer(self):
		self._updateRectMap()
		#TODO: More things in here

	def _show(self):
		pygame.display.update()

	def start(self):
		pygame.init()
		self.getScreen().blit(self._towerMenuBackground, (480, 0))

		isLeftClicked = False
		isRightClicked = False

		while True:
			mousePos = pygame.mouse.get_pos()

			if isLeftClicked:
				self.setMatrixElement(self.getClickedSquare(mousePos),value=1)

			elif isRightClicked:
				self.setMatrixElement(self.getClickedSquare(mousePos),value=0)

			event = pygame.event.poll() # same as 'for event in pygame.event.get():' but more elegant

			if event.type == pygame.QUIT or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE):
				print("Saving map...")
				
				file = open('maps/map1.map', 'w') #TODO: Better saving naming options

				for line in self.getMatrix():
					file.write(str(line)+'\n')

				file.close()

				sys.exit("Exiting Map Creation !")

			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				isLeftClicked = True
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				isLeftClicked = False
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
				isRightClicked = True
			if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
				isRightClicked = False

			self._updateScreenBuffer()
			self._show()


if __name__ == '__main__':
	mapcreator = MapCreator()
	mapcreator.setWindowCaption("Map Creation Window !")
	mapcreator.start()
	