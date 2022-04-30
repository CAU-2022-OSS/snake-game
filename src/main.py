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
        self.saved=False #if there exists saved data or not
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
        background_img=pg.image.load("../static/image/menu.png")
        self.screen.fill(BGCOLOR)
        menu=[]
        #draw.rect and draw_text will be replaced by image load
        self.screen.blit(background_img,(WIDTH/3,HEIGHT/4))
        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4+100,300,40],2)
        #PLAY
        menu.append([WIDTH/2.5, HEIGHT/4+100, 300,40, self.show_game_screen])

        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4 + 176,300,40],2)
        #LOAD
        menu.append([WIDTH/2.5, HEIGHT/4 + 176, 300,40, self.load])

        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4 + 250,300,40],2)
        #RANKING
        menu.append([WIDTH/2.5, HEIGHT/4 +250, 300,40, self.ranking])

        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4 + 326,300,40],2)
        #EXIT
        menu.append([WIDTH/2.5, HEIGHT/4 +326, 300,40, self.quit_game])

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
        #self.draw_text("loading...", 48, WHITE, WIDTH/2, HEIGHT/4)
        if self.saved==True:
            self.draw_text("loading game...", 30, WHITE, WIDTH/2, HEIGHT/4)
            self.draw_text("latest saved data", 30, WHITE, WIDTH/2, HEIGHT/4+50)
            tmp="user name : "+player.user_name+" score : "+str(player.point)
            self.draw_text(tmp, 30, WHITE, WIDTH/2, HEIGHT/4+100)
            #print("load game", player.user_name, player.point, player.positions)
            pg.display.flip()
            time.sleep(1)
            self.show_game_screen(player, apple)
        else:
            back_button=pg.image.load("../static/image/back_button.png")
            self.screen.blit(back_button,(WIDTH-200,HEIGHT/10+40))
            menu=[]
            #pg.draw.rect(self.screen, BLACK, [WIDTH-210,HEIGHT/10 + 30,100,100],2)
            #self.draw_text("<-",32,RED,WIDTH-50,HEIGHT/10 + 40)
            menu.append([WIDTH-210, HEIGHT/10 +30, 100,100, self.show_menu_screen])
            self.draw_text("There's no saved game data that can be loading", 30, WHITE, WIDTH/2, HEIGHT/4)
            #print("you didn't saved data")
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
                            self.show_menu_screen()
                            break
            

    def ranking(self, player=None, apple=None):
        #loading ranking
        print("rank")
        background_img=pg.image.load("../static/image/ranking_board.png")
        back_button=pg.image.load("../static/image/back_button.png")
        self.screen.fill(BGCOLOR)
        self.screen.blit(background_img,(WIDTH/4,HEIGHT/5))
        self.screen.blit(back_button,(WIDTH-200,HEIGHT/10+40))
        menu=[]
        #pg.draw.rect(self.screen, BLACK, [WIDTH-210,HEIGHT/10 + 30,100,100],2)
        #self.draw_text("<-",32,RED,WIDTH-50,HEIGHT/10 + 40)
        menu.append([WIDTH-210, HEIGHT/10 +30, 100,100, self.show_menu_screen])
        for i in range(len(self.rank)):
            self.draw_text(str(self.rank[i][0]),22,BLACK,WIDTH/4 + 100,HEIGHT/3+(30*(i+1)))
            self.draw_text(str(self.rank[i][1]),22,BLACK,WIDTH*3/4,HEIGHT/3+(30*(i+1)))
            print(self.rank)
        if len(self.rank)==0:
            self.draw_text("There are no records saved yet", 22, BLACK, WIDTH/2, HEIGHT/3+30)
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
                        self.show_menu_screen(player, apple)
                        break

    def show_game_screen(self, player=None, apple=None):
        last_moved_time = datetime.now()
        if player==None:
            #need to input user name
            player = Snake() #new player
            apple = Apple()
            self.played=True
        
        #print("start game",player.user_name, player.point, player.positions)
        
        while self.running:
            self.clock.tick(FPS)
            background_img = pg.image.load("../static/image/background.png")
            background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
            self.screen.blit(background_img, (0,0))
            
            gameboard_img = pg.image.load("../static/image/game_board.png")
            gameboard_img = pg.transform.scale(gameboard_img, (800, 800))
            self.screen.blit(gameboard_img, (45,85))
            
            logo_img = pg.image.load("../static/image/logo.png")
            logo_img = pg.transform.scale(logo_img, (303, 235))
            self.screen.blit(logo_img, (880,200))
     
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
                #apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                apple.position = (random.randint(5, 35), random.randint(10, 40))
                if apple.position in player.positions: # apple의 position이 snake와 겹칠 시 다른 위치로
                    apple.position = (random.randint(5, 35), random.randint(10, 40))
                player.point = player.point + 1 # a point up when snake ate an apple
                
            if player.positions[0][0] < 5 or player.positions[0][0] > 42 or player.positions[0][1] < 3 or player.positions[0][1] > 40:
                #limit up, down, left and right
                print("player position..", player.user_name, player.point, player.positions)
                self.game_over_screen(player, apple)
                #self.show_game_menu_screen(player,apple)
                break
            
            if player.positions[0] in player.positions[1:]: # 스스로를 물면 게임 오버
                print("player position..", player.user_name, player.point, player.positions)
                self.game_over_screen(player, apple)
                #self.show_game_menu_screen(player,apple)
                break
                
            player.draw(self.screen)
            apple.draw(self.screen)
            self.draw_text(str(player.point), 200, BLACK, 1050, 500)
            pg.display.update()
    
    def game_over_screen(self, player, apple):
        print("game over")
        gameoverback_img = pg.image.load("../static/image/game_over_back.png")
        gameoverback_img = pg.transform.scale(gameoverback_img, (WIDTH, HEIGHT))
        self.screen.blit(gameoverback_img, (0,0))

        gameover_img = pg.image.load("../static/image/game_over.png")
        gameover_img = pg.transform.scale(gameover_img, (500, 500))
        self.screen.blit(gameover_img, (390,230))
        
        self.draw_text(str(player.point), 200, BLACK, 640, 330)
        
        pg.display.flip()
        while self.running:

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key==pg.K_ESCAPE:
                        print("escape", player.user_name, player.point, player.positions)
                        self.show_game_menu_screen(player, apple)
                        break
                    
        # 이름 입력 칸 미완성
        '''
        text1 = 'Name?'
        font1 = pg.font.Font('../static/font/poxel.ttf',21)
        img1 = font1.render(text1,True,BLACK)
         
        rect1 = img1.get_rect()
        rect1.topleft = (570,550)
        rect1.width = 182
        rect1.height = 43
        cursor1 = pg.Rect(rect1.topright,(3,rect1.height))
        print(cursor1)
        
        running = True
        
        pg.display.flip()
        while self.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
         
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_BACKSPACE:
                        if len(text1)> 0:
                            text1 = text1[:-1]
                            print("x")
         
                    #elif event.key == pg.K_g:
                    #    print(chr(12622))
                    #    text1 += chr(12622)
                    else:
                        text1 += event.unicode
                        print("o")
                    img1 = font1.render(text1,True,BLACK)
                    rect1.size = img1.get_size()
                    cursor1.topleft = rect1.topright
         
            #self.screen.fill(BLUE)
            self.screen.blit(img1,rect1)
            if time.time() % 1 > 0.5:
                pg.draw.rect(self.screen, BLACK, cursor1)
            pg.display.update()
         
        pg.quit()
        
        
        '''
        
        
        
    
    def show_game_menu_screen(self,player,apple):
        print("game menu")
        
        gameoverback_img = pg.image.load("../static/image/game_over_back.png")
        gameoverback_img = pg.transform.scale(gameoverback_img, (WIDTH, HEIGHT))
        self.screen.blit(gameoverback_img, (0,0))
        
        background_img=pg.image.load("../static/image/game_menu.png")
        #self.screen.fill(BGCOLOR)
        self.screen.blit(background_img,(WIDTH/3,HEIGHT/4))
        
        menu=[]
        #draw.rect and draw_text will be replaced by image load
        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4+100,300,40],2)
        #RESUME
        #menu.append([WIDTH/2.5, HEIGHT/4+100, 300,40, self.show_game_screen])
        menu.append([WIDTH/2.5, HEIGHT/4+100, 300,40, 'resume'])

        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4 + 176,300,40],2)
        #RESTART
        menu.append([WIDTH/2.5, HEIGHT/4 + 176, 300,40, self.show_game_screen])

        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4 + 250,300,40],2)
        #SAVE
        menu.append([WIDTH/2.5, HEIGHT/4 +250, 300,40, self.save])

        #pg.draw.rect(self.screen, BLACK, [WIDTH/2.5,HEIGHT/4 + 326,300,40],2)
        #EIXT
        menu.append([WIDTH/2.5, HEIGHT/4 +326, 300,40, self.exit])

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
                        elif i[4]=='resume':
                            print('resume')
                            self.saved=True
                            #self.load(player, apple)
                            self.show_game_screen(player, apple)
                            self.saved=False
                        i[4]()
                        break

    def save(self,player=None,apple=None):
        #save game value
        #print("save game", player.user_name, player.point, player.positions)
        #self.screen.fill(WHITE)
        #self.draw_text("save game value...", 48, BLACK, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.saved=True
        self.show_menu_screen(player,apple)

    def exit(self,player=None,apple=None):
        #reset game value
        #print("exit")
        #self.screen.fill(WHITE)
        #self.draw_text("exit...", 48, BLACK, WIDTH/2, HEIGHT/4)
        pg.display.flip()
        time.sleep(1)
        self.saved=False
        self.rank.append((player.user_name, player.point))
        self.rank.sort(key=lambda x:x[1], reverse=True)
        if len(self.rank)>10:
            self.rank=self.rank[:10]
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
        #self.positions = [(HEIGHT/20/2,WIDTH/20/2),((HEIGHT/20/2)+1,WIDTH/20/2),((HEIGHT/20/2)+2,WIDTH/20/2)]  # 뱀의 위치
        self.positions = [(22, 24),(23, 24),(24, 24)]  # 뱀의 위치
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
    def __init__(self, position=(random.randint(5, 35), random.randint(10, 40))):
        self.position = position
 
    def draw(self, screen):
        draw_dot(screen, "../static/image/apple.png", self.position)

    def initialize(self):
        self.position=(random.randint(3, 40), random.randint(5, 42))

window = Window()
window.show_menu_screen()