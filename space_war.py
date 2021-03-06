# Imports
import pygame
import random

# Initialize game engine
pygame.init()

# Window
WIDTH = 960
HEIGHT = 660
SIZE = (WIDTH, HEIGHT)
TITLE = "Space War"
screen = pygame.display.set_mode(SIZE, pygame.FULLSCREEN)
pygame.display.set_caption(TITLE)

# Game Statistics
score = 0

# Timer
clock = pygame.time.Clock()
refresh_rate = 60


# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (100, 255, 100)



# Fonts
FONT_SM = pygame.font.Font(None, 24)
FONT_MD = pygame.font.Font("assets/fonts/rainbow.ttf", 45)
FONT_LG = pygame.font.Font("assets/fonts/spacerangerboldital.ttf", 55)
FONT_XL = pygame.font.Font("assets/fonts/dark_ghost.otf", 96)


# Images
ship_img = pygame.image.load('assets/images/spaceship.red.png').convert_alpha()
laser_img = pygame.image.load('assets/images/laserRed.png').convert_alpha()
enemy_img = pygame.image.load('assets/images/enemyship.png').convert_alpha()
bomb_img = pygame.image.load('assets/images/laserGreen.png').convert_alpha()
explosion_img = pygame.image.load('assets/images/explosion.png')
bg_surf= pygame.image.load('assets/images/Background/galaxy.png')
explosion2_img = pygame.image.load('assets/images/explosion2.png')
powerup_img = pygame.image.load('assets/images/powerup.png')
ufo_img = pygame.image.load('assets/images/ufo.png')

# Sounds
EXPLOSION = pygame.mixer.Sound('assets/sounds/explosion.ogg')
SHOOT = pygame.mixer.Sound('assets/sounds/shoot.wav')
pygame.mixer.music.load('assets/sounds/my_music.mp3')

# Stages
START = 0
PLAYING = 1
WIN = 2
LOSE = 3
PAUSE = 4
RESET = 5

# Game classes
class Ship(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3
        self.shield = 3
        self.shoots_double = False
        
    def move_left(self):
        self.rect.x -= self.speed
    

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed
        
    def shoot(self):
        print("Pew")

        laser = Laser(laser_img)
        laser.rect.centerx = self.rect.centerx
        laser.rect.centery = self.rect.top
        lasers.add(laser)
        
    def update(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH

        ''' check powerups '''
        hit_list = pygame.sprite.spritecollide(self, powerups, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            hit.apply(self)
            
            
        ''' check bombs '''
        hit_list = pygame.sprite.spritecollide(self, bombs, True, pygame.sprite.collide_mask)

        for hit in hit_list:
            print("Oof!")
            self.shield -= 1

            if self.shield == 0:
                self.kill()
                
            explosion = Explosion(explosion2_img)
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery
            explosions.add(explosion)
            
            EXPLOSION.play()

class Explosion(pygame.sprite.Sprite):
     def __init__(self, image):
        self.ticks = 10
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
    
        
     def update(self):
        self.ticks -= 1

        if self.ticks == 0:
            self.kill()

            EXPLOSION.play()
            
class Laser(pygame.sprite.Sprite):
     def __init__(self, image):
        super().__init__()

        self.image = image
        self.rect = self.image.get_rect()
        self.speed = 10

        SHOOT.play()
        
     def update(self):
        self.rect.y -= self.speed

        if self.rect.bottom < 0:
            self.kill()
       
class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def drop_bomb(self):
        print("Boom!")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.top
        bombs.add(bomb)

    def update(self):
        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            print("Hehe!")
            player.score += 1
            self.kill()
           
            explosion = Explosion(explosion_img)
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery
            explosions.add(explosion)

class Ufo(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3

    def drop_bomb(self):
        print("Boom!")

        bomb = Bomb(bomb_img)
        bomb.rect.centerx = self.rect.centerx
        bomb.rect.centery = self.rect.top
        bombs.add(bomb)
        
    def update(self):
        self.rect.x += self.speed

        hit_list = pygame.sprite.spritecollide(self, lasers, True, pygame.sprite.collide_mask)

        if len(hit_list) > 0:
            print("Woo!")
            SHOOT.play()
            self.kill()
            player.score += 10

            explosion = Explosion(explosion_img)
            explosion.rect.centerx = self.rect.centerx
            explosion.rect.centery = self.rect.centery
            explosions.add(explosion)

        
class Bomb(pygame.sprite.Sprite):
     def __init__(self, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.speed = 3

        SHOOT.play()
        
     def update(self):
        self.rect.y += self.speed

        if self.rect.top > HEIGHT:
            self.kill()

class ShieldPowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()

        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 6

    def apply(self, ship):
        print(" Yee ")
        ship.shield = 3

        '''self.shoots_double = True'''
        self.kill()
                                
    
    def update(self):
        self.rect.y += self.speed
        
        if self.rect.top > HEIGHT:
            self.kill()
        
class Fleet():
    def __init__(self, mobs):
       self.mobs = mobs
       self.speed = 1
       self.moving_right = True
       self.drop_speed = 20
       self.bomb_rate = 60 # lower is faster
       
    def move(self):
        hits_edge = False
        
        for m in mobs:
            if self.moving_right:
                m.rect.x += self.speed

                if m.rect.right >= WIDTH:
                    hits_edge = True
            else:
                m.rect.x -= self.speed

                if m.rect.left <= 0:
                    hits_edge = True

        if hits_edge:
            self.reverse()
            self.move_down()
                    
    def reverse(self):
        self.moving_right = not self.moving_right

    def move_down(self):
        for m in mobs:
            m.rect.y += self.drop_speed

    def choose_bomber(self):
        rand = random.randrange(self.bomb_rate)
        mob_list = mobs.sprites()

        if len(mob_list) > 0 and rand == 0:
            bomber = random.choice(mob_list)
            bomber.drop_bomb()
    
    def update(self):
        self.move()
        self.choose_bomber()
        
# Game helper functions
def draw_backround():
    screen.blit(bg_surf, [0, 0])

def show_title_screen():
    title_text = FONT_XL.render("Space War!", 1, WHITE)
    w = title_text.get_width()
    screen.blit(title_text, [WIDTH/2 - w/2, 215])

def show_win_screen():
    title_text = FONT_LG.render("YOU WIN " + str(player.score) + ' points in ' + str(ticks // refresh_rate) + ' seconds ! ', 1, WHITE)
    screen.blit(title_text, [25, 250])

def show_lose_screen():
    title_text = FONT_XL.render("YOU LOSE!", 1, WHITE)
    screen.blit(title_text, [250, 210])

def show_pause():
    text1 = FONT_MD.render("Game Paused", True, WHITE)
    text2 = FONT_MD.render("(Press 'p' to resume)", True, WHITE)
    screen.blit(text1, [400, 250])
    screen.blit(text2, [350, 300])
    
def show_stats():
    score_text = FONT_LG.render(str(player.score), 1, RED)
    screen.blit(score_text, [20, 20])

    shield = FONT_MD.render('Shield: ' + str(ship.shield), 1, WHITE)
    shield_rect = shield.get_rect()
    shield_rect.right = WIDTH - 10
    shield_rect.top = 10
    screen.blit(shield, shield_rect)

def check_win():
    global stage
    
    if len(mobs) == 0:
        stage = WIN
    elif len(player) == 0:
        stage = LOSE

def setup():
    global stage, done, player, ship, lasers, mobs, fleet, bombs, explosions, ticks, powerups, ufo
    

    ''' Make game objects '''
    ship = Ship(ship_img)
    ship.rect.centerx = WIDTH / 2
    ship.rect.bottom = HEIGHT - 30

    ''' Make sprite groups '''
    player = pygame.sprite.GroupSingle()
    player.add(ship)
    player.score = 0
    
    lasers = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
     
    mob1 = Mob(150, 50, enemy_img)
    mob2 = Mob(400, 50, enemy_img)
    mob3 = Mob(650, 50, enemy_img)
    mob4 = Mob(25, 200, enemy_img)
    mob5 = Mob(750, 200, enemy_img)
    
    mobs = pygame.sprite.Group()
    mobs.add(mob1,mob2, mob3, mob4, mob5)

    ufo1 = Ufo(-650, 75, ufo_img)
    ufo = pygame.sprite.Group()
    ufo.add(ufo1)

    
    fleet = Fleet(mobs)

    powerup1 = ShieldPowerUp(200, -2000, powerup_img)
    powerups = pygame.sprite.Group()
    powerups.add(powerup1)
                                
    ''' set stage '''
    stage = START
    done = False

    ''' set timer '''
    ticks = 0
    
# Game loop
setup()

pygame.mixer.music.play(-1)

while not done:

    # Input handling (React to key presses, mouse clicks, etc.)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
                
            if stage == START:
                if event.key == pygame.K_SPACE:
                    stage = PLAYING

            elif stage == PLAYING:
                if event.key == pygame.K_SPACE:
                    ship.shoot()

            elif event.key == pygame.K_p:
                    stage = PAUSE
                    
            elif stage == PAUSE:
                if event.key == pygame.K_p:
                    stage = PLAYING

            elif event.key == pygame.K_r:
                setup()
                    
            elif stage == WIN:
                if event.key == pygame.K_SPACE:
                    setup()

            elif stage == LOSE:
                 if event.key == pygame.K_SPACE:
                    setup()
                    
    pressed = pygame.key.get_pressed()

    if stage == PLAYING:
        if pressed[pygame.K_LEFT]:
            ship.move_left()
        elif pressed[pygame.K_RIGHT]:
            ship.move_right()
        if pressed[pygame.K_UP]:
            ship.move_up() 
        elif pressed[pygame.K_DOWN]: 
            ship.move_down()
    
    # Game logic (Check for collisions, update points, etc.)
    if stage == PLAYING:
        player.update()
        lasers.update()
        bombs.update()
        fleet.update()
        mobs.update()
        ufo.update()
        powerups.update()
        explosions.update()
        ticks += 1
        
        check_win()
        
    # Drawing code (Describe the picture. It isn't actually drawn yet.)
    screen.fill(BLACK)
    draw_backround()
    player.draw(screen)
    lasers.draw(screen)
    bombs.draw(screen)
    mobs.draw(screen)
    ufo.draw(screen)
    powerups.draw(screen)
    explosions.draw(screen)
    show_stats()
    
    
    if stage == START:
        show_title_screen()
    if stage == WIN:
        show_win_screen()
    elif stage == LOSE:
        show_lose_screen()
        
    elif stage == PAUSE:
        show_pause_screen()

    if stage == RESET:
        show_lose_screen()
        
    # Update screen (Actually draw the picture in the window.)
    pygame.display.flip()
    

    # Limit refresh rate of game loop 
    clock.tick(refresh_rate)


# Close window and quit
pygame.quit()
