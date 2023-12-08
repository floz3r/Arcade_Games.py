#Importing required modules
import pygame
import random
import time


BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
TITLE_WHITE = ( 255, 200, 255)
LIGHT_GREEN = (0, 180, 0)
GREEN = (78, 255, 87)
YELLOW = (241, 255, 0)
BLUE = (80, 255, 239)
PURPLE = (203, 0, 255)
RED = (237, 28, 36)
ROCK = (54, 54, 54)


timer = 0
# adding font file
FONT = "fonts/space_invaders.ttf"
#Loading Alien images
AlienImages = {"image1_1" : "./images/enemy1_1.png",
               "image1_2" : "./images/enemy1_2.png",
               "image2_1" : "./images/enemy2_1.png",
               "image2_2" : "./images/enemy2_2.png",
               "image3_1" : "./images/enemy3_1.png",
               "image3_2" : "./images/enemy3_2.png"
              }
Alien1 = {1 : AlienImages["image1_1"], -1 : AlienImages["image1_2"]}
Alien2 = {1 : AlienImages["image2_1"], -1 : AlienImages["image2_2"]}
Alien3 = {1 : AlienImages["image3_1"], -1 : AlienImages["image3_2"]}

# Initializing game sounds
pygame.mixer.init(frequency=44100, channels=1, buffer=512)
shoot_sound=pygame.mixer.Sound('./sounds/shoot.wav')
#List to store enemy ships
ships = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,1,1,1,1,1,1,1,1,1,1]
]

class Ship(pygame.sprite.Sprite):
    """
    Defining the defender spaceship and its
    properties
    """

    # defines the initial x and y pos of our ship
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.image = pygame.image.load("./images/ship.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = (x_pos, y_pos))
        self.moving_speed = 2

    def update(self, keystate):
        #Right Key
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            if self.rect.x < 730:
                self.rect.x += self.moving_speed

        #Left Key
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            if self.rect.x > 20:
                self.rect.x -= self.moving_speed

        self.draw()

    def draw(self):
        #Drawing the Ship
        game.screen.blit(self.image, self.rect)


class Bullet(pygame.sprite.Sprite):
    """
    describing bullets; thinking to keep missils
    type same for everythnig - all alien ships and
    defender
    """
    def __init__(self, x_pos, y_pos, ofPlayer):

        super().__init__()
        if ofPlayer is True:
            self.image = pygame.image.load("./images/laser.png").convert_alpha()
            self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
            self.velocity = -3
        else:
            self.image = pygame.image.load("./images/enemylaser.png").convert_alpha()
            self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
            self.velocity = 3

    def update(self):
        self.rect.y += self.velocity
        if self.rect.y < 25 or self.rect.y > 600:
            self.kill()
        self.draw()

    def draw(self):
        game.screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    """
    class for alien spaceship and their
    properties. We need to create a list of
    lists of objects of this class Aliens probably.
    """

    def __init__(self, images, x, y, row, col):
        super().__init__()
        self.row=row
        self.col=col
        self.flip = -1
        self.images = images
        self.image = pygame.image.load(self.images[self.flip]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (35, 35))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed_H = 16
        self.speed_V = 12
        self.time_H = 0.75
        self.move_D = False

    def update(self):
        game.timer += game.elapsed_time
        self.time_H = 0.40 + len(game.All_Aliens)/150
        for alien in game.All_Aliens:
            if alien.rect.y >= 495:
                game.gameOver()
                pygame.quit()

        if game.timer > self.time_H:
            if self.move_D:
                self.down()

            else:
                for alien in game.All_Aliens:
                    alien.rect.x += self.speed_H
                    alien.flip *= -1
                    alien.image = pygame.image.load(alien.images[alien.flip]).convert_alpha()
                    alien.image = pygame.transform.scale(alien.image , (35, 35))
                    alien.draw()
                if any(alien.rect.x > 720 for alien in game.All_Aliens) or\
                   any(alien.rect.x < 30 for alien in game.All_Aliens):
                    self.move_D = True
                    self.speed_H *= -1
                game.timer -= self.time_H

        else:
            for alien in game.All_Aliens:
                alien.draw()



    def down(self):
        for alien in game.All_Aliens:
            alien.rect.y += self.speed_V
            alien.flip *= -1
            alien.image = pygame.image.load(alien.images[alien.flip]).convert_alpha()
            alien.image = pygame.transform.scale(alien.image , (35, 35))
            alien.draw()
        self.move_D = False
        game.timer -= self.time_H

    def draw(self):
        game.screen.blit(self.image, self.rect)


class Blocker(pygame.sprite.Sprite):
    """
    Class for defining blocks and their properties;
    basically their damage rate.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((25, 12))
        self.image.fill(ROCK)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self):
        game.screen.blit(self.image, self.rect)


class Mystery(pygame.sprite.Sprite):
    '''
    Class for mystery ship
    '''
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("./images/mystery.png")
        self.image = pygame.transform.scale(self.image, (75, 35))
        self.rect = self.image.get_rect(topleft=(20,40))
        self.current_status=False
        self.rect.x = -75

    def start(self, direct):
        self.direct = direct
        if direct == -1:
            self.rect.x = 800
        else:
            self.rect.x = -75
        self.current_status = True

    def update(self):

        self.rect.x= self.rect.x + self.direct
        game.screen.blit(self.image, self.rect)

        if self.rect.x>800 or self.rect.x<-75:
            self.current_status=False

    def destroyed(self):
        self.current_status=False

    '''
    def status(self,bullet):
        if bullet.rect.x=self.rect.x and bullet.rect.y=self.rect.y:
            self.health=self.health-1
            if self.health==0:
                Add explosion effect and music
                Add to score
                return 1
            else:
                return 0
        else return 0
    '''


class Explosion(pygame.sprite.Sprite):
    """
    Code is for type of explosion:
    1 - 30 points enemy ships (purple)
    2 - 20 points enemy ships (blue)
    3 - 10 points enemy ships (green)
    4 - Mystery
    5 - Player's Ship (haven't added yet)
    """
    def __init__(self, code, score, x, y):
        super().__init__()
        self.code = code
        self.x = x
        self.y = y
        if code == 4:
            self.text = pygame.font.Font(FONT, 20)
            self.textsurface = self.text.render(str(score), False, TITLE_WHITE)
            game.screen.blit(self.textsurface,(self.x + 20, self.y + 6))

        elif code == 5:
            self.image = pygame.image.load("./images/ship.png")
            self.rect = self.image.get_rect(topleft=(self.x, self.y))

        else:
            if code == 1:
                self.image = pygame.image.load("./images/explosionpurple.png")

            elif code == 2:
                self.image = pygame.image.load("./images/explosionblue.png")

            elif code == 3:
                self.image = pygame.image.load("./images/explosiongreen.png")

            self.image = pygame.transform.scale(self.image, (40, 35))
            self.rect = self.image.get_rect(topleft=(x, y))
            game.screen.blit(self.image, self.rect)

        self.timer = time.time()

    def update(self, currentTime):

        if self.code == 4:
            if currentTime - self.timer <= 0.1:
                game.screen.blit(self.textsurface,(self.x + 20, self.y + 6))
            if currentTime - self.timer > 0.4 and currentTime - self.timer <= 0.6:
                game.screen.blit(self.textsurface,(self.x + 20, self.y + 6))
            if currentTime - self.timer > 0.6:
                self.kill()

        elif self.code == 5:
            if currentTime - self.timer > 0.3 and currentTime - self.timer <= 0.6:
                game.screen.blit(self.image, self.rect)
            if currentTime - self.timer > 900:
                self.kill()

        else:
            if currentTime - self.timer <= 0.1:
                game.screen.blit(self.image, self.rect)
            if currentTime - self.timer > 0.1 and currentTime - self.timer <= 0.2:
                self.image = pygame.transform.scale(self.image, (50, 45))
                game.screen.blit(self.image, (self.rect.x-6, self.rect.y-6))
            if currentTime - self.timer > 0.4:
                self.kill()

        """elif self.isShip:
            if currentTime - self.timer > 300 and currentTime - self.timer <= 600:
                game.screen.blit(self.image, self.rect)
            if currentTime - self.timer > 900:
                self.kill()
        else:
            if currentTime - self.timer <= 100:
                game.screen.blit(self.image, self.rect)
            if currentTime - self.timer > 100 and currentTime - self.timer <= 200:
                self.image = transform.scale(self.image, (50, 45))
                game.screen.blit(self.image, (self.rect.x-6, self.rect.y-6))
            if currentTime - self.timer > 400:
                self.kill()"""


class SpaceInvaders(object):
    def __init__(self):
        #Initialize pygame
        pygame.init()
        self.clock = pygame.time.Clock()
        self.timer = 0
        self.timer_2 = 0

        #Initial Game sound in infinite loop
        pygame.mixer.music.load('./sounds/Title_Screen.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)
        #Load screen and caption
        #Initialzing a screen for display
        self.screen = pygame.display.set_mode((800,600))
        #Setting Caption of the game
        pygame.display.set_caption('Space Invaders')

        #Initialzing variables
        self.current_score = 0
        self.lives = 3
        self.current_player = 1
        self.draw_state = 0
        self.background = pygame.image.load("./images/background.png").convert_alpha()
        self.check = False
        #other variables will also be required

        #Initializing font module
        pygame.font.init()

        #Initialzing high score from text file "highscore.txt"
        try:
            filename = "highscore.txt"
            file = open(filename,"r")
            self.highest_score = int(file.read())
            if self.highest_score == ' ':
                self.highest_score=0
            file.close()
        except:
            self.highest_score=0
        #Functions for working on Sound, initial, score, displaying etc.
        #def reset(self):

    def welcome_screen(self):
	#Filling screen black
        self.screen.fill(BLACK)

    	########################################
	    ####Loading Titles and Enemy Points#####
	    ########################################

        pygame.mixer.music.load('./sounds/Title_Screen.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)
        self.titleText1 = pygame.font.Font(FONT, 50)
        textsurface = self.titleText1.render('SPACE', False, TITLE_WHITE)
        self.screen.blit(textsurface,(300,120))

        self.titleText2 = pygame.font.Font(FONT, 33)
        textsurface = self.titleText2.render('INVADERS', False, LIGHT_GREEN)
        self.screen.blit(textsurface,(300,170))

        #This font will be used for all enemy ships text and Continue text
        self.titleText3 = pygame.font.Font(FONT, 25)

        self.enemy1 = pygame.image.load("./images/enemy3_1.png").convert_alpha()
        self.enemy1 = pygame.transform.scale(self.enemy1 , (40, 40))
        self.screen.blit(self.enemy1, (300, 250))

        textsurface = self.titleText3.render('   =  10 pts', False, GREEN)
        self.screen.blit(textsurface,(350,250))

        self.enemy2 = pygame.image.load("./images/enemy2_2.png").convert_alpha()
        self.enemy2 = pygame.transform.scale(self.enemy2 , (40, 40))
        self.screen.blit(self.enemy2, (300, 300))

        textsurface = self.titleText3.render('   =  20 pts', False, BLUE)
        self.screen.blit(textsurface,(350,300))

        self.enemy3 = pygame.image.load("./images/enemy1_2.png").convert_alpha()
        self.enemy3 = pygame.transform.scale(self.enemy3 , (40, 40))
        self.screen.blit(self.enemy3, (300, 350))

        textsurface = self.titleText3.render('   =  30 pts', False, PURPLE)
        self.screen.blit(textsurface,(350,350))

        self.enemy4 = pygame.image.load("./images/mystery.png").convert_alpha()
        self.enemy4 = pygame.transform.scale(self.enemy4 , (80, 40))
        self.screen.blit(self.enemy4, (281, 400))

        textsurface = self.titleText3.render('   =  ?????', False, RED)
        self.screen.blit(textsurface,(350,400))

        textsurface = self.titleText3.render('Press any key to continue', False, TITLE_WHITE)
        self.screen.blit(textsurface,(200,500))

    def mute_status(self,ctr):
        mouse = pygame.mouse.get_pos()
        click_status=pygame.mouse.get_pressed()
        if 785 > mouse[0] > 745 and 45 > mouse[1] > 5:
            if click_status[0]==1 :
                ctr=ctr+1
                if ctr % 2 == 0 :
                    pygame.mixer.music.unpause()
                else :
                    pygame.mixer.music.pause()
        return ctr

    def game_reset(self):

        self.background_text = self.titleText1.render('Next Level..', False, WHITE)

        self.screen.fill(BLACK)
        self.start_time = time.time()
        end =  False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.elapsed_time = time.time() - self.start_time
            if self.elapsed_time <= 1:
                alpha = (1.0 * self.elapsed_time )


            else:
                end = True

            self.background_surface_1 = pygame.surface.Surface((800,600))
            self.background_surface_1.set_alpha(255 * alpha)

            self.screen.fill(BLACK)
            self.background_surface.blit(self.background_text, (300,300))
            self.screen.blit(self.background_surface,(0,0))

            pygame.display.flip()

        # Drawing ships
        self.All_Aliens = pygame.sprite.Group()
        self.Aliens_1 = pygame.sprite.Group()
        self.Aliens_2 = pygame.sprite.Group()
        self.Aliens_3 = pygame.sprite.Group()

        for i in range(11):
            self.SHIP = Enemy(Alien1, 20 + 50 * i, 80, 4, i)
            self.All_Aliens.add(self.SHIP)
            self.Aliens_1.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy(Alien2, 20 + 50 * i, 130, 3, i)
            self.All_Aliens.add(self.SHIP)
            self.Aliens_2.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy(Alien2, 20 + 50 * i, 180, 2, i)
            self.All_Aliens.add(self.SHIP)
            self.Aliens_2.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy(Alien3, 20 + 50 * i, 230, 1, i)
            self.All_Aliens.add(self.SHIP)
            self.Aliens_3.add(self.SHIP)
            self.SHIP.draw()
        for i in range(11):
            self.SHIP = Enemy(Alien3, 20 + 50 * i, 280, 0, i)
            self.All_Aliens.add()
            self.Aliens_3.add()
            self.SHIP.draw()

        pygame.display.flip()

        self.draw_state += 1

    def update_stats(self):
        """
        Function to show current score, highest score and number of lifes left
        """
        self.scoreText = pygame.font.Font(FONT, 20)

        #update score
        textsurface = self.scoreText.render(("Score: "+str(self.current_score)), False, BLUE)
        self.screen.blit(textsurface,(5,5))

        #update high score
        if self.highest_score <= self.current_score:
            self.highest_score = self.current_score
            #To write highest score to file
            filename = "highscore.txt"
            file = open(filename,"w")
            file.write(str(self.highest_score))
            file.close()

        #Display High Score
        textsurface = self.scoreText.render(("Highest Score: "+str(self.highest_score)), False, BLUE)
        self.screen.blit(textsurface,(230,5))

        #Display Life Text
        textsurface = self.scoreText.render("Lives: ", False, BLUE)
        self.screen.blit(textsurface,(570,5))

        #Shows lifes left
        for i in range(self.lives):
            self.live = pygame.image.load("./images/ship.png").convert_alpha()
            self.live = pygame.transform.scale(self.live , (20, 20))
            self.screen.blit(self.live, (670+(i*25), 7))

        #Mute Button
        button=pygame.image.load("./images/mutebutton.png")
        button=pygame.transform.scale(button,(30,30))
        self.screen.blit(button, (750,5))


    def shoot(self):
        shoot_sound.play()
        self.player_bullet = Bullet((self.player.rect.x + 25) , self.player.rect.y, ofPlayer = True)
        self.bullet_group.add(self.player_bullet)
        shoot_sound.play()

    def gameOver(self):
        self.quit = False
        self.Flag = False
        while not self.quit:
            game_oversound = pygame.mixer.music.load('./sounds/Game_Over.wav')
            pygame.mixer.music.set_volume(0.0)
            if self.Flag == True:
                break
            else:
                self.screen.fill(BLACK)
                textsurface = self.titleText1.render('GAME OVER', False, WHITE)
                self.screen.blit(textsurface, (220, 230))
                restart_text = self.titleText3.render('Press R to restart', False, WHITE)
                self.screen.blit(restart_text, (250, 300))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # If user quits game
                        self.quit = True
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            self.reset_game()
                            self.Flag = True
                            break
                        break
                    break
            pygame.display.flip()

    def reset_game(self):
        # Сброс счётчиков и переменных
        self.current_score = 0
        self.lives = 3
        self.draw_state = 0

        # Очистка групп спрайтов
        self.All_Aliens.empty()
        self.Aliens_1.empty()
        self.Aliens_2.empty()
        self.Aliens_3.empty()
        self.frontRow.empty()
        self.block_group.empty()
        self.mystery_group.empty()
        self.explosion_group.empty()
        self.bullet_group.empty()
        self.enemy_bullets.empty()
        self.quit = False
        # Инициализация игры снова
        self.start_game()
    def start_game(self):
        global alpha
        self.background = pygame.image.load("./images/background.png").convert_alpha()
        self.background = pygame.transform.scale(self.background, (800,600))
        pygame.mixer.music.stop()
        pygame.mixer.music.load('./sounds/game_sound.wav')
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(0)
        ## ADD GAMEPLAY START SOUND HERE

        self.timer = 0


        self.screen.fill(BLACK)
        start_time = time.time()
        end =  False
        while not end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            self.elapsed_time = time.time() - start_time
            if self.elapsed_time <= 1:
                alpha = (1.0 * self.elapsed_time )


            else:
                end = True

            self.background_surface = pygame.surface.Surface((800,600))
            self.background_surface.set_alpha(255 * alpha)

            self.screen.fill(BLACK)
            self.background_surface.blit(self.background, (0,0))
            self.screen.blit(self.background_surface,(0,0))

            pygame.display.flip()

        ### ADD all Sprites class object declaration HERE ###

        #Defender Ship
        self.player = Ship(375, 530)
        self.player.draw()
        self.player_group = pygame.sprite.Group()
        self.player_group.add(self.player)

        #Blockers
        self.block_group = pygame.sprite.Group()
        for i in range(8):
            for j in range(4):
                block_1 = Blocker(80+(15*i), 450+(12*j))
                block_2 = Blocker(340+(15*i), 450+(12*j))
                block_3 = Blocker(605+(15*i), 450+(12*j))
                self.block_group.add(block_1, block_2, block_3)
        self.block_group.draw(game.screen)

        #Mystery Ship
        self.mystery_group = pygame.sprite.Group()
        self.mystery=Mystery()
        self.mystery_group.add(self.mystery)

        # Drawing ships
        self.All_Aliens = pygame.sprite.Group()
        self.Aliens_1 = pygame.sprite.Group()
        self.Aliens_2 = pygame.sprite.Group()
        self.Aliens_3 = pygame.sprite.Group()

        self.frontRow = pygame.sprite.Group()

        for i in range(11):
            self.SHIP = Enemy(Alien1, 20 + 50 * i, 80, 0, i)
            ships[0][i] = self.SHIP
            self.All_Aliens.add(self.SHIP)
            self.Aliens_1.add(self.SHIP)
            self.SHIP.draw()

        for i in range(11):
            self.SHIP = Enemy(Alien2, 20 + 50 * i, 130, 1, i)
            ships[1][i] = self.SHIP
            self.All_Aliens.add(self.SHIP)
            self.Aliens_2.add(self.SHIP)
            self.SHIP.draw()

        for i in range(11):
            self.SHIP = Enemy(Alien2, 20 + 50 * i, 180, 2, i)
            ships[2][i] = self.SHIP
            self.All_Aliens.add(self.SHIP)
            self.Aliens_2.add(self.SHIP)
            self.SHIP.draw()

        for i in range(11):
            self.SHIP = Enemy(Alien3, 20 + 50 * i, 230, 3, i)
            ships[3][i] = self.SHIP
            self.All_Aliens.add(self.SHIP)
            self.Aliens_3.add(self.SHIP)
            self.SHIP.draw()

        for i in range(11):
            self.SHIP = Enemy(Alien3, 20 + 50 * i, 280, 4, i)
            ships[4][i] = self.SHIP
            self.frontRow.add(self.SHIP)
            self.All_Aliens.add(self.SHIP)
            self.Aliens_3.add(self.SHIP)
            self.SHIP.draw()

        #Explosion Group
        self.explosion_group = pygame.sprite.Group()

        #Player Bullet Group
        self.bullet_group = pygame.sprite.Group()

        #Enemy Bullet Group
        self.enemy_bullets = pygame.sprite.Group()

        pygame.display.flip()

        self.draw_state += 1

    def collisions_checking(self):

        #Enemy's Bullet and Player's bullet
        currentcollisions = pygame.sprite.groupcollide(self.bullet_group, self.enemy_bullets, True, True)

        #Blocker and Player's bullet
        currentcollisions = pygame.sprite.groupcollide(self.bullet_group, self.block_group, True, True)

        #Blocker and Enemy's bullet
        currentcollisions = pygame.sprite.groupcollide(self.enemy_bullets, self.block_group, True, True)

        #Enemy and Player's bullet
        currentcollisions = pygame.sprite.groupcollide(self.bullet_group, self.All_Aliens, True, False)
        if currentcollisions:
            for value in currentcollisions.values():
                for currentSprite in value:
                    killed_sound=pygame.mixer.Sound('./sounds/invaderkilled.wav')
                    killed_sound.play()

                    if self.frontRow.has(currentSprite):
                        #print(currentSprite.row-1, currentSprite.col)
                        i=1
                        while type(ships[currentSprite.row-i][currentSprite.col])is not Enemy and (currentSprite.row-i)>=0:
                            i=i+1

                        if type(ships[currentSprite.row-i][currentSprite.col])is Enemy and (currentSprite.row-i)>=0:
                            self.frontRow.add(ships[currentSprite.row-i][currentSprite.col])

                    if self.Aliens_1.has(currentSprite):
                        exp = Explosion(1, 30, currentSprite.rect.x, currentSprite.rect.y)
                        self.explosion_group.add(exp)
                        self.current_score += 30
                        self.Aliens_1.remove(currentSprite)
                        ships[currentSprite.row][currentSprite.col]=0

                    if self.Aliens_2.has(currentSprite):
                        exp = Explosion(2, 20, currentSprite.rect.x, currentSprite.rect.y)
                        self.explosion_group.add(exp)
                        self.current_score += 20
                        self.Aliens_2.remove(currentSprite)
                        ships[currentSprite.row][currentSprite.col]=0

                    if self.Aliens_3.has(currentSprite):
                        exp = Explosion(3, 10, currentSprite.rect.x, currentSprite.rect.y)
                        self.explosion_group.add(exp)
                        self.current_score += 10
                        self.Aliens_3.remove(currentSprite)
                        ships[currentSprite.row][currentSprite.col]=0

                    currentSprite.kill()
                break

        #Player and Enemy's bullet
        currentcollisions = pygame.sprite.groupcollide(self.enemy_bullets, self.player_group, True, False)
        if currentcollisions:
            for value in currentcollisions.values():
                for currentSprite in value:
                    killed_sound=pygame.mixer.Sound('./sounds/invaderkilled.wav')
                    killed_sound.play()

                    exp = Explosion(5, 10, currentSprite.rect.x, currentSprite.rect.y)
                    self.explosion_group.add(exp)

                    self.killed_time = time.time()
                    self.check = True

                    self.lives-=1
                    self.player_group.remove(currentSprite)
                break

        #Mystery and Player's bullet
        currentcollisions = pygame.sprite.groupcollide(self.bullet_group, self.mystery_group, True, False)
        if currentcollisions:
            for value in currentcollisions.values():
                for currentSprite in value:
                    killed_sound=pygame.mixer.Sound('./sounds/invaderkilled.wav')
                    killed_sound.play()
                    score = random.choice([50, 100, 150, 200])
                    exp = Explosion(4, score, currentSprite.rect.x, currentSprite.rect.y) #In place of 150, implement some random score here
                    self.current_score += score
                    self.explosion_group.add(exp)
                    currentSprite.rect.x = -75
                    currentSprite.destroyed()
                break

        #Blocker and Enemy
        currentcollisions = pygame.sprite.groupcollide(self.All_Aliens, self.block_group, False, True)


    def mystery_appear(self):

        if self.mystery.current_status==True:
            self.mystery.update()

        else:
            num=random.randint(0,100000)
            if num > 350 and num < 380 :
                #self.mystery=Mystery()
                self.mystery_group.add(self.mystery)
                direct=random.choice([-1,1])
                self.mystery.start(direct)


    def alien_shoot(self):
        chance=random.randint(1,5500)
        #print(chance,len(self.frontRow.sprites()))
        if chance > 300 and chance < 350 and len(self.frontRow.sprites()):
            shoot_sound.play()
            shooter = random.choice(self.frontRow.sprites())
            self.enemy_bullet = Bullet(shooter.rect.x+17, shooter.rect.y+18, False)
            self.enemy_bullets.add(self.enemy_bullet)


    def main(self):
        self.quit = False
        self.welcome_screen() #Display welcome message
        self.Flag = False


        self.st = time.time()
        self.dt = 0

        self.start_time = time.time()
        self.elapsed_time = time.time() - self.start_time


        button_ctr=0
        while not self.quit:
            if self.draw_state == 0:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #If user quits game
                        self.quit = True
                    elif event.type == pygame.KEYDOWN:
                        self.start_game()
                        if event.type == pygame.K_r:
                            self.start_game()

                        self.elased_time = 0

            if self.draw_state > 0:
                #Updating Ship's location
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: #If user quits game
                        self.quit = True
                    #Shoot Key
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and (len(self.bullet_group.sprites()) == 0):
                            self.shoot()

                self.start_time = time.time()
                keystate = pygame.key.get_pressed()

                ### CALL All updating functions here ###
                self.screen.blit(self.background,(0,0))

                if self.check is True:
                    if self.check is True:
                        if time.time() - self.killed_time > 0.9:
                            self.player_group.add(self.player)
                            self.check = False
                if self.check is False:
                    self.player.update(keystate)

                grplen = len(self.bullet_group.sprites())
                if grplen:
                    self.player_bullet.update()
                    self.player_bullet.draw()

                self.block_group.draw(game.screen)
                self.alien_shoot()
                self.SHIP.update()
                self.enemy_bullets.update()
                self.update_stats()
                self.mystery_appear()
                self.mute_status(button_ctr)

                button_ctr=self.mute_status(button_ctr)
                self.collisions_checking()
                self.explosion_group.update(time.time())
                self.elapsed_time = time.time() - self.start_time

                if len(game.All_Aliens) == 0:
                    self.game_reset()

                if self.lives == 0:
                    self.gameOver()

            pygame.display.flip() #Update portions of the screen for software displays
            #pygame.display.update() #Update portions of the screen for software displays

        pygame.quit() #Uninitialize all pygame modules

game = SpaceInvaders()

def run_game():
    game.main()
if __name__ == "__main__":
    run_game()