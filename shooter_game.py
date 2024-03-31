#Создай собственный Шутер!

from pygame import *

from random import randint

window = display.set_mode((700, 500))
display.set_caption('Шутер')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

background = transform.scale(image.load('galaxy.jpg'), (700, 500))

run = True
Clock = time.Clock()

from time import time

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (70, 70))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'right'

    def reset(self):
            window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def move(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', player.rect.centerx, player.rect.centery, 5)
        bullet.image = transform.scale(image.load('bullet.png'), (15, 25))
        bullets.add(bullet)


player = Player('rocket.png', 320, 400, 12)

lost = 0
win = 0

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(0, 625)
            self.rect.y = 0
            lost = lost + 1

enemies = sprite.Group()

enemy = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3))
enemy2 = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3))
enemy3 = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3))
enemy4 = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3))
enemy5 = Enemy('ufo.png', randint(0, 625), 0, randint(1, 3))

enemies.add(enemy)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)

font.init()
font1 = font.SysFont('Arial', 30)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

num_shoot = 0

five_time = 0

bullets = sprite.Group()

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.kill()

        
finish = False

sec_tick = 0

while run == True:
    for e in event.get():
        keys_pressed = key.get_pressed()
        if e.type == QUIT:
            run = False

        elif keys_pressed[K_UP]:
            if num_shoot <= 5:
                player.fire()
                num_shoot += 1
                five_time = time()
            else:
                cur_time = time()

                if cur_time - five_time >= 2:
                    player.fire()
                    num_shoot = 1

    collides = sprite.groupcollide(enemies, bullets, True, True)

    for collide_enemy in collides:
        win = win + 1
        enemy = Enemy('ufo.png', randint(0, 625), 0, randint(2, 6))
        enemies.add(enemy)

    if lost >= 10:
        finish = True
        window.blit(text_defeat, (300, 300))

    if win >= 20:
        finish = True
        window.blit(text_end, (300, 300))

    sec_tick += 1
    
    if sec_tick >= 180:
        asteroid = Asteroid('asteroid.png', randint(0, 625), 2, 3)
        sec_tick = 0

    if finish == False:
        window.blit(background, (0, 0))
        try:
            asteroid.update()
            asteroid.reset()
        except:
            pass    
        enemies.draw(window)
        enemies.update()
        player.reset()
        player.move()
        bullets.draw(window)
        bullets.update()
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (20, 20))
        text_win = font1.render('Счёт: ' + str(win), 1, (255, 255, 255))
        window.blit(text_win, (20, 45))
        text_defeat = font1.render('Проигрыш!', 1, (255, 255, 255))
        text_end = font1.render('Победа!', 1, (255, 255, 255))

    Clock.tick(60)
    display.update()




