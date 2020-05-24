import pygame
import math
import random
from pygame.locals import *

class Particle:
    def __init__(self):
        self.pos = [200, 200]
        self.rays = []
        for i in range(0, 360, 1):
            self.rays.append(Ray(self.pos, math.radians(i)))

    def show(self, canvas):
        pygame.draw.circle(canvas, (255, 255, 255), self.pos, 5)
        for ray in self.rays:
            ray.show(canvas)

    def getLength(self, a, b):
        x1 = a[0]
        y1 = a[1]
        x2 = b[0]
        y2 = b[1]
        hLength = x1 - x2
        vLength = y1 - y2
        d = math.sqrt((hLength * hLength) + (vLength * vLength))
        return d

    def look(self, walls, canvas):
        for ray in self.rays:
            closest = None
            record = math.inf
            for wall in walls:
                pt = ray.cast(wall)
                if pt:
                    d = self.getLength(self.pos, pt)
                    if d < record:
                        record = d
                        closest = pt
            if closest:
                closest[0] = int(closest[0])
                closest[1] = int(closest[1])
                pos = [0, 0]
                pos[0] = int(self.pos[0])
                pos[1] = int(self.pos[1])
                rayLine = pygame.draw.line(canvas, (255, 255, 255), pos, closest, 1)



    def updatePos(self, x, y):
        self.pos[0] = int(x)
        self.pos[1] = int(y)


class Boundry:
    def __init__(self, x1, y1, x2, y2):
        self.a = [x1, y1]
        self.b = [x2, y2]

    def show(self, canvas):
        pygame.draw.line(canvas, (255, 255, 255), self.a, self.b, 1)


class Ray:
    def __init__(self, pos, angle):
        self.pos = pos
        self.dir = [math.cos(angle), math.sin(angle)]

    def show(self, canvas):
         rayLine = pygame.draw.line(canvas, (255, 255, 255), [self.pos[0], self.pos[1]] , [self.pos[0] + self.dir[0] * 10, self.pos[1] + self.dir[1] * 10], 1)

    def lookAt(self, x, y):
        self.dir[0] = x - self.pos[0]
        self.dir[1] = y - self.pos[1]

        # Normalise
        length = math.sqrt((self.dir[0] * self.dir[0]) + (self.dir[1] * self.dir[1]))

        self.dir[0] = self.dir[0]/length
        self.dir[1] = self.dir[1]/length


    def cast(self, wall):
        x1 = wall.a[0]
        y1 = wall.a[1]
        x2 = wall.b[0]
        y2 = wall.b[1]

        x3 = self.pos[0]
        y3 = self.pos[1]
        x4 = self.pos[0] + self.dir[0]
        y4 = self.pos[1] + self.dir[1]

        den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        if den == 0:
            return None

        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / den

        if t > 0 and t < 1 and u > 0:
            pt = [0, 0]
            pt[0] = x1 + t * (x2 - x1)
            pt[1] = y1 + t * (y2 - y1)
            return pt
        else:
            return None

class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True
        self.walls = []
        self.walls.append(Boundry(0, 0, 640, 0))
        self.walls.append(Boundry(0, 0, 0, 400))
        self.walls.append(Boundry(640, 0, 640, 400))
        self.walls.append(Boundry(0, 400, 640, 400))
        for i in range(5):
            x1 = random.randint(0, 640)
            y1 = random.randint(0, 400)
            x2 = random.randint(0, 640)
            y2 = random.randint(0, 400)
            self.walls.append(Boundry(x1, y1, x2, y2))
        self.particle = Particle()

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        mousex, mousey = pygame.mouse.get_pos()
        self.particle.updatePos(mousex, mousey)

    def on_render(self):
        self._display_surf.fill(pygame.Color("black"))
        self.particle.show(self._display_surf)
        self.particle.look(self.walls, self._display_surf)
        for wall in self.walls:
            wall.show(self._display_surf)
        pygame.display.update()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()
    theApp.on_execute()
