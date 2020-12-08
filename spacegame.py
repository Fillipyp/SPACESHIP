import os
import random
import arcade
import pygame
import self
from pygame.examples.sound import mixer
from pyglet.media import player

pygame.font.init()
pygame.init()

WIDTH, HEIGHT = 1320, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CoroFighter")

# Load images
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "corona.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "corona.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "corona.png"))
LOGO = pygame.image.load(os.path.join("assets", "logo2.png"))
FUNDO = pygame.image.load(os.path.join("assets", "menu2.png"))
# Player player
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "ninja2.png"))

# Lasers
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets", "alcool2.png"))
SUPER_LASER = pygame.image.load(os.path.join("assets", "alcool3.png"))

# Background
BG = pygame.image.load(os.path.join("assets", "background.png"))
BG2 = pygame.image.load(os.path.join("assets", "background2.png"))
BG3 = pygame.image.load(os.path.join("assets", "background3.png"))

#music





class Laser:
    def __init__(self, x, y, img):

        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)



class Shooter(arcade.Window):
    def __init__(self, width, height, title):

        super().__init__(width, height, title)

        #Loots e muitas outras variáveis a serem configuradas
        #como sons,imagens, valores referentes a quantidade de vida etc..

        self.colisaosound1 = arcade.load_sound("sons/explosion1.wav")
        self.colisaosound2 = arcade.load_sound("sons/explosion2.wav")
        self.bgmusic = arcade.load_sound("sons/title.wav")
        self.lasersound = arcade.load_sound("sons/lasergun1.wav")
        self.lasersound2 = arcade.load_sound("sons/miss.wav")
        self.titlemusic = arcade.load_sound("sons/computer1.wav")
        self.powerupsound = arcade.load_sound("sons/powerup.wav")

class Ship:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0



    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)

            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):

        if self.cool_down_counter == 0:
            lasersound = arcade.load_sound("sons/lasergun1.wav")
            arcade.play_sound(lasersound)
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.colisaosound1 = arcade.load_sound("sons/explosion2.wav")
        self.lasersound = arcade.load_sound("sons/lasergun1.wav")
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()

        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasersound.play(volume=0.035)
                        if laser in self.lasers:

                            self.lasers.remove(laser)
                            self.colisaosound1.play(volume=0.040)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))


class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.lasersound = arcade.load_sound("sons/lasergun1.wav")
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel

    def shoot(self):
        if self.cool_down_counter == 0:

            laser = Laser(self.x-20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1



def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 0
    lives = 10
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 5
    enemy_vel = 3

    player_vel =  7
    laser_vel = 7

    player = Player(300, 630)

    clock = pygame.time.Clock()

    lost = False
    lost_count = 0


    def redraw_window():
        if level == 1:
            WIN.blit(BG, (0, 0))
        if level == 2:
            WIN.blit(BG2, (0, 0))
            COOLDOWN = 4

        if level == 3:
            WIN.blit(BG3, (0, 0))




        # draw text
        lives_label = main_font.render(f"Vidas : {lives}", 1, (255,255,255))
        level_label = main_font.render(f"Level: {level}", 1, (255,255,255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("Você Perdeu!!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()


        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()




        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player.x - player_vel > 0: # left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH: # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: # up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: # down
            player.y += player_vel
        if keys[pygame.K_SPACE]: ##ATRIBUIR O SOM DO TIRO AQUI


           player.shoot()



        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 2*60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)



def main_menu():
    title_font = pygame.font.SysFont("comicsans", 70)
    WIN.blit(LOGO,(200,200))
    pygame.display.flip()

    from pygame import mixer
    mixer.init()
    mixer.music.load('sons/computer1.wav')
    pygame.mixer.music.set_volume(0.25)
    mixer.music.play()

    run = True
    while run:
        WIN.blit(LOGO, (500, 200))
        pygame.display.flip()
        WIN.blit(FUNDO, (0,0))
        title_label = title_font.render("...", 1, (255,255,255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mixer.music.stop()
                pygame.mixer.music.load("sons/musica.mp3")
                pygame.mixer.music.play(-1)
                main()

    pygame.quit()


main_menu()
