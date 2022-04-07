import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from entity import Entity
from modes import ModeController

class Ghost(Entity):
    def __init__(self, node, pacman=None, blinky=None):
        Entity.__init__(self, node)
        self.name = GHOST
        self.points = 200
        self.goal = Vector2()
        self.directionMethod = self.goalDirection
        self.pacman = pacman
        self.mode = ModeController(self)
        self.blinky = blinky
        self.homeNode = node

    def update(self, dt):
        self.mode.update(dt)
        if self.mode.current is SCATTER: 
            self.scatter()
        elif self.mode.current is CHASE:
            self.chase()
        Entity.update(self, dt) 
    
    def scatter(self):
        self.goal = Vector2()

    def chase(self):
        self.goal = self.pacman.position

    def startFreight(self):
        self.mode.setFreightMode()
        if self.mode.current == FREIGHT: 
            self.setSpeed(50) 
            self.directionMethod = self.randomDirection

    def normalMode(self): 
        self.setSpeed(100) 
        self.directionMethod = self.goalDirection

    def spawn(self):
        self.goal = self.spawnNode.position
        
    def setSpawnNode(self, node):
        self.spawnNode = node

    def startSpawn(self):
        self.mode.setSpawnMode()
        if self.mode.current == SPAWN:
            self.setSpeed(150)
            self.directionMethod = self.goalDirection
            self.spawn()

class Blinky(Ghost): # defaul SCATTER & CHASE methods
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = BLINKY
        self.color = RED

class Pinky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = PINKY
        self.color = PINK
    
    def scatter(self): # top right corner as SCATTER target/goal
        self.goal = Vector2(TILEWIDTH*NCOLS, 0)

    def chase(self): # 4 tiles ahead of pacman as CHASE target/goal
        self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

class Inky(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = INKY
        self.color = TEAL
    
    def scatter(self): # SCATTER target as bottom right corner 
        self.goal = Vector2(TILEWIDTH*NCOLS, TILEHEIGHT*NROWS)

    def chase(self): # CHASE target == ((((2 tiles in front of Pacman's position) - (Blinky's position)) * 2) + (Blinky's position))
        vec1 = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 2
        vec2 = (vec1 - self.blinky.position) * 2
        self.goal = self.blinky.position + vec2
        
class Clyde(Ghost):
    def __init__(self, node, pacman=None, blinky=None):
        Ghost.__init__(self, node, pacman, blinky)
        self.name = CLYDE
        self.color = ORANGE
    
    def scatter(self): # SCATTER target as bottom left corner
        self.goal = Vector2(0, TILEHEIGHT*NROWS)
    
    def chase(self): # if 8 tiles from Pacman, will SCATTER; else taget as 4 tiles ahead of pacman (like Pinky)
        d = self.pacman.position - self.position
        ds = d.magnituedSqured()
        if ds <= (TILEWIDTH * 8)**2:
            self.scatter()
        else:
            self.goal = self.pacman.position + self.pacman.directions[self.pacman.direction] * TILEWIDTH * 4

class GhostGroup(object): # loops through generated ghostList and calls/performs methods/actions to/for each ghost
    def __init__(self, node, pacman):
        self.blinky = Blinky(node, pacman)
        self.pinky = Pinky(node, pacman)
        self.inky = Inky(node, pacman)
        self.clyde = Clyde(node, pacman)
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde] # all ghosts objects stored in a list

    def __iter__(self): # shortens list ref; self.ghosts to self
        return iter(self.ghosts)

    def update(self, dt): 
        for ghost in self:
            ghost.update(dt)
    
    def startFreight(self):
        for ghost in self:
            ghost.startFreight()
        self.resetPoints() 

    def setSpawnNode(self, node):
        for ghost in self:
            ghost.setSpawnNode(node)

    def updatePoints(self):
        for ghost in self:
            ghost.points *= 2

    def resetPoints(self):
        for ghost in self:
            ghost.points = 200

    def reset(self):
        for ghost in self:
            ghost.reset()

    def hide(self):
        for ghost in self:
            ghost.visible = False

    def show(self):
        for ghost in self:
            ghost.visible = True

    def render(self, screen):
        for ghost in self:
            ghost.render(screen)