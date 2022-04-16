from re import L
from turtle import Screen, home
import pygame
from pygame.locals import *
from constants import *
from pacman import Pacman
from nodes import NodeGroup
from pellets import PelletGroup
from ghosts import *
from fruit import Fruit
from pause import Pause
from text import TextGroup

class GameController(object):
    def __init__(self):
        pygame.init() 
        self.screen = pygame.display.set_mode(SCREENSIZE, 0, 32) 
        self.background = None
        self.clock = pygame.time.Clock()
        self.fruit = None
        self.pause = Pause(True)
        self.level = 0
        self.lives = 5
        self.score = 0
        self.textgroup = TextGroup()

    def setBackground(self): # sets up background
        self.background = pygame.surface.Surface(SCREENSIZE).convert()
        self.background .fill(BLACK)

    def startGame(self):
        self.setBackground()
        self.nodes = NodeGroup("maze1.txt")
        self.nodes.setPortalPair((0, 17), (27, 17)) # temp hard coded portal neighbors
        homekey = self.nodes.createHomeNodes(11.5, 14) # temp hard coded based on maze1 txtFile
        self.nodes.connectHomeNodes(homekey, (12, 14), LEFT) # temp hard coded homeNodes left/right pos
        self.nodes.connectHomeNodes(homekey, (15,14), RIGHT)
        self.pacman = Pacman(self.nodes.getNodeFromTiles(15, 26)) # temp start node, as correct start position is between 2 nodes
        self.pellets = PelletGroup("maze1.txt") # creates PelletGroup object, passes in maze1 txtFile
        self.ghosts = GhostGroup(self.nodes.getStartTempNode(), self.pacman)
        self.ghosts.blinky.setStartNode(self.nodes.getNodeFromTiles((2+11.5), (0+14))) # all ghosts have their startNode + xOffset and yOffset values
        self.ghosts.pinky.setStartNode(self.nodes.getNodeFromTiles((2+11.5), (3+14)))
        self.ghosts.inky.setStartNode(self.nodes.getNodeFromTiles((0+11.5), (3+14)))
        self.ghosts.clyde.setStartNode(self.nodes.getNodeFromTiles((4+11.5), (3+14)))
        self.ghosts.setSpawnNode(self.nodes.getNodeFromTiles(2+11.5, 3+14)) # creates ghosts (list) object vs. just a ghost object
        self.nodes.denyHomeAccess(self.pacman)
        self.nodes.denyHomeAccessList(self.ghosts) # ghosts can only go UP
        self.nodes.denyAccessList(2+11.5, 3+14, LEFT, self.ghosts)
        self.nodes.denyAccessList(2+11.5, 3+14, RIGHT, self.ghosts)
        self.ghosts.inky.startNode.denyAccess(RIGHT, self.ghosts.inky)
        self.ghosts.clyde.startNode.denyAccess(LEFT, self.ghosts.clyde)
        self.nodes.denyAccessList(12, 14, UP, self.ghosts) # restrictions from original game
        self.nodes.denyAccessList(15, 14, UP, self.ghosts)
        self.nodes.denyAccessList(12, 26, UP, self.ghosts)
        self.nodes.denyAccessList(15, 26, UP, self.ghosts)

    def update(self): # called once per frame, game loop
        dt = self.clock.tick(30) / 1000.0 # changes method from Update() to FixedUpdate(), Unity method names
        self.textgroup.update(dt)
        self.pellets.update(dt)
        if not self.pause.paused:
            self.pacman.update(dt)
            self.ghosts.update(dt)
            if self.fruit is not None:
                self.fruit.update(dt)
            self.checkPelletEvents()
            self.checkGhostEvents()
            self.checkFruitEvents()
        afterPauseMethod = self.pause.update(dt)
        if afterPauseMethod is not None:
            afterPauseMethod()
        self.checkEvents()
        self.render()

    def render(self): 
        self.screen.blit(self.background, (0, 0)) # redraws background/erases all objects and redraws them at new positions
        self.nodes.render(self.screen) # placing before pacman so pellets appear in front of nodes when rendered
        self.pellets.render(self.screen) # drawn before pacman so pacman in front of pellets
        if self.fruit is not None:
            self.fruit.render(self.screen)
        self.pacman.render(self.screen)
        self.ghosts.render(self.screen)
        self.textgroup.render(self.screen)
        pygame.display.update()

    def updateScore(self, points):
        self.score += points
        self.textgroup.updateScore(self.score)

    def checkEvents(self): 
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.pacman.alive: # prevents pause during pacman death
                        self.pause.setPause(playerPaused=True)
                        if not self.pause.paused:
                            self.textgroup.hideText()
                            self.showEntities()
                        else:
                            self.textgroup.showText(PAUSETXT)
                            self.hideEntities() 

    def checkPelletEvents(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList) # sends pelletList to pacman; returns pellet he's colliding with, if any
        if pellet: # if pellet not None
            self.pellets.numEaten += 1
            self.updateScore(pellet.points)
            if self.pellets.numEaten == 30:
                self.ghosts.inky.startNode.allowAccess(RIGHT, self.ghosts.inky)
            if self.pellets.numEaten == 70:
                self.ghosts.clyde.startNode.allowAccess(LEFT, self.ghosts.clyde)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == POWERPELLET:
                self.ghosts.startFreight()
            if self.pellets.isEmpty(): # game pauses for 3 sec after last pellet eaten before calling nextLevel(); hides entities during this time
                self.hideEntities()
                self.pause.setPause(pauseTime=3, func=self.nextLevel)

    def checkGhostEvents(self): # returns which ghost from ghosts list pacman is colliding with vs bool if colliding; will return None if not colliding
        for ghost in self.ghosts:
            if self.pacman.collideGhost(ghost):
                if ghost.mode.current is FREIGHT:
                    self.pacman.visible = False
                    ghost.visible = False
                    self.updateScore(ghost.points)
                    self.textgroup.addText(str(ghost.points), WHITE, ghost.position.x, ghost.position.y, 8, time=1)
                    self.ghosts.updatePoints()
                    self.pause.setPause(pauseTime=1, func=self.showEntities) # will pause game for 1 sec, showEntities after
                    ghost.startSpawn()
                    self.nodes.allowHomeAccess(ghost) # ghosts allowed in home during SPAWN
                elif ghost.mode.current is not SPAWN: # pacman ignores ghost in SPAWN
                    if self.pacman.alive:
                        self.lives -= 1
                        self.pacman.die()
                        self.ghosts.hide()
                        if self.lives <= 0:
                            self.textgroup.showText(GAMEOVERTEXT)
                            self.pause.setPause(pauseTime=3, func=self.restartGame)
                        else:
                            self.pause.setPause(pauseTime=3, func=self.resetLevel)

    def checkFruitEvents(self):
        if self.pellets.numEaten == 50 or self.pellets.numEaten == 140:
            if self.fruit is None:
                self.fruit = Fruit(self.nodes.getNodeFromTiles(9, 20)) # starting node sent to Fruit class as param
        if self.fruit is not None:
            if self.pacman.collideCheck(self.fruit): # if fruit exists and has been eaten by pacman
                self.updateScore(self.fruit.points)
                self.textgroup.addText(str(self.fruit.points), WHITE, self.fruit.position.x, self.fruit.position.y, 8, time=1)
                self.fruit = None
            elif self.fruit.destroy: # if fruit timer runs out and is destoryed
                self.fruit = None

    def showEntities(self):
        self.pacman.visible = True
        self.ghosts.show()

    def hideEntities(self): # allows hide all entities (when game paused)
        self.pacman.visible = False
        self.ghosts.hide()

    def nextLevel(self): # increments level, repauses game, starts game over; origial pacMan was same level with slightly altered game mechanics each time
        self.showEntities()
        self.level += 1
        self.pause.paused = True
        self.startGame()
        self.textgroup.updateLevel(self.level)

    def restartGame(self):
        self.lives = 5
        self.level = 0
        self.pause.paused = True
        self.fruit = None
        self.startGame()
        self.score = 0
        self.textgroup.updateScore(self.score)
        self.textgroup.updateLevel(self.level)
        self.textgroup.showText(READYTXT)

    def resetLevel(self):
        self.pause.paused = True
        self.pacman.reset() 
        self.ghosts.reset() # reset() from entity class
        self.fruit = None
        self.textgroup.showText(READYTXT)

if __name__ == "__main__":
    game = GameController()
    game.startGame()
    while True:
        game.update()