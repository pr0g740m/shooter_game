#Create your own shooter

from pygame import *
from random import *
import time as t
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Game")

background = transform.scale(image.load("galaxy.jpg"), (700, 500))

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

fire = mixer.Sound("fire.ogg")

font.init()
font2 = font.Font(None, 36)
win = font2.render("You Win!!", 1, (255, 255, 0))
lose = font2.render("You lost.", 1, (255,0,0))

run = True
clock = time.Clock()

score = 0
lost = 0
lives = 3

class Gamesprite(sprite.Sprite):
    def __init__(self, w, h, picture, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    
    def fire(self):
        bullet = Bullet(15, 20, "bullet.png", self.rect.centerx, self.rect.top, 10)
        bullets.add(bullet)

class Enemy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            
            lost += 1

class Bullet(Gamesprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

class Asteroids(Gamesprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            
            
        

turret = player(50, 75, "rocket.png", 100, 400, 7)
enemies = sprite.Group()

rel_time = False
num_fire = 0
max_bullet = 5

for i in range(1, 6):
    enemy = Enemy(80, 50, "ufo.png", randint(80, win_width - 80), -40, randint(1, 4))
    enemies.add(enemy)

bullets = sprite.Group() 
asteroids = sprite.Group()

for i in range(1, 3):
    asteroid = Asteroids(80, 80, "asteroid.png", randint(80, win_width - 80), -40, randint(1, 3))
    asteroids.add(asteroid)
finished = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key == K_SPACE:


                if num_fire < max_bullet and rel_time == False:
                    num_fire += 1
                    turret.fire()
                    fire.play()
                
                if num_fire >= max_bullet and rel_time == False:
                    rel_time = True
                    start_time = t.time()
            

    if not finished:
        window.blit(background, (0,0))

        text = font2.render("Score: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lost = font2.render("Lost: " +  str(lost), 1, (255, 255, 255))
        window.blit(text_lost, (10, 50))     

        turret.update()
        turret.reset()
        enemies.update()
        enemies.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        if rel_time == True:
            end = t.time()
            if end - start_time < 3:
                text_rel = font2.render("wait, reloading...", 1, (255, 100, 0))
                window.blit(text_rel, (300, 400))
            else:
                num_fire = 0
                rel_time = False
    
        collided = sprite.groupcollide(enemies, bullets, True, True)
        for s in collided:
            score += 1
            enemy = Enemy(80, 50, "ufo.png", randint(80, win_width - 80), -40, randint(1, 4))
            enemies.add(enemy)
        
        if lost >= 3 or lives <= 0:
            finished = True
            window.blit(lose, (300, 200))
        
        if score >= 10:
            finished = True
            window.blit(win, (300, 200))

        if sprite.spritecollide(turret, asteroids, False) or sprite.spritecollide(turret, enemies, False):
            lives -= 1
            sprite.spritecollide(turret, asteroids, True)
            sprite.spritecollide(turret, enemies, True)
        
        text_lives = font2.render(str(lives), 1, (0, 255, 0))
        window.blit(text_lives, (650, 50))

        display.update()

    
    else:
        t.sleep(5)
        finished = False
        score = 0
        lost = 0
        num_fire = 0
        for e in enemies:
            e.kill()
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()
        
        for i in range(1, 6):
            enemy = Enemy(80, 50, "ufo.png", randint(80, win_width - 80), -40, randint(1, 4))
            enemies.add(enemy)
        for i in range(1, 3):
            asteroid = Asteroids(80, 80, "asteroid.png", randint(80, win_width - 80), -40, randint(1, 3))
            asteroids.add(asteroid)

        
    display.update()
    clock.tick(40)


        

