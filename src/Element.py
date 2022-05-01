import pygame as pg
import random
from settings import *


def draw_dot(screen, img, pos):
    block_img = pg.image.load(img)
    block_img.get_rect().size = (20,20)
    block_x, block_y = pos[1]*20, pos[0]*20
    
    screen.blit(block_img, (block_x, block_y))


class Snake:
    def __init__(self):
        self.positions = [(22, 24),(23, 24),(24, 24)]  #  snake's start position
        self.direction = ''
        self.user_name = 'name'
        self.point = 0

    def draw(self, screen):
        draw_dot(screen, STATIC_PATH+"image/snake_head.png", self.positions[0])
        for position in self.positions[1:]: 
            draw_dot(screen, STATIC_PATH+"image/snake_body.png", position)
 
    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            self.positions = [(y-1, x)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y+1, x)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(y, x-1)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y, x+1)] + self.positions[:-1]
 
    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'N':
            self.positions.append((y-1, x))
        elif self.direction == 'S':
            self.positions.append((y+1, x))
        elif self.direction == 'W':
            self.positions.append((y, x-1))
        elif self.direction == 'C':
            self.positions.append((y, x+1))  

    def initialize(self):
        self.user_name='name'
        self.point=0
        self.position=[(HEIGHT/20/2,WIDTH/20/2),((HEIGHT/20/2)+1,WIDTH/20/2),((HEIGHT/20/2)+2,WIDTH/20/2)]
        self.direction=''
        pass


class Apple:
    def __init__(self, position=(random.randint(5, 35), random.randint(10, 40))):
        self.position = position
 
    def draw(self, screen):
        draw_dot(screen, STATIC_PATH+"image/apple.png", self.position)

    def initialize(self):
        self.position=(random.randint(3, 40), random.randint(5, 42))