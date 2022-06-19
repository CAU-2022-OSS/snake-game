import pygame as pg
import time
import random
from settings import *
from datetime import datetime
from datetime import timedelta
from Element import Apple, dualApple, Snake, SnakeArrow, SnakeWasd
import re

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
        pg.mixer.init()
        pg.mixer.music.load('../static/snake_music.mp3')
        pg.mixer.music.play()
        pg.mixer.music.set_volume(0.5)

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
        menu_img=pg.image.load(STATIC_PATH+"image/v2_menu.png")
        self.screen.blit(menu_img,(WIDTH/3,HEIGHT/4))

        menu=[] # save each menu button image location
        menu.append([WIDTH/2.5, HEIGHT/4+75, 300,40, self.show_single_game_screen]) # SINGLE PLAY
        menu.append([WIDTH/2.5, HEIGHT/4+130, 300,40, self.show_dual_game_screen]) #DUAL PLAY
        menu.append([WIDTH/2.5, HEIGHT/4+185, 300,40, self.show_automode_screen]) #AUTO PLAY
        menu.append([WIDTH/2.5, HEIGHT/4+245, 300,40, self.load]) # LOAD
        menu.append([WIDTH/2.5, HEIGHT/4+300, 300,40, self.ranking]) # RANKING
        menu.append([WIDTH/2.5, HEIGHT/4+355, 300,40, self.quit_game]) # EXIT

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
            self.show_single_game_screen(player, apple)
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
    def show_single_game_screen(self, player=None, apple=None):
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
                    if event.key in KEY_DIRECTION2:
                        player.direction = KEY_DIRECTION2[event.key]
                    elif event.key==pg.K_ESCAPE:
                        self.show_game_menu_screen(player, apple)

            if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
                player.move()
                last_moved_time = datetime.now()

            # event) get apple
            if player.positions[0] == apple.position:
                player.grow()
                # apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                apple.position = (random.randint(5, 35), random.randint(10, 40))
                while(apple.position in player.positions): #  while new apple's position overlaps with snake
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

    def show_dual_game_screen(self, player1=None, player2=None, apple1=None, apple2=None):
        last_moved_time = datetime.now()

        # if it is new game then make new object
        if player1==None and player2==None:
            player1 = SnakeWasd() # new player1
            player2 = SnakeArrow() # new player2
            apple1 = dualApple((random.randint(12, 52), random.randint(3, 81)))
            apple2 = dualApple((random.randint(12, 52), random.randint(3, 81)))
            self.played=True

        appleList = [apple1, apple2]
        # game running
        while self.running:
            # drawing
            self.clock.tick(FPS)
            background_img = pg.image.load(STATIC_PATH+"image/v2_dp_bg.png")
            background_img = pg.transform.scale(background_img, (WIDTH, HEIGHT))
            self.screen.blit(background_img, (0,0))

            # get user's key interaction
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key in KEY_DIRECTION1:
                        player1.direction = KEY_DIRECTION1[event.key]
                    elif event.key in KEY_DIRECTION2:
                        player2.direction = KEY_DIRECTION2[event.key]
                    elif event.key==pg.K_ESCAPE:
                        self.dual_game_menu_screen(player1, player2, apple1, apple2)

            if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
                player1.move()
                player2.move()
                last_moved_time = datetime.now()

            # event) get apple
            for i in appleList:
                if player1.positions[0] == i.position:
                    player1.grow()
                    # apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                    i.position = (random.randint(12, 51), random.randint(3, 81))
                    while(i.position in (player1.positions, player2.positions)): #  while new apple's position overlaps with snake
                        i.position = (random.randint(12, 51), random.randint(3, 81)) # repositioning
                    player1.point = player1.point + 1 #  a point up when snake ate an apple
                elif player2.positions[0]  == i.position:
                    player2.grow()
                    # apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                    i.position = (random.randint(12, 51), random.randint(3, 81))
                    while(i.position in (player1.positions, player2.positions)): #  while new apple's position overlaps with snake
                        i.position = (random.randint(12, 51), random.randint(3, 81)) # repositioning
                    player2.point = player2.point + 1 #  a point up when snake ate an apple


            # event) collision with wall
            if (player1.positions[0][0] < 12 or
                player1.positions[0][0] > 51 or
                player1.positions[0][1] < 3 or
                player1.positions[0][1] > 81):
                player1.is_dead = 1
                self.dual_game_over_screen(player1, player2, apple1, apple2)
                break
            if (player2.positions[0][0] < 12 or
                player2.positions[0][0] > 51 or
                player2.positions[0][1] < 3 or
                player2.positions[0][1] > 81):
                player2.is_dead = 1
                self.dual_game_over_screen(player1, player2, apple1, apple2)
                break

            # event) collision with itself
            if player1.positions[0] in player1.positions[1:]:
                player1.is_dead = 1
                self.dual_game_over_screen(player1, player2, apple1, apple2)
                break
            if player2.positions[0] in player2.positions[1:]:
                player2.is_dead = 1
                self.dual_game_over_screen(player1, player2, apple1, apple2)
                break

            # event) collision each other
            if player1.positions[0] in player2.positions[0:]: # player1 is dead
                player1.is_dead = 1
                self.dual_game_over_screen(player1, player2, apple1, apple2)
                break
            if player2.positions[0] in player1.positions[0:]: # player2 is dead
                player2.is_dead = 1
                self.dual_game_over_screen(player1, player2, apple1, apple2)
                break

            player1.draw(self.screen)
            player2.draw(self.screen)
            apple1.draw(self.screen)
            apple2.draw(self.screen)
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
                    if 680 > mouse[0] > 600 and 653 > mouse[1] > 605:
                        return text

                if event.type == pg.KEYDOWN:
                    if active:
                        if event.key == pg.K_RETURN:
                            return text
                        elif event.key == pg.K_BACKSPACE:
                            text = text[:-1]
                        elif re.match("[a-zA-Z0-9]", event.unicode): # allow only english and number
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

    def dual_game_over_screen(self, player1, player2, apple1, apple2):
        player1_win_img = pg.image.load(STATIC_PATH+"image/v2_dp_p1_win.png")
        player1_win_img = pg.transform.scale(player1_win_img, (WIDTH, HEIGHT))

        player2_win_img = pg.image.load(STATIC_PATH+"image/v2_dp_p2_win_bg.png")
        player2_win_img = pg.transform.scale(player2_win_img, (WIDTH, HEIGHT))

        if player2.is_dead == 1:
            player2.is_dead = 0
            self.screen.blit(player1_win_img, (0,0))
        if player1.is_dead == 1:
            player1.is_dead = 0
            self.screen.blit(player2_win_img, (0,0))

        pg.display.flip()

        while self.running:
            player1.initialize()
            player2.initialize()
            apple1.initialize()
            apple2.initialize()
            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
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
        menu.append([WIDTH/2.5, HEIGHT/4 + 100, 300,40, 'resume']) # RESUME
        menu.append([WIDTH/2.5, HEIGHT/4 + 176, 300,40, self.show_single_game_screen]) # RESTART
        menu.append([WIDTH/2.5, HEIGHT/4 + 250, 300,40, self.save]) # SAVE
        menu.append([WIDTH/2.5, HEIGHT/4 + 326, 300,40, self.exit]) # EXIT

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
                                self.show_single_game_screen(player, apple)
                                self.saved=False
                            i[4]()
                            break

    def dual_game_menu_screen(self, player1, player2, apple1, apple2):
        pause_img = pg.image.load(STATIC_PATH+"image/v2_dp_pause_bg.png")
        pause_img = pg.transform.scale(pause_img, (WIDTH, HEIGHT))
        self.screen.blit(pause_img, (0,0))

        menu=[] # save menu image location
        menu.append([WIDTH/2.5, HEIGHT/4 + 100, 300,60, 'resume']) # RESUME
        menu.append([WIDTH/2.5, HEIGHT/4 + 200, 300,60, self.show_dual_game_screen]) # RESTART
        menu.append([WIDTH/2.5, HEIGHT/4 +300, 300,60, self.exit]) # EXIT

        pg.display.flip()

        # wait for user's interaction
        while self.running:
            for event in pg.event.get():
                if event.type==pg.MOUSEBUTTONUP:
                    mouse=pg.mouse.get_pos()
                    for i in menu:
                        if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                            if i[4]=='resume':
                                self.saved=True
                                self.show_dual_game_screen(player1, player2, apple1, apple2)
                                self.saved=False
                            i[4]()
                            break

    def show_automode_screen(self, player=None, apple=None):
        #self.show_game_screen(player, apple)
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
                    #if event.key in KEY_DIRECTION:
                    #    player.direction = KEY_DIRECTION[event.key]
                    if event.key==pg.K_ESCAPE:
                        self.show_automode_game_menu_screen(player, apple)

            if timedelta(seconds=0.01) <= datetime.now() - last_moved_time:
                if player.direction!='':
                    self.auto_move(player, apple)
                else:
                    player.direction='N'
                    player.move()
                last_moved_time = datetime.now()

            # event) get apple
            if player.positions[0] == apple.position:
                cnt = 0
                player.grow()
                # apple.position = (random.randint(0, (HEIGHT/20)-20), random.randint(0, (WIDTH/20)-20))
                apple.position = (random.randint(5, 42), random.randint(3, 40))
                while(apple.position in player.positions): #  while new apple's position overlaps with snake
                    apple.position = (random.randint(5, 42), random.randint(3, 40)) # repositioning
                    cnt += 1
                    if cnt > 10000:
                        self.automode_game_over_screen(player, apple)
                        break
                player.point = player.point + 1 #  a point up when snake ate an apple

            # event) collision with wall
            if player.positions[0][0] < 5 or player.positions[0][0] > 42 or player.positions[0][1] < 3 or player.positions[0][1] > 40:
                self.automode_game_over_screen(player, apple)
                break

            # event) collision with itself
            if player.positions[0] in player.positions[1:]:
                self.automode_game_over_screen(player, apple)
                break

            player.draw(self.screen)
            apple.draw(self.screen)
            self.draw_text(str(player.point), 200, BLACK, 1050, 500, '../static/font/poxel.ttf')
            pg.display.update()


    global priority
    priority = [[0 for col in range(50)] for row in range(50)]
    cnt = 0
    for i in range(3, 41):
        priority[5][43 - i] = cnt
        cnt += 1
    for i in range(3, 41):
        for j in range(6, 43):
            priority[j if i % 2 == 1 else 48 - j][i] = cnt
            cnt += 1

    def auto_move(self, player=None, apple=None):
        global priority
        y = player.positions[0][0]
        x = player.positions[0][1]
        if x != 40 and y >= 6 and ((5, 40) not in player.positions[1:] or x + 2 < player.positions[len(player.positions) - 1][1]) and (x + 1 < apple.position[1] or x > apple.position[1] or (apple.position[0] == y and apple.position[1] - 1 == x)) :
            next = 'E'
        else:
            if priority[y][x] + 1 == priority[y][x + 1]: next = 'E'
            elif priority[y][x] + 1 == priority[y][x - 1]: next = 'W'
            elif priority[y][x] + 1 == priority[y + 1][x]: next = 'S'
            else: next = 'N'
        player.direction = next
        player.move()

    def show_automode_game_menu_screen(self,player,apple):
        # drawing
        gameoverback_img = pg.image.load(STATIC_PATH+"image/game_over_back.png")
        gameoverback_img = pg.transform.scale(gameoverback_img, (WIDTH, HEIGHT))
        self.screen.blit(gameoverback_img, (0,0))

        background_img=pg.image.load(STATIC_PATH+"image/v2_ap_game_menu.png")
        self.screen.blit(background_img,(WIDTH/3,HEIGHT/4))

        menu=[] # save menu image location
        menu.append([WIDTH/2.5, HEIGHT/4+100, 300,60, 'resume']) # RESUME
        menu.append([WIDTH/2.5, HEIGHT/4+200, 300,60, self.show_automode_screen]) # RESTART
        menu.append([WIDTH/2.5, HEIGHT/4+300, 300,60, self.exit]) # EXIT

        pg.display.flip()

        # wait for user's interaction
        while self.running:
            for event in pg.event.get():
                if event.type==pg.MOUSEBUTTONUP:
                    mouse=pg.mouse.get_pos()
                    for i in menu:
                        if i[2] + i[0] > mouse[0] > i[0] and i[1] + i[3] > mouse[1] > i[1] and i[4]!=None:
                            if i[4]=='resume':
                                self.saved=True
                                self.show_automode_screen(player, apple)
                                self.saved=False
                            i[4]()
                            break


    def automode_game_over_screen(self, player, apple):
            # drawing
            gameoverback_img = pg.image.load(STATIC_PATH+"image/game_over_back.png")
            gameoverback_img = pg.transform.scale(gameoverback_img, (WIDTH, HEIGHT))
            self.screen.blit(gameoverback_img, (0,0))

            gameover_img = pg.image.load(STATIC_PATH+"image/v2_ap_game_over.png")
            gameover_img = pg.transform.scale(gameover_img, (500, 500))
            self.screen.blit(gameover_img, (390,230))
            self.draw_text(str(player.point), 200, BLACK, 640, 330, '../static/font/poxel.ttf') # display user's points

            pg.display.flip()

            # wait for user's interaction
            while self.running:
                for event in pg.event.get():
                    if event.type==pg.MOUSEBUTTONUP:
                        mouse=pg.mouse.get_pos()
                        if 680 > mouse[0] > 590 and 658 > mouse[1] > 608:
                            self.saved=False
                            player.initialize()
                            apple.initialize()
                            self.show_menu_screen()
                            break

    def save(self,player=None,apple=None):
        self.saved=True
        self.show_menu_screen(player,apple)

    def exit(self):
        self.saved=False
        self.show_menu_screen()
