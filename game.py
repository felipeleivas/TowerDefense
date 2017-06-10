# coding=utf-8
import pygame
import config

# Classe Game:
# Classe utilizada assim que o jogo é aberto.
# É a interface que permeia o jogo desde o menu,
# durante a partida, até a hora que o jogador clica no exit.
class Game:
    def __init__(self):
        self._gameExit = False
        self._noCashTimer = 0
        self._FPS = 0
        self._gameDisplay = 0
        self._clock = 0

    def setGameExit(self):
        self._gameExit = True

    def getGameExit(self):
        return self._gameExit

    def setGameDisplay(self, gameDisplay):
        self._gameDisplay = gameDisplay

    def getGameDisplay(self):
        return self._gameDisplay

    def setClock(self, clock):
        self._clock = clock

    def getClock(self):
        return self._clock

    def turnOnFPS(self):
        self._FPS = True

    def turnOffFPS(self):
        self._FPS = False

    def isFPSOn(self):
        return self._FPS

    def start(self):
        pygame.init()
        self._gameDisplay = pygame.display.set_mode((config.Config.DISPLAY_WIDTH, config.Config.DISPLAY_HEIGHT))
        pygame.display.set_caption("Tower Defense")
        self._clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)  # 1 second is 1000 milliseconds

    def update(self):
        pygame.display.update()

    def quit(self):
        pygame.quit()

    def getMousePosition(self):
        return pygame.mouse.get_pos()

    def getEvents(self):
        return pygame.event.get()

    def paintAllStuff(self, gameDisplay, clock):
        if self.isFPSOn():
           self.paintFPS(gameDisplay, clock.get_fps())

    def paintFPS(self, gameDisplay, fps):
        font = pygame.font.SysFont(None, 25)
        text = font.render("FPS = %.2f" % fps, True, (0,0,0))
        gameDisplay.blit(text, (0, 0))
