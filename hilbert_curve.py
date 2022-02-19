import pygame as pg
import math

# Globals
width = 900
height = 900
screen = pg.display.set_mode((width, height))
clock = pg.time.Clock()
fps = 60
white = (255,255,255)
black = (0,0,0)

class Unit():
    def __init__(self, size, x, y, typ):
        self.size = size
        self.x = x
        self.y = y
        self.typ = typ
        self.points = self.get_points()
    
    def get_points(self):
        if self.typ == 'A':
            p1 = (self.x+self.size/4, self.y+self.size*3/4)
            p2 = (self.x+self.size/4, self.y+self.size/4)
            p3 = (self.x+self.size*3/4, self.y+self.size/4)
            p4 = (self.x+self.size*3/4, self.y+self.size*3/4)
        if self.typ == 'B':
            p1 = (self.x+self.size*3/4, self.y+self.size/4)
            p2 = (self.x+self.size/4, self.y+self.size/4)
            p3 = (self.x+self.size/4, self.y+self.size*3/4)
            p4 = (self.x+self.size*3/4, self.y+self.size*3/4)
        if self.typ == 'C':
            p1 = (self.x+self.size*3/4, self.y+self.size/4)
            p2 = (self.x+self.size*3/4, self.y+self.size*3/4)
            p3 = (self.x+self.size/4, self.y+self.size*3/4)
            p4 = (self.x+self.size/4, self.y+self.size/4)
        if self.typ == 'D':
            p1 = (self.x+self.size/4, self.y+self.size*3/4)
            p2 = (self.x+self.size*3/4, self.y+self.size*3/4)
            p3 = (self.x+self.size*3/4, self.y+self.size/4)
            p4 = (self.x+self.size/4, self.y+self.size/4)
        return [p1, p2, p3, p4]
    
    def draw(self, surface):
        pg.draw.line(surface, white, self.points[0], self.points[1])
        pg.draw.line(surface, white, self.points[1], self.points[2])
        pg.draw.line(surface, white, self.points[2], self.points[3])
    
class Hilbert():
    def __init__(self, order):
        self.order = order
        self.units = []
        self.iterate([Unit(width, 0, 0, 'C')])
    
    def iterate(self, units):
        if len(units) >= 4**(self.order - 1):
            self.units = units[:]
            return
        new_units = []
        for unit in units:
            size = unit.size/2
            x = unit.x
            y = unit.y
            if unit.typ == 'A':
                u1 = Unit(size, x, y+size, 'D')
                u2 = Unit(size, x, y, 'A')
                u3 = Unit(size, x+size, y, 'A')
                u4 = Unit(size, x+size, y+size, 'B')
                
            if unit.typ == 'B':
                u1 = Unit(size, x+size, y, 'C')
                u2 = Unit(size, x, y, 'B')
                u3 = Unit(size, x, y+size, 'B')
                u4 = Unit(size, x+size, y+size, 'A')
                
            if unit.typ == 'C':
                u1 = Unit(size, x+size, y, 'B')
                u2 = Unit(size, x+size, y+size, 'C')
                u3 = Unit(size, x, y+size, 'C')
                u4 = Unit(size, x, y, 'D')
            if unit.typ == 'D':
                u1 = Unit(size, x, y+size, 'A')
                u2 = Unit(size, x+size, y+size, 'D')
                u3 = Unit(size, x+size, y, 'D')
                u4 = Unit(size, x, y, 'C')
            new_units += [u1,u2,u3,u4]
        
        self.iterate(new_units)
        
    def draw(self, surface):
        for i,unit in enumerate(self.units):
            unit.draw(surface)
            if i == len(self.units)-1:
                break
            else:
                pg.draw.line(surface, white, self.units[i].points[3], self.units[i+1].points[0])
            pg.display.flip()
            clock.tick(fps)

def main():
    running = True
    test = Hilbert(6)
    test.draw(screen)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.flip()
        clock.tick(fps)
        
main()
pg.quit()
