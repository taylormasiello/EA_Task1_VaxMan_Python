from platform import node
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from nodes import *
from entity import Entity

class Pacman(Entity):
    def __init__(self, node):
        Entity.__init__(self, node)
        self.name = PACMAN
        self.color = YELLOW
        self.direction = LEFT # when game starts, pacMan will start move LEFT vs standing still until player input
        self.setBetweenNodes(LEFT) # pacman between nodes is accurate to original game
        self.alive = True
    
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        if self.overshotTarget(): # corrects if pacman overshoots node; if target node valid, move in that direction; if not, stop on that node
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None: # check if node is portal, if true pacman will "jump" between
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.target = self.getNewTarget(self.direction)
            if self.target is self.node: 
                self.direction = STOP
            self.setPosition()
        else: # if not overshooting a node, traveling between nodes, so can reverse direction
            if self.oppositeDirection(direction):
                self.reverseDirection()

    def getValidKey(self):
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_UP]:
            return UP
        if key_pressed[K_DOWN]:
            return DOWN
        if key_pressed[K_LEFT]:
            return LEFT
        if key_pressed[K_RIGHT]:
            return RIGHT
        return STOP

    def eatPellets(self, pelletList):
        for pellet in pelletList: # loops through pelletList, if pacman collides w/ pellet, returns pellet
            if self.collideCheck(pellet):
                return pellet
        return None

    def collideGhost(self, ghost):
        return self.collideCheck(ghost)
    
    def collideCheck(self, other): # checks collision with some entity
        d = self.position - other.position
        dSquared = d.magnitudeSquared()
        rSquared = (self.collideRadius + other.collideRadius)**2
        if dSquared <= rSquared:
            return True
        return False

    def reset(self): # extending reset() from entity
        Entity.reset(self)
        self.direction = LEFT
        self.setBetweenNodes(LEFT)
        self.alive = True

    def die(self):
        self.alive = False
        self.direction = STOP
