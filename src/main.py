import pygame as pg
from settings import *

cauLogo = pg.image.load("../static/image/cau.bmp")

class Window:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)

    
    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    waiting = False
    

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def show_menu_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("menu screen", 22, WHITE, WIDTH/2, HEIGHT/4)
        self.screen.blit(cauLogo, [ WIDTH/2, HEIGHT/2 ] )
        pg.display.flip()
        self.wait_for_key()
        self.show_game_screen()


    def show_game_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text("game screen", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        self.wait_for_key()
        self.show_menu_screen()
    


window = Window()
window.show_menu_screen()

pg.quit()

