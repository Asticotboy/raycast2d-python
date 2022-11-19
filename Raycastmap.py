import pygame
from pygame.locals import *
import math
import win32api

BLUE = (0,0,255)
RED = (255,0,0)
GREEN = (0,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
YELLOW = (255,255,0)

WIDTH = 7
HEIGHT = 4


class RaycastMap:
    def __init__(self, environnment, fov, xpos, ypos, angle):
        self.environnment = environnment
        self.fov = fov
        self.xpos = xpos
        self.ypos = ypos
        self.angle = angle
        self.speed =0.025

        self.range_distance = 200


        self.display = pygame.display.set_mode((WIDTH*100, HEIGHT*100))
        pygame.display.set_caption("RaycastMap by Asticotboy")

        self.clock = pygame.time.Clock()

        self.run = True

        self.keys_pressed = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
            "space": False
        }

    def line_coords(self, x,y,angle,lenght):
            return [x + math.cos(angle) * lenght , y + math.sin(angle) * lenght]

    def canMove(self, x, y):
            if self.environnment[int(y)][int(x)] == 2:
                self.run = False
                win32api.MessageBox(0, 'Bravo tu as gangé ! Ce n\'était pas si dur que ça !','Asticotboy')

            if self.environnment[int(y)][int(x)] != 1:
                return True           

            else:
                return False

    def handle_input(self):
            for e in pygame.event.get():
                if e.type == QUIT:
                    self.run = False
                if e.type == KEYDOWN:
                    if e.key == K_LEFT:
                        self.keys_pressed["left"] = True

                    if e.key == K_RIGHT:
                        self.keys_pressed["right"] = True

                    if e.key == K_UP:
                        self.keys_pressed["up"] = True

                    if e.key == K_DOWN:
                        self.keys_pressed["down"] = True

                    if e.key == K_SPACE:
                        self.keys_pressed["space"] = not self.keys_pressed["space"]

                if e.type == KEYUP:
                    if e.key == K_LEFT:
                        self.keys_pressed["left"] = False

                    if e.key == K_RIGHT:
                        self.keys_pressed["right"] = False

                    if e.key == K_UP:
                        self.keys_pressed["up"] = False

                    if e.key == K_DOWN:
                        self.keys_pressed["down"] = False
                    

    def update(self):
            if self.keys_pressed["left"]:
                self.angle -= 0.05
            if self.keys_pressed["right"]:
                self.angle += 0.05
            if self.keys_pressed["up"]:                
                next_x =self.xpos + math.cos(self.angle) * self.speed
                next_y = self.ypos + math.sin(self.angle) * self.speed
                if self.canMove(next_x, next_y):
                    self.xpos = next_x
                    self.ypos = next_y

            if self.keys_pressed["down"]:
                next_x =self.xpos - math.cos(self.angle) * self.speed
                next_y = self.ypos - math.sin(self.angle) * self.speed
                if self.canMove(next_x, next_y):
                    self.xpos = next_x
                    self.ypos = next_y

    def raycast(self):
        detail = 100
        angle = self.angle - math.radians(30)
        for f in range(self.fov):
            xpos, ypos = self.xpos, self.ypos
            for i in range(detail):
                x, y = self.line_coords(xpos*100, ypos*100, angle, self.range_distance/detail)

                try:
                    if self.environnment[int(y/100)][int(x/100)] != 1:
                        pygame.draw.line(self.display, RED, (self.xpos*100, self.ypos*100), (x, y), 10)
                    else:
                        break
                except:
                    break
                xpos, ypos = x/100, y/100
            angle += math.radians(1)

    def draw(self):
        while self.run:
            self.clock.tick(60)
            self.handle_input()
            self.update()

            self.display.fill(BLACK)

            self.raycast()
            if self.keys_pressed["space"]:
                pygame.draw.line(self.display, GREEN, (self.xpos*100, self.ypos*100), self.line_coords(self.xpos*100, self.ypos*100, self.angle-math.radians(30), self.range_distance), 10)
                pygame.draw.line(self.display, GREEN, (self.xpos*100, self.ypos*100), self.line_coords(self.xpos*100, self.ypos*100, self.angle+math.radians(30), self.range_distance), 10)
            

            for x in range(WIDTH):
                for y in range(HEIGHT):
                    if self.environnment[y][x] == 1:
                        pygame.draw.rect(self.display, WHITE, (x*100, y*100, x+100, y+100))
                    elif self.environnment[y][x] == 2:
                        pygame.draw.rect(self.display, YELLOW, (x*100, y*100, x+100, y+100))


            
            pygame.draw.circle(self.display, BLUE, (self.xpos*100, self.ypos*100), 10)
            

            pygame.display.update()


########### MAP GENERATOR ###########
environment = [
    [1,1,1,1,1,1,1],
    [1,0,0,0,0,0,2],
    [1,0,1,0,0,0,1],
    [1,1,1,1,1,1,1]
]

############  PLAYER CONFIGURATION  ########################
player_position = [1.5, 2.5]
range_distance = 200
angle = 0/math.pi
fov = 60
################## INSTANTIATE MAP   ############################
RaycastMap(environment, fov, player_position[0], player_position[1], angle).draw()