import pygame as pg
import time
from settings import *
from datetime import datetime
from datetime import timedelta
import random

#cauLogo = pg.image.load("../static/image/cau.bmp")
class Window:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.play=False #if it has been played or not
        self.saved=False #if there exists savied data or not
        self.rank=[]

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


    def show_menu_screen(self, player=None, apple=None):
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
                        if i[4]==self.load or i[4]==self.ranking:
                            i[4](player, apple)
                        else:
                            i[4]()
                        break

    def load(self, player=None, apple=None):
        #loading game value
        self.screen.fill(BGCOLOR)
        self.draw_text("loading...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        if self.saved==True:
            print("load game", player.user_name, player.point, player.positions)
            self.show_game_screen(player, apple)
        else:
            print("you didn't saved data")
            self.show_game_screen()
    
    def ranking(self, player=None, apple=None):
        #loading ranking
        print("rank")
        self.screen.fill(BGCOLOR)
        menu=[]
        self.draw_text("ranking...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.draw.rect(self.screen, WHITE, [WIDTH-130,HEIGHT/10 + 40,130,40],2)
        self.draw_text("menu",22,WHITE,WIDTH-50,HEIGHT/10 + 40)
        menu.append([WIDTH-130, HEIGHT/10 +40, 130,40, self.show_menu_screen])
        pg.display.flip()
        print(self.rank)
        while self.running:
            key = self.wait_for_key()
            if key==1.5:
                self.quit_game()
                break
            elif key==2:
                mouse=pg.mouse.get_pos()
                for i in menu:
                    if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                        self.show_menu_screen(player, apple)
                        break

    def show_game_screen(self, player=None, apple=None):
        '''
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
        '''
        last_moved_time = datetime.now()
        if player==None:
            #need to input user name
            player = Snake() #new player
            apple = Apple()
            self.played=True
        
        print("start game",player.user_name, player.point, player.positions)
        
        while self.running:
            self.clock.tick(FPS)
            background_img = pg.image.load("../static/image/background.png")
            background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
            self.screen.blit(background_img, (0,0))
     
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key in KEY_DIRECTION:
                        player.direction = KEY_DIRECTION[event.key]
                    elif event.key==pg.K_ESCAPE:
                        print("escape", player.user_name, player.point, player.positions)
                        self.show_game_menu_screen(player, apple)
                        
                        
     
            if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
                player.move()
                last_moved_time = datetime.now()
            
            if player.positions[0] == apple.position:
                player.grow()    
                apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                player.point = player.point + 1 # a point up when snake ate an apple
            
            if player.positions[0] in player.positions[1:]:
                print("player position..", player.user_name, player.point, player.positions)
                self.show_game_menu_screen(player,apple)
                break
                
            player.draw(self.screen)
            apple.draw(self.screen)
            self.draw_text(str(player.point), 22, BLACK, 40, 0)
            pg.display.update()
    
    def show_game_menu_screen(self,player,apple):
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
                        if i[4]==self.exit or i[4]==self.save:
                            print(i[4])
                            i[4](player,apple)
                        i[4]()
                        break

    def save(self,player=None,apple=None):
        #save game value
        print("save game", player.user_name, player.point, player.positions)
        self.screen.fill(BGCOLOR)
        self.draw_text("save game value...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.saved=True
        self.show_menu_screen(player,apple)

    def exit(self,player=None,apple=None):
        #reset game value
        print("exit")
        self.screen.fill(BGCOLOR)
        self.draw_text("exit...", 48, WHITE, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.saved=False
        self.rank.append((player.user_name, player.point))
        player.initialize()
        apple.initialize()
        self.show_menu_screen()

 
KEY_DIRECTION = {
    pg.K_UP: 'N',
    pg.K_DOWN: 'S',
    pg.K_LEFT: 'W',
    pg.K_RIGHT: 'E',
}

def draw_dot(screen, img, pos):
    block_img = pg.image.load(img)
    block_img.get_rect().size = (20,20)
    block_x, block_y = pos[1]*20, pos[0]*20
    
    screen.blit(block_img, (block_x, block_y))
    
class Snake:
    def __init__(self):
        self.positions = [(HEIGHT/20/2,WIDTH/20/2),((HEIGHT/20/2)+1,WIDTH/20/2),((HEIGHT/20/2)+2,WIDTH/20/2)]  # 뱀의 위치
        self.direction = ''
        self.user_name = 'name'
        self.point = 0

    def draw(self, screen):
        draw_dot(screen, "../static/image/snake_head.png", self.positions[0])
        for position in self.positions[1:]: 
            draw_dot(screen, "../static/image/snake_body.png", position)
 
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
    def __init__(self, position=(10,10)):
        self.position = position
 
    def draw(self, screen):
        draw_dot(screen, "../static/image/apple.png", self.position)

    def initialize(self):
        self.position=(10,10)

window = Window()
window.show_menu_screen()