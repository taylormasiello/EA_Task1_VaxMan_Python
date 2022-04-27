from sre_constants import IN
import pygame
import numpy as np # type: ignore ; supression of incorrect warning
from vector import Vector2
from constants import *

# creates connected graph data structure as a node map
class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None, PORTAL: None} # node neighbors set up as dictionary
        self.access = {UP: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], # dictionary
                    DOWN: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], # keys - 4 directions entities can go
                    LEFT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT], # values - entities that have access to travel in that direction
                    RIGHT: [PACMAN, BLINKY, PINKY, INKY, CLYDE, FRUIT]}

    def denyAccess(self, direction, entity):
        if entity.name in self.access[direction]:
            self.access[direction].remove(entity.name)
    
    def allowAccess(self, direction, entity):
        if entity.name not in self.access[direction]:
            self.access[direction].append(entity.name)

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4) # draws edges between nodes in graph, node map
                pygame.draw.circle(screen, RED, self.position.asInt(), 12) # draws node

class NodeGroup(object):
    def __init__(self, level): # brings in txtFile as level data input
        self.level = level
        self.nodesLUT = {} # dictionary containing nodes, easier to look up nodes; LUT means "Look Up Table"
        self.nodeSymbols = ['+', 'P', 'n']
        self.pathSymbols = ['.', '-', '|', 'p']
        data = self.readMazeFile(level)
        self.createNodeTable(data)
        self.connectHorizontally(data)
        self.connectVertically(data)
        self.homekey = None

    def render(self, screen): # loops through nodeList and calls nodes render method
        for node in self.nodesLUT.values():
            node.render(screen)

    def readMazeFile(self, textfile): #reads txtFile of level data and returns 2D numpy array
        return np.loadtxt(textfile, dtype='<U1')

    def createNodeTable(self, data, xoffset=0, yoffset=0): # data is the 2D numpy array; creates entry in LUT, creates node at (row, col); dictionary keys (x, y) tuple, values node object with (x, y) location passed to it also;
        for row in list(range(data.shape[0])):
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols:
                    x, y = self.constructKey(col + xoffset, row + yoffset)
                    self.nodesLUT[(x, y)] = Node(x, y)

    def constructKey(self, x, y): # converts row,col from textFile to screen pixel values; multiplies by tileSizes
        return x * TILEWIDTH, y * TILEHEIGHT

    def connectHorizontally(self, data, xoffset=0, yoffset=0): # connects horizontal nodes from data;
        for row in list(range(data.shape[0])):
            key = None # set to None at start of each new row
            for col in list(range(data.shape[1])):
                if data[row][col] in self.nodeSymbols: # if '+' found, looks at key value
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset) # set to key of node in dictionary
                    else: # if key is not None, connect 2 nodes together
                        otherkey = self.constructKey(col + xoffset, row + yoffset) 
                        self.nodesLUT[key].neighbors[RIGHT] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[LEFT] = self.nodesLUT[key]
                        key = otherkey
                elif data[row][col] not in self.pathSymbols: # if char not '.' for pathSymbol, key reset to None
                    key = None
    
    def connectVertically(self, data, xoffset=0, yoffset=0):
        dataT = data.transpose() # transposes data array; cols become rows and rows become cols; keys flipped as result, (m, n) shaped array to (n, m)
        for col in list(range(dataT.shape[0])):
            key = None
            for row in list(range(dataT.shape[1])):
                if dataT[col][row] in self.nodeSymbols:
                    if key is None:
                        key = self.constructKey(col + xoffset, row + yoffset)
                    else:
                        otherkey = self.constructKey(col + xoffset, row + yoffset)
                        self.nodesLUT[key].neighbors[DOWN] = self.nodesLUT[otherkey]
                        self.nodesLUT[otherkey].neighbors[UP] = self.nodesLUT[key]
                        key = otherkey
                elif dataT[col][row] not in self.pathSymbols:
                    key = None

    def getNodeFromPixels(self, xpixel, ypixel): 
        if (xpixel, ypixel) in self.nodesLUT.keys():
            return self.nodesLUT[(xpixel, ypixel)]
        return None
    
    def getNodeFromTiles(self, col, row):
        x, y = self.constructKey(col, row)
        if (x, y) in self.nodesLUT.keys():
            return self.nodesLUT[(x, y)]
        return None

    def createHomeNodes(self, xoffset, yoffset):
        homedata = np.array([['X','X','+','X','X'],
                             ['X','X','.','X','X'],
                             ['+','X','.','X','+'],
                             ['+','.','+','.','+'],
                             ['+','X','X','X','+']])
        
        self.createNodeTable(homedata, xoffset, yoffset)
        self.connectHorizontally(homedata, xoffset, yoffset)
        self.connectVertically(homedata, xoffset, yoffset)
        self.homekey = self.constructKey(xoffset+2, yoffset)
        return self.homekey # key to top node of homedata

    def connectHomeNodes(self, homekey, otherkey, direction): # connects topmost node to specified node
        key = self.constructKey(*otherkey)
        self.nodesLUT[homekey].neighbors[direction] = self.nodesLUT[key] # allows embedded homeNodes to be interactable...
        self.nodesLUT[key].neighbors[direction*-1] = self.nodesLUT[homekey] # ...in both directions

    def setPortalPair(self, pair1, pair2): # takes 2 tuple values, checks to see if both in nodesLUT; if yes, connected as portals
        key1 = self.constructKey(*pair1)
        key2 = self.constructKey(*pair2)
        if key1 in self.nodesLUT.keys() and key2 in self.nodesLUT.keys():
            self.nodesLUT[key1].neighbors[PORTAL] = self.nodesLUT[key2]
            self.nodesLUT[key2].neighbors[PORTAL] = self.nodesLUT[key1]

    def getStartTempNode(self): # temp method to start pacman on first node in LUT
        nodes = list(self.nodesLUT.values())
        return nodes[0]

    # restrict/allow access 
    def denyAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.denyAccess(direction, entity)

    def allowAccess(self, col, row, direction, entity):
        node = self.getNodeFromTiles(col, row)
        if node is not None:
            node.allowAccess(direction, entity)

    def denyAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)
    
    def allowAccessList(self, col, row, direction, entities):
        for entity in entities:
            self.denyAccess(col, row, direction, entity)

    def denyHomeAccess(self, entity):
        self.nodesLUT[self.homekey].denyAccess(DOWN, entity)

    def allowHomeAccess(self, entity):
        self.nodesLUT[self.homekey].allowAccess(DOWN, entity)

    def denyHomeAccessList(self, entities):
        for entity in entities:
            self.denyHomeAccess(entity)
    
    def allowHomeAccessList(self, entities):
        for entity in entities:
            self.allowHomeAccess(entity)