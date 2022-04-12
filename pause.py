import pygame
from constants import *

class Pause(object):
    def __init__(self, paused=False):
        self.paused = paused
        self.timer = 0 # for instances when we want to pause the game programmically using time
        self.pauseTime = None
        self.func = None # ref for a method to run after a pause is finished

    def update(self, dt):
        if self.pauseTime is not None:
            self.timer += dt
            if self.timer >= self.pauseTime:
                self.timer = 0
                self.paused = False
                self.pauseTime = None
                return self.func # returns method (if any) to the calling object
        return None

    def setPause(self, playerPaused = False, pauseTime = None, func = None): # player vs game pause, will pass in func if any
        self.timer = 0
        self.func = func
        self.pauseTime = pauseTime
        self.flip()

    def flip(self):
        self.paused = not self.paused