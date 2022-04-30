import pygame as pg
import time
from settings import *
from datetime import datetime
from datetime import timedelta
import random


class Window:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font(FONT_NAME)
        self.play=False # if it has been played or not
        self.saved=False # if there exists saved data or not
        self.rank=[]

    def quit_game(self):
        self.running=False
        pg.quit()

    def draw_text(self, text, size, color, x, y, fontName=''):
        if fontName == '':
            font = pg.font.Font(self.font_name, size)
        else:
            font = pg.font.Font(fontName, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

    # main menu screen
    def show_menu_screen(self, player=None, apple=None):
        # drawing
        background=pg.image.load(STATIC_PATH+"image/background.png")
        background_img=pg.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background_img, (0,0))
        menu_img=pg.image.load(STATIC_PATH+"image/menu.png")
        self.screen.blit(menu_img,(WIDTH/3,HEIGHT/4))

        menu=[] # save each menu button image location
        menu.append([WIDTH/2.5, HEIGHT/4+100, 300,40, self.show_game_screen]) # PLAY
        menu.append([WIDTH/2.5, HEIGHT/4 + 176, 300,40, self.load]) # LOAD
        menu.append([WIDTH/2.5, HEIGHT/4 +250, 300,40, self.ranking]) # RANKING
        menu.append([WIDTH/2.5, HEIGHT/4 +326, 300,40, self.quit_game]) # EXIT

        pg.display.flip()

        # wait for user's interaction
        while self.running:
            for event in pg.event.get():
                if event.type==pg.MOUSEBUTTONUP:
                    mouse=pg.mouse.get_pos()
                    for i in menu:
                        if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                            if i[4]==self.load or i[4]==self.ranking:
                                i[4](player, apple) # load or ranking - needs player, apple info
                            else:
                                i[4]() # else - do not need any info
                            break

    # loading screen
    def load(self, player=None, apple=None):
        # drawing
        background=pg.image.load(STATIC_PATH+"image/background.png")
        background_img=pg.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background_img, (0,0))

        # loading previous game value
        if self.saved==True:
            self.draw_text("loading game...", 25, BLACK, WIDTH/2, HEIGHT/3+70)
            pg.display.flip()
            time.sleep(1)
            # start game
            self.show_game_screen(player, apple)
        else: # if there's no saved game data
            back_button=pg.image.load(STATIC_PATH+"image/back_button.png")
            self.screen.blit(back_button,(WIDTH-200,HEIGHT/10+40))
            menu=[WIDTH-210, HEIGHT/10 +30, 100,100, self.show_menu_screen] # save back button image location
            self.draw_text("There's no saved game data that can be loading", 25, BLACK, WIDTH/2, HEIGHT/3+70)
            pg.display.flip()
            # wait for user's interaction
            while self.running:
                for event in pg.event.get():
                    if event.type==pg.MOUSEBUTTONUP:
                        mouse=pg.mouse.get_pos()
                        if menu[2] + menu[0] > mouse[0] > menu[0] and menu[1] + menu[3] > mouse[1] > menu[1] and menu[4]!=None:
                            self.show_menu_screen() # go back to menu screen
                            break
            

    # ranking screen
    def ranking(self, player=None, apple=None):
        # drawing
        background=pg.image.load(STATIC_PATH+"image/background.png")
        background_img=pg.transform.scale(background, (WIDTH, HEIGHT))
        self.screen.blit(background_img, (0,0))

        rank_background_img=pg.image.load(STATIC_PATH+"image/ranking_board.png")
        back_button=pg.image.load(STATIC_PATH+"image/back_button.png")
        self.screen.blit(rank_background_img,(WIDTH/4-30,HEIGHT/5))
        self.screen.blit(back_button,(WIDTH-200,HEIGHT/10+40))

        menu=[] # save back button image location
        menu.append([WIDTH-210, HEIGHT/10 +30, 100,100, self.show_menu_screen])

        # loading rank data
        if len(self.rank)>0:
            for i in range(len(self.rank)):
                self.draw_text(str(i+1),22,BLACK,WIDTH/4+60, HEIGHT/3+(30*(i+1))) # rank
                self.draw_text(str(self.rank[i][0]),22,BLACK,WIDTH/4 + 100,HEIGHT/3+(30*(i+1))) # name
                self.draw_text(str(self.rank[i][1]),22,BLACK,WIDTH*3/4-50,HEIGHT/3+(30*(i+1))) # score
                print(self.rank)
        else: # if there's no saved record
            self.draw_text("There are no records saved yet", 22, BLACK, WIDTH/2+10, HEIGHT/3+70)

        pg.display.flip()

        # wait for user's interaction
        while self.running:
            for event in pg.event.get():
                if event.type==pg.MOUSEBUTTONUP:
                    mouse=pg.mouse.get_pos()
                    for i in menu:
                        if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                            self.show_menu_screen(player, apple)
                            break

    # game screen
    def show_game_screen(self, player=None, apple=None):
        last_moved_time = datetime.now()

        # if it is new game then make new object
        if player==None:
            player = Snake() # new player
            apple = Apple()
            self.played=True
        
        # game running
        while self.running:
            # drawing
            self.clock.tick(FPS)
            background_img = pg.image.load(STATIC_PATH+"image/background.png")
            background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
            self.screen.blit(background_img, (0,0))
            
            gameboard_img = pg.image.load(STATIC_PATH+"image/game_board.png")
            gameboard_img = pg.transform.scale(gameboard_img, (800, 800))
            self.screen.blit(gameboard_img, (45,85))
            
            logo_img = pg.image.load(STATIC_PATH+"image/logo.png")
            logo_img = pg.transform.scale(logo_img, (303, 235))
            self.screen.blit(logo_img, (880,200))
     
            # get user's key interaction
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
            
            # event) get apple
            if player.positions[0] == apple.position:
                player.grow()    
                # apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                apple.position = (random.randint(5, 35), random.randint(10, 40))
                if apple.position in player.positions: #  if new apple's position is overlaps with snake
                    apple.position = (random.randint(5, 35), random.randint(10, 40)) # repositioning
                player.point = player.point + 1 #  a point up when snake ate an apple
                
            # event) collision with wall
            if player.positions[0][0] < 5 or player.positions[0][0] > 42 or player.positions[0][1] < 3 or player.positions[0][1] > 40:
                self.game_over_screen(player, apple)
                break
            
            # event) collision with itself
            if player.positions[0] in player.positions[1:]:
                self.game_over_screen(player, apple)
                break
                
            player.draw(self.screen)
            apple.draw(self.screen)
            self.draw_text(str(player.point), 200, BLACK, 1050, 500, '../static/font/poxel.ttf')
            pg.display.update()
    
    def text_box(self):
        font = pg.font.Font('../static/font/poxel.ttf', 32)
        clock = pg.time.Clock()
        input_box = pg.Rect(564, 539, 184, 44)
        active = True
        text = ''
        done = False

        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    
                if event.type == pg.MOUSEBUTTONUP:
                    mouse=pg.mouse.get_pos()
                    print(mouse)
                    if 680 > mouse[0] > 600 and 653 > mouse[1] > 605:
                        print(text)
                        return text

                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            print(text)
                            return text
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            text += event.unicode
                            if len(text) > 7:
                                return text[0:7]

            #  Render the current text.
            txt_surface = font.render(text, True, BLACK)
            #  Blit the text.
            self.screen.blit(txt_surface, (568, 544))

            pg.display.flip()
            clock.tick(30)
    
    # game over screen
    def game_over_screen(self, player, apple):
        # drawing
        gameoverback_img = pg.image.load(STATIC_PATH+"image/game_over_back.png")
        gameoverback_img = pg.transform.scale(gameoverback_img, (WIDTH, HEIGHT))
        self.screen.blit(gameoverback_img, (0,0))

        gameover_img = pg.image.load(STATIC_PATH+"image/game_over.png")
        gameover_img = pg.transform.scale(gameover_img, (500, 500))
        self.screen.blit(gameover_img, (390,230))

        self.draw_text(str(player.point), 200, BLACK, 640, 330, '../static/font/poxel.ttf') # display user's points
        
        pg.display.flip()

        # wait for user's interaction
        while self.running:
            player.user_name = self.text_box()
            self.saved=False
            self.rank.append((player.user_name, player.point))
            self.rank.sort(key=lambda x:x[1], reverse=True)
            if len(self.rank)>10:
                self.rank=self.rank[:10]
            player.initialize()
            apple.initialize()
            self.show_menu_screen()
            break
        
        
    # game menu screen
    def show_game_menu_screen(self,player,apple):
        # drawing
        gameoverback_img = pg.image.load(STATIC_PATH+"image/game_over_back.png")
        gameoverback_img = pg.transform.scale(gameoverback_img, (WIDTH, HEIGHT))
        self.screen.blit(gameoverback_img, (0,0))
        
        background_img=pg.image.load(STATIC_PATH+"image/game_menu.png")
        self.screen.blit(background_img,(WIDTH/3,HEIGHT/4))
        
        menu=[] # save menu image location
        menu.append([WIDTH/2.5, HEIGHT/4+100, 300,40, 'resume']) # RESUME
        menu.append([WIDTH/2.5, HEIGHT/4 + 176, 300,40, self.show_game_screen]) # RESTART
        menu.append([WIDTH/2.5, HEIGHT/4 +250, 300,40, self.save]) # SAVE
        menu.append([WIDTH/2.5, HEIGHT/4 +326, 300,40, self.exit]) # EXIT

        pg.display.flip()

        # wait for user's interaction
        while self.running:
            for event in pg.event.get():
                if event.type==pg.MOUSEBUTTONUP:
                    mouse=pg.mouse.get_pos()
                    for i in menu:
                        if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                            if i[4]==self.save:
                                i[4](player,apple)
                            elif i[4]=='resume':
                                self.saved=True
                                self.show_game_screen(player, apple)
                                self.saved=False
                            i[4]()
                            break

    def save(self,player=None,apple=None):
        self.saved=True
        self.show_menu_screen(player,apple)

    def exit(self):
        self.saved=False
        self.show_menu_screen()

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

window = Window()
window.show_menu_screen()