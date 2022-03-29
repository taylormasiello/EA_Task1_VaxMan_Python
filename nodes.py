from typing import no_type_check_decorator
import pygame
from vector import Vector2
from constants import *

class Node(object):
    def __init__(self, x, y):
        self.position = Vector2(x, y)
        self.neighbors = {UP:None, DOWN:None, LEFT:None, RIGHT:None} # node neighbors set up as dictionary

    def render(self, screen):
        for n in self.neighbors.keys():
            if self.neighbors[n] is not None:
                line_start = self.position.asTuple()
                line_end = self.neighbors[n].position.asTuple()
                pygame.draw.line(screen, WHITE, line_start, line_end, 4) # draws edges between nodes in graph, node map
                pygame.draw.circle(screen, RED, self.position.asInt(), 12) # draws node

class NodeGroup(object):
    def __init__(self):
        self.nodeList = [] # init empty list of of nodes

    def setupTestNodes(self): # manually populating node list
        nodeA = Node(80, 80) # node locations
        nodeB = Node(160, 80)
        nodeC = Node(80, 160)
        nodeD = Node(160, 160)
        nodeE = Node(208, 160)
        nodeF = Node(80, 320)
        nodeG = Node(208, 320)
        nodeA.neighbors[RIGHT] = nodeB # linking nodes by adding nodes to neighbors dictionary of each node
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF
        self.nodeList = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG] # add all nodes to nodeList

    def render(self, screen): # loops through nodeList and calls nodes render method
        for node in self.nodeList:
            node.render(screen)