from constants import *
from ghosts import *

class MainMode(object):
    def __init__(self):
        self.timer = 0
        self.scatter() # sets SCATTER as default mode

    def update(self, dt): 
        self.timer += dt
        if self.timer >= self.time:
            if self.mode is SCATTER:
                self.chase()
            elif self.mode is CHASE:
                self.scatter()
    
    def scatter(self):
        self.mode = SCATTER
        self.time = 7
        self.timer = 0

    def chase(self):
        self.mode = CHASE 
        self.time = 20
        self.timer = 0

class ModeController(object): # to know which mode the entity should be in
    def __init__(self, entity):
        self.timer = 0
        self.time = None
        self.mainmode = MainMode() # SCATTER(default) or CHASE
        self.current = self.mainmode.mode
        self.entity = entity

    def update(self, dt):
        self.mainmode.update(dt)
        if self.current is FREIGHT:
            self.timer += dt
            if self.timer >= self.time:
                self.time = None
                self.entity.normalMode()
                self.current = self.mainmode.mode
        elif self.current in [SCATTER, CHASE]:
            self.current = self.mainmode.mode

    def setFreightMode(self):
        if self.current in [SCATTER, CHASE]:
            self.timer = 0
            self.time = 7
            self.current = FREIGHT
        elif self.current is FREIGHT:
            self.timer = 0