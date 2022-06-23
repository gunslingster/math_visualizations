import pygame
import random
import numpy as np
import sys

black = (0,0,0)
white = (200,200,200)
red = (200, 0, 0)
width = 1200
height = 800
pygame.init()
screen = pygame.display.set_mode(size=(width,height))
clock = pygame.time.Clock()
screen.fill(black)

class Maze():
    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.num_rows = self.height // self.cell_size
        self.num_cols = self.width // self.cell_size
        self.num_cells = self.num_rows * self.num_cols
        self.links = []
        self.grid = [[i for i in range(self.num_cols)] for i in range(self.num_rows)]
        
    def draw_link(self,p1,p2):
            x1 = p1[0]
            x2 = p2[0]
            y1 = p1[1]
            y2 = p2[1]
            
            # Make link to the right
            if x2 > x1:
                # Set pixel locations
                px = (x1+1) * self.cell_size - 1
                py = y1 * self.cell_size + 1
                rect = pygame.Rect(px, py, 2, self.cell_size -2 )
                pygame.draw.rect(screen, black, rect)
                
            # Make link to the left
            if x2 < x1:
                px = (x2+1) * self.cell_size - 1
                py = y1 * self.cell_size + 1
                rect = pygame.Rect(px, py, 2, self.cell_size -2 )
                pygame.draw.rect(screen, black, rect)
                
            # Make link above
            if y2 < y1:
                py = (y2+1) * self.cell_size - 1
                px = x1 *self.cell_size + 1
                rect = pygame.Rect(px, py, self.cell_size-2, 2)
                pygame.draw.rect(screen, black, rect)
            
            # Make link below
            if y2 > y1:
                py = (y1+1) * self.cell_size - 1
                px = x1 * self.cell_size + 1
                rect = pygame.Rect(px, py, self.cell_size-2, 2)
                pygame.draw.rect(screen, black, rect)
                
            pygame.display.flip()
    
    def gen_links(self):
        """
        Will generate random links between points in the grid.
        Does not terminate until all points in the grid have been visited.
        Will add Tuples to self.links to represent a link between points.
        """
        stack = []
        visited = []
        num_visited = 0
            
        def check_visited(point):
            if point in visited:
                return True
            else:
                return False
        
        def find_unvisited_neighbors(cell):
            unvisited_neighbors = []
            x = cell[0]
            y = cell[1]
            NSEW = [(x-1,y), (x+1,y), (x,y+1), (x,y-1)]
            for elem in NSEW:
                if elem[0] < 0 or elem[0] >= self.num_cols or elem[1] < 0 or elem[1] >= self.num_rows:
                    continue
                else:
                    unvisited_neighbors.append(elem)
            unvisited_neighbors = [cell for cell in unvisited_neighbors if cell not in visited]
            return unvisited_neighbors
                    
        def test():
            for i in range(self.num_rows):
                for j in range(self.num_cols):
                    print(find_unvisited_neighbors((i,j)))
                    
        stack.append((0,0))
        curr_cell = stack[-1]
        while num_visited < self.num_cells:
            if not check_visited(curr_cell):
                visited.append(curr_cell)
                num_visited += 1
            paths = find_unvisited_neighbors(curr_cell)
            if paths != []:
                temp = curr_cell
                next_cell = random.choice(paths)
                self.links.append((temp, next_cell))
                #breakpoint()
                self.draw_link(temp, next_cell)
                curr_cell = next_cell
                stack.append(curr_cell)
            else:
                stack.pop()
                curr_cell = stack[-1]
                
    def draw_maze(self):
        for i in range(0, self.width, self.cell_size):
            for j in range(0, self.height, self.cell_size):
                rect = pygame.Rect(i, j, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, white, rect,1)
                pygame.display.flip()
                
class agent():
    def __init__(self, size,maze):
        self.size = size
        self.end = (maze.num_cols-1, maze.num_rows-1)
        self.maze = maze
        self.start = (0,0)
        self.position = self.start 
        self.distance = self.maze.cell_size
        self.moves = ['N', 'S', 'E', 'W']
        self.visited = []
        self.stack = []
    
        
    def draw_agent(self,position, draw_erase):
        x = (position[0] + 1) * self.maze.cell_size - self.maze.cell_size/2
        y = (position[1] + 1) * self.maze.cell_size - self.maze.cell_size/2
        if draw_erase == True:
            pygame.draw.circle(screen, red, (x,y), self.size)
        else:
            pygame.draw.circle(screen, black, (x,y), self.size)
        pygame.display.flip()
    
        
    def find_open_cells(self,cell):
        paths = [link for link in self.maze.links if cell in link]
        open_cells = []
        for path in paths:
            for cell_ in path:
                if cell_ != cell:
                    open_cells.append(cell_)
        return open_cells
            
    def move_agent(self):
        old_pos = self.position
        open_cells = self.find_open_cells(old_pos)
        new_pos = random.choice(open_cells)
        self.position = new_pos
        self.draw_agent(old_pos, False)
        self.draw_agent(new_pos, True)
        
    def solve(self):
        if self.position != self.end:
            self.move_agent()
            
    def solve_2(self):
        #breakpoint()
        if self.position != self.end:
            #print(self.position)
            self.visited.append(self.position)
            moves = self.find_open_cells(self.position)
            moves = [move for move in moves if move not in self.visited]
            #print(self.stack)
            # Check if agent has to backtrack
            if moves == []:
                old_pos = self.position
                new_pos = self.stack.pop()
                self.position = new_pos
                self.draw_agent(old_pos, False)
                self.draw_agent(new_pos, True)
            else:
                self.stack.append(self.position)
                old_pos = self.position
                new_pos = random.choice(moves)
                self.position = new_pos
                self.draw_agent(old_pos, False)
                self.draw_agent(new_pos, True)
                
class q_learning_agent():
    def __init__(self, size, maze):
        self.size = size
        self.maze = maze
        self.start = (0,0)
        self.position = self.start
        self.end = (maze.num_cols-1, maze.num_rows-1)
        self.Q = np.zeros((self.maze.num_rows*self.maze.num_cols, 4))
        self.reward = np.zeros((self.maze.num_rows, self.maze.num_cols))
        self.reward += -1
        self.eps = 0.2
        self.lr = 0.8
        self.gamma = 0.95
        self.reward[-1][-1] += 11
        self.NSEW = [0,1,2,3]
        
    def draw_agent(self,position, draw_erase):
        x = (position[0] + 1) * self.maze.cell_size - self.maze.cell_size/2
        y = (position[1] + 1) * self.maze.cell_size - self.maze.cell_size/2
        if draw_erase == True:
            pygame.draw.circle(screen, red, (x,y), self.size)
        else:
            pygame.draw.circle(screen, black, (x,y), self.size)
        pygame.display.flip()
    
    def find_open_cells(self,cell):
        paths = [link for link in self.maze.links if cell in link]
        open_cells = []
        for path in paths:
            for cell_ in path:
                if cell_ != cell:
                    open_cells.append(cell_)
        return open_cells
        
    def update(self):
        
        
        pass
    
    def draw(self):
        pass
            
            
def main():
    m = Maze(width, height, 20)
    m.draw_maze()
    m.gen_links()
    q_agent = q_learning_agent(5,m)
    print(q_agent.Q)
    print(q_agent.reward)
    actor = agent(3, m)
    running = True
    while running:
        actor.solve_2()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit(), sys.exit()
        clock.tick(2)
        
main()
