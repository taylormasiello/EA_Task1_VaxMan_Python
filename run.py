import pygame
from pygame.locals import *
from constants import *

pygame.init() # debug fix 1
screen = pygame.display.set_mode(SCREENSIZE, 0, 32) # debug fix 1

class GameController(object):
    def _init_(self):
        # pygame.init() -bug 1
        # self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32) -bug 1
        self.background = None

    def setBackground(self): # sets up background
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background .fill(BLACK)

    def startGame(self):
        self.setBackground()

    def update(self): # called once per frame, game loop
        self.checkEvents()
        self.render()

    def checkEvents(self): 
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()                

    def render(self): 
        pygame.display.update()

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()