import pygame
from pygame.locals import *
import math
from sys import exit
from random import randint

pygame.init()

largura = 640

altura = 480
a_dallas = 260
b_dallas = 292

modojanela = True

tela = pygame.display.set_mode((largura, altura),pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption('Last Bullet')
pygame.display.set_icon(pygame.image.load('Dallas/face.png'))

class Dallas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Dallas/walk.png')
        for i in range(4):
            sheet = sprite_sheet.subsurface((i * 24,0),(24,20))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(24*3, 20*3))
        self.speed = 6
        self.rect = self.image.get_rect(topleft = (a_dallas,b_dallas))
        self.life = 100
        self.points = 0
        self.cooldown = 0
        self.regeneration = 0

    def movemento(self):
        self.movleft = False
        self.movright = False
        if self.rect.x <= largura-82:
            if pygame.key.get_pressed()[pygame.K_d]:
                self.rect.x += self.speed
                self.movleft = False
                self.movright = True
        if self.rect.x >= -10:
            if pygame.key.get_pressed()[pygame.K_a]:             
                self.rect.x -= self.speed
                self.movleft = True
                self.movright = False

    def update(self):
        self.movemento()
        if self.life < 100:
            self.life += self.regeneration
        if self.movright and self.movleft == False:
            self.atual += 0.4
            if self.atual >= len(self.sprites):
                self.atual = 0
                pass
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image,(24*3, 20*3))
        elif self.movleft and self.movright == False:
            self.atual += 0.4
            if self.atual >= len(self.sprites):
                self.atual = 0
                pass
            self.image = self.sprites[int(self.atual)]
            self.image = pygame.transform.scale(self.image,(24*3, 20*3))
            self.image = pygame.transform.flip(self.image,True,False)

    def atirar(self):
        self.tiro = Bullet(self.rect.centerx, self.rect.centery, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        return self.tiro

class Life(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Bars/lifebars.png')
        for i in range(6):
            sheet = sprite_sheet.subsurface((0,i * 16),(64,16))
            self.sprites.append(sheet)
        self.atual = 5
        self.image = self.sprites[self.atual]
        self.a_bars = 10
        self.b_bars = 10
        self.image = pygame.transform.scale(self.image,(64*4, 16*4))
        
        self.rect = self.image.get_rect(topleft = (self.a_bars,self.b_bars))
                                            
    def update(self):
        if dallas.life >= 90:
            self.atual = 0
        elif dallas.life >= 70:
            self.atual = 1
        elif dallas.life >= 50:
            self.atual = 2
        elif dallas.life >= 30:
            self.atual = 3
        elif dallas.life >= 10:
            self.atual = 4
        elif dallas.life < 10:
            self.atual = 5
            
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(64*4, 16*4))

class Bullet(pygame.sprite.Sprite):
    def __init__(self, a_bullet, b_bullet, a_target, b_target):
        super().__init__()
        self.image = pygame.Surface((8, 8))
        self.image.fill((228, 58, 22))
        self.rect = self.image.get_rect(center = (a_bullet, b_bullet))

        self.speed = 10

        angulo = math.atan2(b_target-b_bullet, a_target-a_bullet)
        self.cos = math.cos(angulo) * self.speed 
        self.sen = math.sin(angulo) * self.speed 
        self.a = a_bullet
        self.b = b_bullet

    def update(self):
        if self.rect.right >= 640:
            self.kill()
        if self.rect.bottom >= 350:
            self.kill()
        if self.rect.centery <= 0:
            self.kill()
        if self.rect.left <= 0:
            self.kill()

        self.a += self.cos
        self.b += self.sen
        self.rect.centerx = int(self.a)
        self.rect.centery = int(self.b)
      
class Ufo(pygame.sprite.Sprite):
    def __init__(self, a_ufo, b_ufo):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Ufo/ufo.png')
        for i in range(6):
            sheet = sprite_sheet.subsurface((i * 21,0),(21,20))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(21*3, 20*3))
        self.life = 25

        self.speed = randint(0,3)
        self.downspeed = randint(1,4)
        
        self.rect = self.image.get_rect(topleft = (a_ufo,b_ufo))

    def action(self):
        if self.rect.y <= 290:
            if self.rect.x < dallas.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > dallas.rect.x:
                self.rect.x -= self.speed
            self.rect.y += self.downspeed
        else:
            dallas.points -= 15
        if self.rect.colliderect(dallas.rect):
            dallas.life -= 1

    def morte(self):
        if pygame.sprite.spritecollide(self, bullet, True):
            pygame.mixer.Sound.play(destroy)
            self.life -= 25
        if self.life <= 0:
            dallas.points += 25
            self.kill()

    def spawn(self):
        return Ufo(randint(-10, 550), -70)
    
    def update(self):
        self.action()
        self.morte()
        self.atual += 0.2
        if self.atual >= len(self.sprites):
            self.atual = 0
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(21*3, 20*3))

class UfoAxe(pygame.sprite.Sprite):
    def __init__(self, a_ufoa, b_ufoa):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Ufo/ufoaxe.png')
        for i in range(4):
            sheet = sprite_sheet.subsurface((i * 45,0),(45,33))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(45*3, 33*3))
        self.life = 75

        self.speed = randint(1,3)
        self.downspeed = randint(3,5)
        
        self.rect = self.image.get_rect(topleft = (a_ufoa,b_ufoa))

    def action(self):
        if self.rect.x < dallas.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > dallas.rect.x:
            self.rect.x -= self.speed
        if self.rect.y <= 230:
            self.rect.y += self.downspeed
        if self.rect.colliderect(dallas.rect):
            dallas.life -= 2

    def spawn(self):
        return UfoAxe(randint(-10, 550), -80)

    def morte(self):
        if pygame.sprite.spritecollide(self, bullet, True):
            pygame.mixer.Sound.play(destroy)
            self.life -= 25
        if self.life <= 0:
            dallas.points += 80
            self.kill()
            
    def update(self):
        self.action()
        self.morte()
        self.atual += 0.2
        if self.atual >= len(self.sprites):
            self.atual = 0
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(45*3, 33*3))

class UfoShield(pygame.sprite.Sprite):
    def __init__(self, a_ufos, b_ufos):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Ufo/ufoshield.png')
        for i in range(4):
            sheet = sprite_sheet.subsurface((i * 44,0),(44,32))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(44*3, 32*3))
        self.life = 125

        self.speed = randint(1,3)
        self.downspeed = randint(3,5)
        
        self.rect = self.image.get_rect(topleft = (a_ufos,b_ufos))

    def action(self):
        if self.rect.x < dallas.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > dallas.rect.x:
            self.rect.x -= self.speed
        if self.rect.y <= 230:
            self.rect.y += self.downspeed
        if self.rect.colliderect(dallas.rect):
            dallas.life -= 1

    def spawn(self):
        return UfoShield(randint(-10, 550), -80)

    def morte(self):
        if pygame.sprite.spritecollide(self, bullet, True):
            pygame.mixer.Sound.play(destroy)
            self.life -= 25
        if self.life <= 0:
            dallas.points += 100
            self.kill()
            
    def update(self):
        self.action()
        self.morte()
        self.atual += 0.2
        if self.atual >= len(self.sprites):
            self.atual = 0
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(44*3, 32*3))

class UfoBall(pygame.sprite.Sprite):
    def __init__(self, a_ufob, b_ufob):
        super().__init__()
        self.sprites = []
        self.zenmode = []
        sprite_sheet = pygame.image.load('Ufo/ufoball.png')
        for i in range(4,8):
            zensheet = sprite_sheet.subsurface((i * 48,0),(48,25))
            self.zenmode.append(zensheet)
        for i in range(4):
            sheet = sprite_sheet.subsurface((i * 48,0),(48,25))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(48*3, 25*3))
        self.life = 100

        self.speed = randint(0,1)
        self.downspeed = 20
        
        self.rect = self.image.get_rect(topleft = (a_ufob,b_ufob))

    def action(self):
        if self.rect.y < 275:
            if self.rect.x < dallas.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > dallas.rect.x:
                self.rect.x -= self.speed
            self.rect.y += self.downspeed
        elif self.rect.y == 275:
            self.sprites = self.zenmode
            self.rect.y += 2
            self.life += 50
        if self.rect.colliderect(dallas.rect):
            dallas.life -= 1

    def morte(self):
        if pygame.sprite.spritecollide(self, bullet, True):
            pygame.mixer.Sound.play(destroy)
            self.life -= 25
        if self.life <= 0:
            dallas.points += 120
            self.kill()

    def spawn(self):
        return UfoBall(randint(-10, 550), -85)
    
    def update(self):
        self.action()
        self.morte()
        self.atual += 0.2
        if self.atual >= len(self.sprites):
            self.atual = 0
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(48*3, 25*3))
        
class Ground(pygame.sprite.Sprite):
    def __init__(self, posição):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('Background/Chão.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(16*4, 32*4))
        self.rect = self.image.get_rect()
        a_ground = posição * 64
        b_ground = altura - 128
        self.rect = self.image.get_rect(topleft = (a_ground,b_ground))

ufo = Ufo(randint(10,600), -70)
ufo_s = pygame.sprite.Group()

ufoaxe = UfoAxe(randint(10,600), -80)
ufoaxe_s = pygame.sprite.Group()

ufoshield = UfoShield(randint(10,600), -80)
ufoshield_s = pygame.sprite.Group()

ufoball = UfoBall(randint(-10, 550), -85)
ufoball_s = pygame.sprite.Group()

bullet = pygame.sprite.Group()

life = Life()
life_s = pygame.sprite.Group()
life_s.add(life)

dallas = Dallas()
dallas_s = pygame.sprite.Group()
dallas_s.add(dallas)

floor_s = pygame.sprite.Group()
for i in range(10):
    ground = Ground(i)
    floor_s.add(ground)
    
imagem_fundo = pygame.image.load('Background/Fundo.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
fim_de_jogo = pygame.image.load('Background/FimdeJogo.png').convert()
fim_de_jogo = pygame.transform.scale(fim_de_jogo, (largura, altura))
titulo = pygame.image.load('Background/Title.png').convert()
titulo = pygame.transform.scale(titulo, (largura, altura))

relogio = pygame.time.Clock()

font_points = pygame.font.SysFont('powergreensmall',40,True,False)
font_score = pygame.font.SysFont('powergreensmall',60,True,False)

start = False
pause = False

score = 0

shoot = pygame.mixer.Sound('Music/shoot.wav')
destroy = pygame.mixer.Sound('Music/destroy.wav')
startm = pygame.mixer.Sound('Music/start.wav')

music = pygame.mixer.music.load('Music/musicafundo.wav')
pygame.mixer.music.set_volume(0.13)
pygame.mixer.music.play(-1)

while True:
    relogio.tick(30)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and start and dallas.life >= 1 and pause == False:
            if event.button == 1:
                bullet.add(dallas.atirar())
                pygame.mixer.Sound.play(shoot)
        if event.type == KEYDOWN and start and dallas.life >= 1:
            if event.key == pygame.K_p:
                pygame.mixer.Sound.play(startm)
                if pause:
                    pause = False
                else:
                    pause = True
           
    if start:
        if dallas.life >= 1:
            
            tela.blit(imagem_fundo, (0,0))
            
            if dallas.points < -1:
                dallas.life = 0
            elif dallas.points >= 30000:
                difc = [10,70,100]
                dallas.regeneration = 0.25
            elif dallas.points >= 20000:
                difc = [10,80,100]
                dallas.regeneration = 0.2
            elif dallas.points >= 13000:
                difc = [10,90,150]
                dallas.regeneration = 0.2
            elif dallas.points >= 10000:
                difc = [11,100,150]
                dallas.regeneration = 0.15
            elif dallas.points >= 7000:
                difc = [12,120,200]
                dallas.regeneration = 0.15
            elif dallas.points >= 5000:
                difc = [13,140,200]
                dallas.regeneration = 0.1
            elif dallas.points >= 3500:
                difc = [14,160,200]
                dallas.regeneration = 0.1
            elif dallas.points >= 2000:
                difc = [15,180,300]
                dallas.regeneration = 0.05
            elif dallas.points >= 1000:
                difc = [15,200,0]
                dallas.regeneration = 0.05
            else:
                difc = [10,0,0]
                dallas.regeneration = 0
            
            if dallas.points > score:
                score = dallas.points
                
            dallas_s.draw(tela)
            ufoaxe_s.draw(tela)
            ufoshield_s.draw(tela)
            ufoball_s.draw(tela)
            ufo_s.draw(tela)
            life_s.draw(tela)
            bullet.draw(tela)
            floor_s.draw(tela)
            
            if pause == False:
                dallas.update()
                ufoshield_s.update()
                ufoaxe_s.update()
                ufoball_s.update()
                ufo_s.update()
                life.update()
                bullet.update()

                if randint(0,difc[0]) == 1:
                    ufo_s.add(ufo.spawn())
                if randint(0,difc[1]) == 1:
                    ufoaxe_s.add(ufoaxe.spawn())
                if randint(0,difc[1]) == 1:
                    ufoshield_s.add(ufoshield.spawn())
                if randint(0,difc[2]) == 1:
                    ufoball_s.add(ufoball.spawn())

            if dallas.points <= 9999:
                points_dallas = dallas.points//10
                points_text = f'Points: {points_dallas}'
                points_local = 400
            else:
                points_dallas = dallas.points//10000
                fract_points = (dallas.points%10000)//1000
                points_text = f'Points: {points_dallas}.{fract_points}K'
                points_local = 385
                
            formatted_points_text = font_points.render(points_text, True, (39,39,54))
            tela.blit(formatted_points_text, (points_local,28))
                
        else:
            tela.blit(fim_de_jogo, (0,0))
            
            score_text = f'Score: {score}'
            formatted_score_text = font_score.render(score_text, True, (255,240,240))
            tela.blit(formatted_score_text, (160,320))
            
            ufo_s = pygame.sprite.Group()
            ufoaxe_s = pygame.sprite.Group()
            ufoshield_s = pygame.sprite.Group()
            ufoball_s = pygame.sprite.Group()
            bullet = pygame.sprite.Group()
                                                
            dallas.rect.x = 260
                                                
            if pygame.key.get_pressed()[K_SPACE]:
                pygame.mixer.Sound.play(startm)
                score = 0
                dallas.life = 100
                dallas.points = 0

    else:
        tela.blit(titulo, (0,0))
        if pygame.key.get_pressed()[K_SPACE]:
            pygame.mixer.Sound.play(startm)
            start = True
    
    pygame.display.flip()
