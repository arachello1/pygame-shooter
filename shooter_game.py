#Create your own shooter

from pygame import *
from random import randint
from time import sleep

show_levelup = False
run = True
miss =  0
clock = time.Clock()
start_time = time.get_ticks()

window = display.set_mode((700,500))
background = 'galaxy.jpg'
bg = transform.scale(image.load(background), (700, 500))
mixer.init()                           
new_volume = 0.1
mixer.music.set_volume(new_volume )
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font2 = font.Font(None, 50)
font3 = font.Font(None, 100)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 8:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600.:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x+14, 400, 50, 50, 25)
        bullets.add(bullet)
        

class Enemy(GameSprite): 
    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.x = randint(8, 600)
            self.rect.y = 0
            miss += 1
    

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
        
player = Player('rocket.png', 350, 425, 75, 75, 20)

enemies = sprite.Group()
asteroids  = sprite.Group()
speed_enemy1 = 1
speed_enemy2 = 5
for i in range(4):
    enemy = Enemy('ufo.png', randint(8, 600), 0, 90, 50, randint(speed_enemy1, speed_enemy2))
    enemies.add(enemy)
for i in range(2):
    asteroid = Enemy('asteroid.png', randint(8, 600), 0, 90, 50, randint(speed_enemy1, speed_enemy2))
    asteroids.add(asteroid)
bullets = sprite.Group()
score = 0
wait = 5
cooldown = True
finish = False

while run:
    current_time = time.get_ticks()
    different_time = (current_time - start_time) / 1000
    if different_time >= 10 and different_time <= 12:
        speed_enemy1 = 5
        speed_enemy2 = 10
        show_levelup = True
    if different_time >= 20 and different_time <= 22:
        show_levelup = True
    for i in event.get():
        if i.type == QUIT:
            run = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE and cooldown == False:
                wait = 5
                player.fire()
                fire_sound.play()
    if not finish:                
        if wait == 0:
            cooldown = False 
        else:
            cooldown = True
            wait -= 1         
        window.blit(bg, (0,0)) 
        player.update()
        player.reset()
        enemies.update()
        enemies.draw(window)
        if different_time >= 20:
            asteroids.update()
            asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        collide = sprite.groupcollide(bullets, enemies, True, True)
        for i in collide:
            score += 1
            enemy = Enemy('ufo.png', randint(8, 600), 0, 90, 50, randint(speed_enemy1, speed_enemy2))
            enemies.add(enemy)
        if sprite.spritecollide(player, enemies, False) or sprite.spritecollide(player, asteroids, False):
            window.blit(lose,(150, 225))
            finish = True
        misses = font2.render('Misses: ' + str(miss), 1, (255, 255, 255))
        points = font2.render('Score: ' + str(score), 1, (255, 255, 255))
        level_up = font3.render('LEVEL UP', 25, (255, 255, 255))
        lose = font3.render('GAME OVER', 25, (255, 0, 0))
        if miss >= 50:
            window.blit(lose,(150, 225))
            finish = True
        if score >= 25:
            win = font3.render('YOU WIN', 25, (0, 255, 0))
            window.blit(win, (200, 225))
            finish = True
        window.blit(misses, (10, 50))
        window.blit(points, (10, 15))
        if show_levelup:
            window.blit(level_up, (200, 225))
            show_levelup = False
        display.update()
    else:
        time.delay(50)
    time.delay(50)