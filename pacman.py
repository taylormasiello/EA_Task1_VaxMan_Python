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
    
    def update(self, dt):
        self.position += self.directions[self.direction]*self.speed*dt
        direction = self.getValidKey()
        # self.direction = direction
        # self.node = self.getNewTarget(direction)
        # self.setPosition()
        if self.overshotTarget(): # corrects if pacman overshoots node; if target node valid, move in that direction; if not, stop on that node
            self.node = self.target
            if self.node.neighbors[PORTAL] is not None: # check if node is portal, if true pacman will "jump" between
                self.node = self.node.neighbors[PORTAL]
            self.target = self.getNewTarget(direction)
            if self.target is not self.node:
                self.direction = direction
            # else:
            #     self.dirtion = STOP
            # self.setPosition()
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
            # d = self.position - pellet.position
            # dSquared = d.magnitudeSquared()
            # rSquared = (pellet.radius+self.collideRadius)**2
            # if dSquared <= rSquared:
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

    # def validDirection(self, direction): # checks if key pressed is a valid direction, if it has a node in that direction
    #     if direction is not STOP:
    #         if self.node.neighbors[direction] is not None:
    #             return True
    #         return False

    # def getNewTarget(self, direction): # moves pacman if key press is valid
    #     if self.validDirection(direction):
    #         return self.node.neighbors[direction]
    #     return self.node

    # def render(self, screen): # pygame needs circle drawn in integers
    #     p = self.position.asInt()
    #     pygame.draw.circle(screen, self.color, p, self.radius)

    # def overshotTarget(self): # checks if pacman overshot taget node; if pacmand distance >= distance between nodes, he overshot
    #     if self.target is not None:
    #         vec1 = self.target.position - self.node.position
    #         vec2 = self.position - self.node.position
    #         node2Target = vec1.magnitudeSquared() # use magnitudeSquared to compare 2 distances to avoid taking square root
    #         node2Self = vec2.magnitudeSquared()
    #         return node2Self >= node2Target
    #     return False

    # def reverseDirection(self): # swaps values to opposite based on constants as flipped values
    #     self.direction *= -1
    #     temp = self.node
    #     self.node = self.target
    #     self.target = temp
    
    # def oppositeDirection(self, direction): # validates checks input direction is opposite of current direction; only these moves available between nodes
    #     if direction is not STOP:
    #         if direction == self.direction * -1:
    #             return True
    #         return False 
    

