import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import Ghost

class GameController(object):
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32) 
        self.background = None
        self.clock = pygame.time.Clock()

    def setBackground(self): # sets up background
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background .fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17)) # temp hard coded portal neighbors
        # self.nodes.setupTestNodes()
        # self.pacman = Pacman(self.nodes.nodeList[0])
        self.pacman = Pacman(self.nodes.getStartTempNode())
        self.pellets = PelletGroup("maze1.txt") # creates PelletGroup object, passes in maze1 txtFile
        self.ghost = Ghost(self.nodes.getStartTempNode(), self.pacman) 

    def update(self): # called once per frame, game loop
        dt = self.clock.tick(30) / 1000.0 # changes method from Update() to FixedUpdate(), Unity method names
        self.pacman.update(dt)
        self.ghost.update(dt)
        self.pellets.update(dt)
        self.checkPelletEvents()
        self.checkEvents()
        self.render()

    def checkEvents(self): 
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()                

    def render(self): 
        self.screen.blit(self.background, (0, 0)) # redraws background/erases all objects and redraws them at new positions
        self.nodes.render(self.screen) # placing before pacman so pellets appear in front of nodes when rendered
        self.pellets.render(self.screen) # drawn before pacman so pacman in front of pellets
        self.pacman.render(self.screen)
        self.ghost.render(self.screen)
        pygame.display.update() 

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList) # sends pelletList to pacman; returns pellet he's colliding with, if any
        if pellet: # if pellet not None
            self.pellets.numEaten += 1
            self.pellets.pelletList.remove(pellet)

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()