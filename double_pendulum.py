import pygame as pg
import random
import math

# Setup and globals
pg.init()
width = 1200
height = 800
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
screen = pg.display.set_mode((width,height))
clock = pg.time.Clock()
pi = math.pi

# Initial state of both pendulums
g = 3
m1, m2 = 10, 3
l1, l2 = 200, 100
theta1, theta2 = pi/4, pi/6
vel1, vel2 = 0, 0
acc1, acc2 = 0, 0
x1, y1 = width//2 + l1 * math.sin(theta1), height//2 + l1 * math.cos(theta1)
x2, y2 = x1 + l2 * math.sin(theta2), y1 + l2 * math.cos(theta2)
history = []

def draw():
    pg.draw.line(screen, white, (width//2, height//2), (x1,y1))
    pg.draw.circle(screen, white, (x1,y1), m1)
    pg.draw.line(screen, white, (x1,y1), (x2,y2))    
    pg.draw.circle(screen, white, (x2,y2), m2)
    for i in range(len(history) - 1):
        pg.draw.line(screen, red, history[i], history[i+1])
    
def update():
    global g, acc1, acc2, vel1, vel2, theta1, theta2, x1, x2, y1, y2
    c1 = g * (2*m1 + m2) * math.sin(theta1)
    c2 = m2 * g * math.sin(theta1 - 2*theta2)
    c3 = 2 * math.sin(theta1 - theta2) * m2 * (vel2**2 * l2 + vel1**2 * l1 * math.cos(theta1 - theta2))
    den1 = l2 * (2 * m1 + m2  - m2 * math.cos(2 * theta1 - 2 * theta2))
    c4 = 2 * math.sin(theta1 - theta2)
    c5 = vel1**2 * l1 * (m1 + m2)
    c6 = g * (m1 + m2) * math.cos(theta1) 
    c7 = vel2**2 * l2 * m2 * math.cos(theta1 - theta2)
    den2 = l2 * (2 * m1 + m2 - m2 * math.cos(2 * theta1 - 2 * theta2))
    acc1 = (-c1 - c2 - c3) / den1
    acc2 = (c4 * (c5 + c6 + c7)) / den2
    vel1 += acc1
    vel2 += acc2
    vel1 *= 0.999
    vel2 *= 0.999
    theta1 += vel1
    theta2 += vel2
    x1, y1 = width//2 + l1 * math.sin(theta1), height//2 + l1 * math.cos(theta1)
    x2, y2 = x1 + l2 * math.sin(theta2), y1 + l2 * math.cos(theta2)
    history.append((x2,y2))
        
def main():
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        update()
        screen.fill(black)
        draw()
        pg.display.flip()
        clock.tick(30)

main()
pg.quit()
