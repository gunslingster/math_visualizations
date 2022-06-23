import pygame as pg
import random
import math
pg.init()

width = 1200
height = 800 
screen = pg.display.set_mode((width, height))
black = (0,0,0)
white = (255,255,255)
grey = (100,100,100)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
orange = (255,165,0)
fps = 10
clock = pg.time.Clock()

def draw_grid(surface, spacing=20, color=grey):
    for i in range(surface.get_width()):
        pg.draw.line(surface, color, (i*spacing, 0), (i*spacing, surface.get_height()))
    for i in range(surface.get_height()):
        pg.draw.line(surface, color, (0, i*spacing), (surface.get_width(), i*spacing))

class cell():
    size = 20
    max_row = height//size
    max_col = width//size
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.index = (self.row,self.col)
        self.neighbors = [(row-1,col), (row+1,col), (row,col-1), (row,col+1), (row-1,col-1), (row-1,col+1), (row+1,col-1), (row+1,col+1)]
        self.neighbors = [x for x in self.neighbors if x[0]>=0 and x[0]<self.max_row and x[1]>=0 and x[1]<self.max_col]
        self.x = self.col * self.size
        self.y = self.row * self.size
        self.pos = (self.x, self.y)
        self.image = pg.Surface((self.size,self.size))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos
        self.living = False
        
    def draw(self):
        if self.living:
            self.image.fill(black)
        else:
            self.image.fill(white)
        screen.blit(self.image, self.rect)
    
    def isLiving(self):
        return self.living 
            
class cell_grid():
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.num_rows = int(self.height//self.cell_size)
        self.num_cols = int(self.width//self.cell_size)
        self.cells = {}
        self.buffer = {}
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.buffer[(i,j)] = False
        self.setup = True
        
    def generate_cells(self):
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                self.cells[(i,j)] = cell(i,j)
                
    def update(self):
        for cell in self.cells.values():
            living_neighbors = 0
            for neighbor in cell.neighbors:
                if self.cells[neighbor].isLiving():
                    living_neighbors += 1
            if cell.isLiving() and living_neighbors < 2:
                self.buffer[cell.index] = False
            if cell.isLiving() and living_neighbors > 3:
                self.buffer[cell.index] = False
            if not cell.isLiving() and living_neighbors == 3:
                self.buffer[cell.index] = True
        for cell in self.cells.values():
            cell.living = self.buffer[cell.index]
            

    def draw(self):
        for cell in self.cells.values():
            cell.draw()
        draw_grid(screen)

def main():
    running = True
    c = cell_grid(width,height,20)
    c.generate_cells()
    print(c.cells[(0,0)])
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    c.setup = False
            if c.setup:
                if event.type == pg.MOUSEBUTTONDOWN:
                    pos = pg.mouse.get_pos()
                    for cell in c.cells.values():
                        if cell.rect.collidepoint(pos):
                            c.buffer[cell.index] = True
                            cell.living = True
                c.draw()
                pg.display.flip()
        if not c.setup:
            c.update()
            c.draw()
            pg.display.flip()
            clock.tick(fps)
        
main()
pg.quit()
