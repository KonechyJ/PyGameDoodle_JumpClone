import pygame
from pygame.locals import *
import sys
import random
import time


pygame.init()
vec = pygame.math.Vector2

HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60

YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
BLUE = (18, 18, 233)
RED = (204, 0, 0)
CYAN = (51, 255, 255)


FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Doodle Jump Game")
background = pygame.image.load("Background.jpg")

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((30, 30))
        #self.surf.fill(BLUE)
        self.surf = pygame.image.load("Player.png")
        self.rect = self.surf.get_rect()
        self.pos = vec((10, 360))
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.jumping = False
        self.score = 0

    def move(self):
        self.acc = vec(0, 0.5)
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        self.rect.midbottom = self.pos

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def update(self):
        hits = pygame.sprite.spritecollide(P1, platforms, False)
        if P1.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False


class Gem(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("gem.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            self.kill()


class platform(pygame.sprite.Sprite):
    def __init__(self, width=0, height=18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        #self.surf = pygame.Surface((random.randint(50, 100), 12))
        #self.surf.fill(GREEN)
        self.image = pygame.image.load("platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center=(random.randint(0, WIDTH - 10), random.randint(0, HEIGHT - 30)))

        self.moving = True
        self.point = True
        self.speed = random.randint(-1, 1)

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:
            self.rect.move_ip(self.speed, 0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.left > WIDTH:
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateGem(self):
        if (self.speed == 0):
            gems.add(Gem((self.rect.centerx, self.rect.centery - 50)))


def plat_gen():
    while len(platforms) < 6:
        width = random.randrange(50, 100)
        p = None
        C = True

        while C:
            p = platform()
            p.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
            C = check(p, platforms)

        p.generateGem()
        platforms.add(p)
        all_sprites.add(p)

def check(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 50) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False



all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
gems = pygame.sprite.Group()

P1 = Player()

PT1 = platform(450, 80)
#PT1.surf = pygame.Surface((WIDTH, 20))
#PT1.surf.fill(RED)
PT1.rect = PT1.surf.get_rect(center=(WIDTH / 2, HEIGHT - 10))
PT1.moving = False
PT1.point = False

all_sprites.add(PT1)
all_sprites.add(P1)
platforms.add(PT1)


for x in range(random.randint(5, 6)):
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    pl.generateGem()
    platforms.add(pl)
    all_sprites.add(pl)


while True:
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top <= HEIGHT / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT:
                plat.kill()

    if P1.rect.top > HEIGHT:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            displaysurface.fill(RED)
            # Maybe display GAME OVER IN BLACK HERE
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()


        for gem in gems:
            gem.rect.y += abs(P1.vel.y)
            if gem.rect.top >= HEIGHT:
                gem.kill()

    plat_gen()
    displaysurface.blit(background, (0, 0))
    f = pygame.font.SysFont("Verdana", 20)
    g = f.render(str(P1.score), True, CYAN)
    displaysurface.blit(g, (WIDTH / 2, 10))

    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    for gem in gems:
        displaysurface.blit(gem.image, gem.rect)
        gem.update()

    pygame.display.update()
    FramePerSec.tick(FPS)



