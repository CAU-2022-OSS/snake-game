import pygame as pg

TITLE = "Snake Game"
WIDTH = 1280
HEIGHT = 960
FPS = 60
FONT_NAME = 'arial'
STATIC_PATH = "../static/"

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

KEY_DIRECTION1 = {
    pg.K_w: 'Nw',
    pg.K_s: 'Ss',
    pg.K_a: 'Wa',
    pg.K_d: 'Ed',
}

KEY_DIRECTION2 = {
    pg.K_UP: 'N',
    pg.K_DOWN: 'S',
    pg.K_LEFT: 'W',
    pg.K_RIGHT: 'E',
}