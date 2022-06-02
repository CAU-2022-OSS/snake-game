import random
import pygame as pg

from settings import *


def draw_dot(screen, img, pos, rec_size):
    block_img = pg.image.load(img)
    block_img.get_rect().size = (rec_size, rec_size)
    block_x, block_y = pos[1] * rec_size, pos[0] * rec_size

    screen.blit(block_img, (block_x, block_y))


class Snake:
    def __init__(self):
        self.positions = [(22, 24), (23, 24), (24, 24)]  #  snake's start position
        self.direction = ""
        self.user_name = "name"
        self.point = 0

    def draw(self, screen):
        draw_dot(screen, STATIC_PATH + "image/snake_head.png", self.positions[0], 20)
        for position in self.positions[1:]:
            draw_dot(screen, STATIC_PATH + "image/snake_body.png", position, 20)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == "N":
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == "S":
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == "W":
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == "E":
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == "N":
            self.positions.append((y - 1, x))
        elif self.direction == "S":
            self.positions.append((y + 1, x))
        elif self.direction == "W":
            self.positions.append((y, x - 1))
        elif self.direction == "E":
            self.positions.append((y, x + 1))

    def initialize(self):
        self.user_name = "name"
        self.point = 0
        self.position = [
            (HEIGHT / 20 / 2, WIDTH / 20 / 2),
            ((HEIGHT / 20 / 2) + 1, WIDTH / 20 / 2),
            ((HEIGHT / 20 / 2) + 2, WIDTH / 20 / 2),
        ]
        self.direction = ""
        pass


class SnakeArrow(Snake):  # control snake by Arrow key
    def __init__(self):
        self.positions = [(40, 74), (41, 74), (42, 74)]  #  snake's start position
        self.direction = ""
        self.user_name = "name"
        self.point = 0
        self.is_dead = 0

    def draw(self, screen):
        draw_dot(screen, STATIC_PATH + "image/v2_dp_p2_head.png", self.positions[0], 15)
        for position in self.positions[1:]:
            draw_dot(screen, STATIC_PATH + "image/v2_dp_p2_body.png", position, 15)

    def initialize(self):
        self.position = [
            (HEIGHT / 15 / 2, WIDTH / 15 / 2),
            ((HEIGHT / 15 / 2) + 1, WIDTH / 15 / 2),
            ((HEIGHT / 15 / 2) + 2, WIDTH / 15 / 2),
        ]
        super().initialize()


class SnakeWasd(Snake):  # control snake by wasd key
    def __init__(self):
        self.positions = [(20, 10), (19, 10), (18, 10)]  #  snake's start position
        self.direction = ""
        self.user_name = "name"
        self.point = 0
        self.is_dead = 0

    def draw(self, screen):
        draw_dot(screen, STATIC_PATH + "image/v2_dp_p1_head.png", self.positions[0], 15)
        for position in self.positions[1:]:
            draw_dot(screen, STATIC_PATH + "image/v2_dp_p1_body.png", position, 15)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == "Nw":
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == "Ss":
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == "Wa":
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == "Ed":
            self.positions = [(y, x + 1)] + self.positions[:-1]
        # print(self.positions)

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == "Nw":
            self.positions.append((y - 1, x))
        elif self.direction == "Ss":
            self.positions.append((y + 1, x))
        elif self.direction == "Wa":
            self.positions.append((y, x - 1))
        elif self.direction == "Ed":
            self.positions.append((y, x + 1))

    def initialize(self):
        self.position = [
            (HEIGHT / 15 / 2, WIDTH / 15 / 2),
            ((HEIGHT / 15 / 2) + 1, WIDTH / 15 / 2),
            ((HEIGHT / 15 / 2) + 2, WIDTH / 15 / 2),
        ]
        super().initialize()


class Apple:
    def __init__(self, position=(random.randint(5, 35), random.randint(10, 40))):
        self.position = position

    def draw(self, screen):
        draw_dot(screen, STATIC_PATH + "image/apple.png", self.position, 20)

    def initialize(self):
        self.position = (random.randint(12, 52), random.randint(3, 81))


class dualApple(Apple):
    def __init__(self, position=(random.randint(12, 52), random.randint(3, 81))):
        self.position = position

    def draw(self, screen):
        draw_dot(screen, STATIC_PATH + "image/v2_dp_apple.png", self.position, 15)
