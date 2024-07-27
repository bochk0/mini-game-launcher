from settings import *

class timer():
    def __init__(self, duration, func = None , repeat = None , autostart = False):
        self.duration = duration
        self.active = False
        self.start_timer = 0
        self.func = func
        self.repeat = repeat

        if autostart:
            self.activate()

    def activate(self):
        self.active = True
        self.start_timer = pygame.time.get_ticks()
    
    def deactivate(self):
        self.active = False
        self.start_timer = 0
        if self.repeat:
            self.activate()

    def update(self):
        if pygame.time.get_ticks() - self.start_timer >= self.duration :
            # print('in update')
            if self.func and self.start_timer != 0:
                self.func()
            self.deactivate()

