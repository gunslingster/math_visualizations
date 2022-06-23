import pygame
import random
import sys
import math
import pdb

red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
colors = [red, green, blue]
black = (0,0,0)
width = 1200
height = 800
FPS = 30
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode(size=(width,height))
screen.fill(black)
pygame.display.flip()

class vec_2d():
    def __init__(self, vx, vy):
        self.vx = vx
        self.vy = vy
        
    def add(self, other):
        return vec_2d(self.vx + other.vx, self.vy + other.vy)
    
    def dot(self, other):
        return self.vx*other.vx + self.vy*other.vy
    
    def normalize(self):
        mag = math.sqrt(self.vx**2 + self.vy**2)
        nx = self.vx/mag
        ny = self.vy/mag
        return vec_2d(nx,ny)
    
    def scale(self, factor):
        return vec_2d(factor*self.vx, factor*self.vy)
    
    
class Particle():
    def __init__(self, x = 0, y = 0, vel = 0, theta = 0, size = 10, color = red):
        self.x = x
        self.y = y 
        self.size = size
        self.theta = theta
        self.vx = vel * math.cos(math.radians(theta))
        self.vy = vel * math.sin(math.radians(theta))
        self.vel = vec_2d(self.vx, self.vy)
        self.color = color
        
    def update_pos(self):
        if self.x > width - self.size:
            self.x = 2*(width - self.size) - self.x
            self.vel.vx = -self.vel.vx
        elif self.x < self.size:
            self.x = 2*self.size - self.x
            self.vel.vx = -self.vel.vx
        if self.y > height - self.size:
            self.y = 2*(height - self.size) - self.y
            self.vel.vy = -self.vel.vy
        elif self.y < self.size:
            self.y = 2*self.size - self.y
            self.vel.vy = -self.vel.vy
        self.x += self.vel.vx/FPS
        self.y += self.vel.vy/FPS
        
            
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x,self.y), self.size)

def collision_test(p1,p2):
    dx = p2.x-p1.x
    dy = p2.y-p1.y
    dist = math.sqrt(dx**2 + dy**2)
    return dist <= (p1.size + p2.size)
           
def collide(p1,p2):
    nvx = p2.x-p1.x
    nvy = p2.y-p1.y
    nv = vec_2d(nvx,nvy)
    nv_unit = nv.normalize()
    tv_unit = vec_2d(-nv_unit.vy, nv_unit.vx)
    v1_i = p1.vel
    v2_i = p2.vel
    v1n = v1_i.dot(nv_unit)
    v1t = v1_i.dot(tv_unit)
    v2n = v2_i.dot(nv_unit)
    v2t = v2_i.dot(tv_unit)
    
    v1tf = v1t
    v2tf = v2t
    v1nf = (v1n*(p1.size-p2.size) + 2 * p2.size * v2n)/(p1.size + p2.size)
    v2nf = (v2n * (p2.size - p1.size) + 2*p1.size*v1n) / (p1.size + p2.size)
    v1nf = nv_unit.scale(v1nf)
    v2nf = nv_unit.scale(v2nf)
    v1tf = tv_unit.scale(v1tf)
    v2tf = tv_unit.scale(v2tf)
    
    v1f = v1nf.add(v1tf)
    v2f = v2nf.add(v2tf)
    p1.vel = v1f
    p2.vel = v2f
    p1.update_pos()
    p2.update_pos()
    
def gen_particles(num):
    particles = []
    for i in range(num):
        x = random.randrange(width)
        y = random.randrange(height)
        vel = random.randrange(200,400)
        theta = random.randrange(360)
        size =  random.randrange(10,50)
        color = random.choice(colors)
        p = Particle(x,y,vel,theta,size,color)
        particles.append(p)
    
    return particles
        

def main():
    running = True
    num_particles = 10
    particles = gen_particles(num_particles)
    for p in particles:
        p.draw()
    pygame.display.flip()
    while running:
        clock.tick(60)
        screen.fill(black)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit(), sys.exit()
        for i in range(len(particles)-1):
            for j in range(i+1, len(particles)):
                if collision_test(particles[i], particles[j]):
                    collide(particles[i], particles[j])
        for p in particles:
            p.update_pos()
            p.draw()
        pygame.display.flip()
       
main()
