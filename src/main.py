import pygame as pg
import time
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

    def quit_game(self):
        self.running=False
        pg.quit()


    def wait_for_key(self):
        #waiting = True
        while self.running:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key==pg.K_ESCAPE:
                        return 1.5
                    else:
                        return 1
                elif event.type == pg.MOUSEBUTTONUP:
                    return 2
        

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)


    def show_menu_screen(self):
        print("menu screen")
        self.screen.fill(BGCOLOR)
        menu=[]
        #draw.rect and draw_text will be replaced by image load
        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4,160,40],2)
        self.draw_text("play",22,WHITE,WIDTH/2,HEIGHT/4)
        menu.append([WIDTH/2.5, HEIGHT/4, 160,40, self.show_game_screen])

        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4 + 50,160,40],2)
        self.draw_text("load",22,WHITE,WIDTH/2,HEIGHT/4 + 50)
        menu.append([WIDTH/2.5, HEIGHT/4 + 50, 160,40, self.load])

        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4 + 100,160,40],2)
        self.draw_text("ranking",22,WHITE,WIDTH/2,HEIGHT/4 + 100)
        menu.append([WIDTH/2.5, HEIGHT/4 +100, 160,40, self.ranking])

        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4 + 150,160,40],2)
        self.draw_text("exit",22,WHITE,WIDTH/2,HEIGHT/4 +150)
        menu.append([WIDTH/2.5, HEIGHT/4 +150, 160,40, self.quit_game])

        pg.display.flip()
        while self.running:
            key = self.wait_for_key()
            if key==2:
                mouse=pg.mouse.get_pos()
                print(mouse[0], mouse[1])
                for i in menu:
                    if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                        i[4]()
                        break

    def load(self):
        #loading game value
        print("load")
        self.screen.fill(BGCOLOR)
        self.draw_text("loading...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.show_game_screen()
    
    def ranking(self):
        #loading ranking
        print("rank")
        self.screen.fill(BGCOLOR)
        menu=[]
        self.draw_text("ranking...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.draw.rect(self.screen, WHITE, [WIDTH-130,HEIGHT/10 + 40,130,40],2)
        self.draw_text("menu",22,WHITE,WIDTH-50,HEIGHT/10 + 40)
        menu.append([WIDTH-130, HEIGHT/10 +40, 130,40, self.show_menu_screen])
        pg.display.flip()
        while self.running:
            key = self.wait_for_key()
            if key==1.5:
                self.quit_game()
                break
            elif key==2:
                mouse=pg.mouse.get_pos()
                for i in menu:
                    if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                        i[4]()
                        break

    def show_game_screen(self):
        print("game")
        self.screen.fill(BGCOLOR)
        self.draw_text("game screen", 48, WHITE, WIDTH/2, HEIGHT/4)
        #load some data...
        pg.display.flip()
        while self.running:
            key = self.wait_for_key()
            if key==1:
                self.show_game_screen()
                break
            elif key==1.5:
                #pause
                self.show_game_menu_screen()
                break
    
    def show_game_menu_screen(self):
        print("game menu")
        self.screen.fill(BGCOLOR)
        menu=[]
        #draw.rect and draw_text will be replaced by image load
        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4,160,40],2)
        self.draw_text("resume",22,WHITE,WIDTH/2,HEIGHT/4)
        menu.append([WIDTH/2.5, HEIGHT/4, 160,40, self.show_game_screen])

        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4 + 50,160,40],2)
        self.draw_text("restart",22,WHITE,WIDTH/2,HEIGHT/4 + 50)
        menu.append([WIDTH/2.5, HEIGHT/4 + 50, 160,40, self.show_game_screen])

        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4 + 100,160,40],2)
        self.draw_text("save",22,WHITE,WIDTH/2,HEIGHT/4 + 100)
        menu.append([WIDTH/2.5, HEIGHT/4 +100, 160,40, self.save])

        pg.draw.rect(self.screen, WHITE, [WIDTH/2.5,HEIGHT/4 + 150,160,40],2)
        self.draw_text("exit",22,WHITE,WIDTH/2,HEIGHT/4 +150)
        menu.append([WIDTH/2.5, HEIGHT/4 +150, 160,40, self.exit])

        pg.display.flip()
        while self.running:
            key=self.wait_for_key()
            if key==2:
                mouse=pg.mouse.get_pos()
                for i in menu:
                    if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                        i[4]()
                        break

    def save(self):
        #save game value
        print("save")
        self.screen.fill(BGCOLOR)
        self.draw_text("save game value...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.show_menu_screen()

    def exit(self):
        #reset game value
        print("exit")
        self.screen.fill(BGCOLOR)
        self.draw_text("exit...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.show_menu_screen()


window = Window()
window.show_menu_screen()

