from platform import node
import pygame
from pygame.locals import *
from vector import Vector2
from constants import *
from nodes import *

class Pacman(object):
    def __init__(self, node):
        self.name = PACMAN
        # self.position = Vector2(200, 400)
        self.directions = {STOP:Vector2(), UP:Vector2(0,-1), DOWN:Vector2(0,1), LEFT:Vector2(-1, 0), RIGHT:Vector2(1, 0)}
        self.direction = STOP
        self.speed = 100
        self.radius = 10
        self.color = YELLOW
        self.node = node
        self.setPosition()
        self.target = node # node pacman is moving toward

    def setPosition(self):
        self.position = self.node.position.copy()
    
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        # self.direction = direction
        # self.node = self.getNewTarget(direction)
        # self.setPosition()
        if self.overshotTarget(): # corrects if pacman overshoots node
            self.node = self.target 
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            else:
                self.dirtion = STOP
            self.setPosition()
    
    def validDirection(self, direction): # checks if key pressed is a valid direction, if it has a node in that direction
        if direction is not STOP:
            if self.node.neighbors[direction] is not None:
                return True
            return False

    def getNewTarget(self, direction): # moves pacman if key press is valid
        if self.validDirection(direction):
            return self.node.neighbors[direction]
        return self.node

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

    def render(self, screen): # pygame needs circle drawn in integers
        p = self.position.asInt()
        pygame.draw.circle(screen, self.color, p, self.radius)

    def overshotTarget(self): # checks if pacman overshot taget node; if pacmand distance >= distance between nodes, he overshot
        if self.target is not None:
            vec1 = self.target.position - self.node.position
            vec2 = self.position - self.node.position
            node2Target = vec1.magnitudeSquared() # use magnitudeSquared to compare 2 distances to avoid taking square root
            node2Self = vec2.magnitudeSquared()
            return node2Self >= node2Target
        return False