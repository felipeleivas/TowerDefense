# coding=utf-8
import pygame
import config
import towerdefense
import player
import game

game = game.Game()
game.start()
player = player.Player("Vinicius")
towerDefense = towerdefense.TowerDefense(player)

while not game.getGameExit():

    mousePosition = game.getMousePosition()

    for event in game.getEvents():
        if event.type == pygame.QUIT:
            game.setGameExit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            towerDefense.mousePress(game.getMousePosition(), game.getGameDisplay())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                if game.isFPSOn():
                    game.turnOffFPS()
                else:
                    game.turnOnFPS()
            elif event.key == pygame.K_LSHIFT:
                towerDefense.turnOnShift()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                towerDefense.turnOffShift()
        if event.type == pygame.USEREVENT + 1:
            towerDefense.decTimer()

    towerDefense.paintAllStuff(game.getGameDisplay(), mousePosition)
    game.paintAllStuff(game.getGameDisplay(), game.getClock())
    game.getClock().tick()
    game.update()
    game.getClock().tick(config.Config.FPS)      # Determina o FPS máximo

game.quit()
quit()
