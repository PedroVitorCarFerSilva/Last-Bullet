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

boss = False

tela = pygame.display.set_mode((largura, altura),pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption('Last Bullet')
pygame.display.set_icon(pygame.image.load('Dallas/face.png'))

pygame.mouse.set_visible(False)

imagem_fundo = pygame.image.load('Background/Fundo.png').convert()
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
fim_de_jogo = pygame.image.load('Background/FimdeJogo.png').convert()
fim_de_jogo = pygame.transform.scale(fim_de_jogo, (largura, altura))
titulo = pygame.image.load('Background/Title.png').convert()
titulo = pygame.transform.scale(titulo, (largura, altura))

relogio = pygame.time.Clock()

font_points = pygame.font.SysFont('powergreensmall',40,True,False)
font_score2 = pygame.font.SysFont('powergreensmall',30,True,False)
font_score = pygame.font.SysFont('powergreensmall',60,True,False)
font_life = pygame.font.SysFont('powergreensmall',21,True,False)

start = False
pause = False

bosscount = 0
deathbosscheck = 0

score = 0

morreukk = 0

menucooldown = 0

shoot = pygame.mixer.Sound('Music/shoot.wav')
destroy = pygame.mixer.Sound('Music/destroy.wav')
startm = pygame.mixer.Sound('Music/start.wav')
takehit = pygame.mixer.Sound('Music/hit.wav')
boom = pygame.mixer.Sound('Music/explosion.wav')
died = pygame.mixer.Sound('Music/death.wav')

music = pygame.mixer.music.load('Music/musicafundo.wav')
pygame.mixer.music.set_volume(0.13)
pygame.mixer.music.play(-1)

class Dallas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Dallas/walk.png')
        for i in range(5):
            sheet = sprite_sheet.subsurface((i * 24,0),(24,20))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(24*3, 20*3))
        self.speed = 6
        self.rect = self.image.get_rect(topleft = (a_dallas,b_dallas))
        self.life = 100
        self.points = 0
        self.hitcooldown = 0
        self.shotcooldown = 0
        self.movleft = False
        self.movright = False
        self.dano = 1
        self.framespeed = 0.4
        self.flip = False
        self.bonusboss = 0
        self.bosshand = 0
        self.power = 20

    def movemento(self):
        self.movleft = False
        self.movright = False
        if self.rect.x <= largura-62:
            if pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.movleft = False
                self.movright = True
                self.flip = False
        if self.rect.x >= -10:
            if pygame.key.get_pressed()[pygame.K_a] or pygame.key.get_pressed()[pygame.K_LEFT]:             
                self.rect.x -= self.speed
                self.movleft = True
                self.movright = False
                self.flip = True
        if pygame.mouse.get_pressed() == (1,0,0) and start and dallas.life >= 1 and pause == False and self.shotcooldown == 0:
            bullet.add(self.atirar())
            pygame.mixer.Sound.play(shoot)
            self.shotcooldown = 10

    def imunidade(self):
        if self.hitcooldown > 0:
            if self.hitcooldown >= 3:
                self.dano = 0
                self.atual = 4
                if self.hitcooldown == 10:
                    pygame.mixer.Sound.play(takehit)
            self.hitcooldown -= 1

    def recuo (self):
        if self.shotcooldown > 0:
            self.shotcooldown -=1

    def update(self):
        if self.movleft == False and self.movright == False:
            self.dano = 4
        self.movemento()
        self.imunidade()
        self.recuo()
        self.atual += self.framespeed
        if self.atual >= len(self.sprites) - self.dano:
            self.atual = 0
            self.dano = 1
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(24*3, 20*3))
        if self.flip:
            self.image = pygame.transform.flip(self.image,True,False)
        self.dano = 1

    def atirar(self):
        self.tiro = Bullet(self.rect.centerx, self.rect.centery+12, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
        return self.tiro

    def gun(self):
        self.arma = Gun(self.rect.centerx, self.rect.centery)
        if pause == False:
            self.arma.update()
        return self.arma

class Gun(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Dallas/gun.png')
        self.image = pygame.transform.scale(self.image,(11*3, 7*3))
        self.locx = 0
        self.locy = 0
        self.rect = self.image.get_rect(center = (x, y + 9))

    def update(self):
        angulo = math.atan2(pygame.mouse.get_pos()[1] - self.rect.centery, pygame.mouse.get_pos()[0] - self.rect.centerx)
        if self.rect.centerx <= pygame.mouse.get_pos()[0]:
            self.image = pygame.transform.rotate(self.image, angulo*-58)
            if angulo*-58 <= 92 and angulo*-58 >= 0:
                self.rect.centery += angulo*12
            else:
                self.rect.centery += angulo*-1.2
        if self.rect.centerx > pygame.mouse.get_pos()[0]:
            self.image = pygame.transform.rotate(self.image, angulo*58)
            self.image = pygame.transform.flip(self.image,False,True)
            if (angulo*-58)-180 > -92 and (angulo*-58)-180 < 1:
                self.rect.centery += ((angulo*-58)-180)/4.5
            else:
                self.rect.centery += ((angulo*-58)+180)/240

class Aim(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Dallas/aim.png')
        self.image = pygame.transform.scale(self.image, (12*3, 12*3))
        self.rect = self.image.get_rect(center = (x, y))

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.centery = pygame.mouse.get_pos()[1]

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

        self.speed = 15

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

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y, r, s):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Dallas/heart.png')
        for i in range(8):
            sheet = sprite_sheet.subsurface((i * 12,0),(12,12))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(12*s, 12*s))
        self.rect = self.image.get_rect(center = (x,y))
        self.framespeed = 0.2
        self.collide = True
        self.speed = 10
        self.float = 8
        self.an = 0
        self.regeneration = r
        self.size = s

    def spawn(self, x, y, r, s):
        return Heart(x, y, r, s)
        
    def update(self):
        if self.rect.colliderect(dallas.rect):
            pygame.mixer.Sound.play(startm)
            dallas.life += self.regeneration
            if dallas.life > 100:
                dallas.life = 100
            self.kill()

        if self.rect.centery >= 310:
            self.an += 10
            seno = math.sin(math.radians(self.an))
            self.rect.centery = seno*self.float+320
        else:
            self.rect.centery += self.speed
        
        self.atual += self.framespeed
        if self.atual >= len(self.sprites):
            self.atual = 0
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(12*self.size, 12*self.size))

class Button(pygame.sprite.Sprite):
    def __init__(self, y, rmq):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Bars/button.png')
        for i in range(2):
            sheet = sprite_sheet.subsurface((0,i * 20),(90,20))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(90*4, 20*4))
        self.rect = self.image.get_rect(center = (largura/2, y))
        self.mode = rmq

        self.font = pygame.font.SysFont('powergreensmall',50,True,False)
        self.text = 'Quit Game'
        if self.mode == 0:
            self.text = '  Resume'
        elif self.mode == 1:
            self.text = 'Main Menu'
        self.formatted_text = self.font.render(self.text, True, (39,39,54))
        self.textx = self.rect.x + 60
        self.texty = self.rect.y + 20

    def texts(self):
        tela.blit(self.formatted_text, (self.textx, self.texty))

    def click(self):
        global pause, start, menucooldown
        if self.rect.colliderect(aim.rect):
            self.atual = 1
            self.textx = self.rect.x + 64
            self.texty = self.rect.y + 24
            if pygame.mouse.get_pressed() == (1,0,0) and menucooldown == 0:
                dallas.shotcooldown = True
                if self.mode == 0:
                    menucooldown = 15
                    pygame.mixer.Sound.play(startm)
                    pause = False
                    button_s = pygame.sprite.Group()
                elif self.mode == 1:
                    pygame.mixer.Sound.play(startm)
                    start = False
                    button_s = pygame.sprite.Group()
                else:
                    pygame.quit()
                    exit()
        else:
            self.atual = 0

    def spawn(self, y, rmq):
        return Button(y, rmq)

    def update(self):
        self.textx = self.rect.x + 60
        self.texty = self.rect.y + 20
        self.click()
        self.texts()
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(90*4, 20*4))
      
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
        self.life = 20
        self.rect = self.image.get_rect(topleft = (a_ufo,b_ufo))
        self.speed = randint(0,3)
        self.downspeed = randint(1,4)
        
        self.collide = True
        self.framespeed = 0.2

    def action(self):
        if boss:
            self.rect.y -= self.downspeed*2
            if self.rect.y < -100:
                self.kill()
                pass
        else:
            if self.rect.y <= 290:
                if self.rect.x < dallas.rect.x-5:
                    self.rect.x += self.speed
                elif self.rect.x > dallas.rect.x+5:
                    self.rect.x -= self.speed
                self.rect.y += self.downspeed
            else:
                dallas.points -= 1
        if self.rect.colliderect(dallas.rect) and dallas.hitcooldown == 0 and self.collide:
            dallas.life -= 5
            dallas.hitcooldown = 10

    def morte(self):
        if self.collide:
            if pygame.sprite.spritecollide(self, bullet, True):
                pygame.mixer.Sound.play(destroy)
                self.life -= dallas.power
                if self.life==0:
                    self.atual = 0
        if self.life <= 0:
            self.collide = False
            self.speed = 0
            self.downspeed = 0
            sprite_sheet = pygame.image.load('Ufo/ufo.png')
            self.sprites = []
            self.framespeed = 0.5
            for i in range(7):
                sheet = sprite_sheet.subsurface((i * 21,20),(21,20))
                self.sprites.append(sheet)
            if self.atual >= len(self.sprites)-1:
                dallas.points += 25
                self.kill()
                pass
            
    def spawn(self):
        return Ufo(randint(-10, 550), -70)
    
    def update(self):
        self.action()
        self.morte()
        self.atual += self.framespeed
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
        for i in range(5):
            sheet = sprite_sheet.subsurface((i * 45,0),(45,33))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(45*3, 33*3))
        self.life = 40
        
        self.speed = randint(1,3)
        self.downspeed = randint(3,5)
        
        self.rect = self.image.get_rect(topleft = (a_ufoa,b_ufoa))

        self.collide = True
        self.framespeed = 0.2

        self.dano = 1

        self.drop = 1

    def action(self):
        
        if boss:
            self.rect.y -= self.downspeed*2
            if self.rect.y < -100:
                self.kill()
                pass

        if self.rect.x < dallas.rect.x-6:
            self.rect.x += self.speed
        elif self.rect.x > dallas.rect.x+6:
            self.rect.x -= self.speed
        if self.rect.y <= 230:
            self.rect.y += self.downspeed
        if self.rect.colliderect(dallas.rect) and dallas.hitcooldown == 0 and self.collide:
            dallas.life -= 20
            dallas.hitcooldown = 10

    def spawn(self):
        return UfoAxe(randint(-10, 550), -80)

    def morte(self):
        if self.collide:
            if pygame.sprite.spritecollide(self, bullet, True):
                self.dano = 0
                self.atual = 4
                pygame.mixer.Sound.play(destroy)
                self.life -= dallas.power
                if self.life==0:
                    self.atual = 0
        if self.life <= 0:
            self.drop -= 1
            self.collide = False
            self.speed = 0
            self.downspeed = 0
            sprite_sheet = pygame.image.load('Ufo/ufoaxe.png')
            self.sprites = []
            self.framespeed = 0.5
            for i in range(7):
                sheet = sprite_sheet.subsurface((i * 45,33),(45,33))
                self.sprites.append(sheet)
            if self.atual >= len(self.sprites)-1:
                dallas.points += 75
                self.kill()
                pass
            
    def update(self):
        self.action()
        self.morte()
        self.atual += self.framespeed
        if self.atual >= len(self.sprites) - self.dano:
            self.atual = 0
            self.dano = 1
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(45*3, 33*3))

class UfoShield(pygame.sprite.Sprite):
    def __init__(self, a_ufos, b_ufos):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Ufo/ufoshield.png')
        for i in range(5):
            sheet = sprite_sheet.subsurface((i * 44,0),(44,32))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(44*3, 32*3))
        self.life = 60

        self.speed = randint(1,3)
        self.downspeed = randint(3,5)
        
        self.rect = self.image.get_rect(topleft = (a_ufos,b_ufos))

        self.collide = True
        self.framespeed = 0.2

        self.dano = 1

        self.drop = 1

    def action(self):
        
        if boss:
            self.rect.y -= self.downspeed*2
            if self.rect.y < -100:
                self.kill()
                pass
        
        if self.rect.x < dallas.rect.x-6:
            self.rect.x += self.speed
        elif self.rect.x > dallas.rect.x+6:
            self.rect.x -= self.speed
        if self.rect.y <= 230:
            self.rect.y += self.downspeed
        if self.rect.colliderect(dallas.rect) and dallas.hitcooldown == 0 and self.collide:
            dallas.life -= 10
            dallas.hitcooldown = 10

    def spawn(self):
        return UfoShield(randint(-10, 550), -80)

    def morte(self):
        if self.collide:
            if pygame.sprite.spritecollide(self, bullet, True):
                self.dano = 0
                self.atual = 4
                pygame.mixer.Sound.play(destroy)
                self.life -= dallas.power
                if self.life==0:
                    self.atual = 0
        if self.life <= 0:
            self.drop -= 1
            self.collide = False
            self.speed = 0
            self.downspeed = 0
            sprite_sheet = pygame.image.load('Ufo/ufoshield.png')
            self.sprites = []
            self.framespeed = 0.5
            for i in range(7):
                sheet = sprite_sheet.subsurface((i * 44,32),(44,32))
                self.sprites.append(sheet)
            if self.atual >= len(self.sprites)-1:
                dallas.points += 75
                self.kill()
                pass
            
    def update(self):
        self.action()
        self.morte()
        self.atual += self.framespeed
        if self.atual >= len(self.sprites) - self.dano:
            self.atual = 0
            self.dano = 1
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(44*3, 32*3))

class UfoBall(pygame.sprite.Sprite):
    def __init__(self, a_ufob, b_ufob):
        super().__init__()
        self.sprites = []
        self.zenmode = []
        sprite_sheet = pygame.image.load('Ufo/ufoball.png')
        for i in range(4,9):
            zensheet = sprite_sheet.subsurface((i * 48,0),(48,25))
            self.zenmode.append(zensheet)
        for i in range(9):
            sheet = sprite_sheet.subsurface((i * 48,0),(48,25))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(48*3, 25*3))
        self.life = 40

        self.speed = randint(0,1)
        self.downspeed = 20
        
        self.rect = self.image.get_rect(topleft = (a_ufob,b_ufob))

        self.collide = True
        self.framespeed = 0.2
        self.dano = 2

        self.drop = 1

    def action(self):
        if self.rect.y < 275:
            if self.rect.x < dallas.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > dallas.rect.x:
                self.rect.x -= self.speed
            self.rect.y += self.downspeed
        elif self.rect.y == 275 and self.life > 0:
            self.sprites = self.zenmode
            self.rect.y += 2
            self.life += 40
        if self.rect.colliderect(dallas.rect) and dallas.hitcooldown == 0 and self.collide:
            dallas.life -= 10
            dallas.hitcooldown = 10

    def morte(self):
        if self.collide:
            if pygame.sprite.spritecollide(self, bullet, True):
                self.dano = 0
                if self.sprites == self.zenmode:
                    self.atual = 4
                else:
                    self.atual = 8
                pygame.mixer.Sound.play(destroy)
                self.life -= dallas.power
                if self.life==0:
                    self.atual = 0
        if self.life <= 0:
            self.drop -= 1
            self.collide = False
            self.speed = 0
            self.downspeed = 0
            sprite_sheet = pygame.image.load('Ufo/ufoball.png')
            self.sprites = []
            self.framespeed = 0.5
            for i in range(7):
                sheet = sprite_sheet.subsurface((i * 48,25),(48,25))
                self.sprites.append(sheet)
            if self.atual >= len(self.sprites)-1:
                dallas.points += 125
                self.kill()
                pass

    def spawn(self):
        return UfoBall(randint(-10, 550), -85)
    
    def update(self):
        self.action()
        self.morte()
        self.atual += self.framespeed
        if self.atual >= len(self.sprites) - self.dano:
            self.atual = 0
            self.dano = 1
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(48*3, 25*3))

class UfoBoss(pygame.sprite.Sprite):
    def __init__(self, a_ufobs, b_ufobs):
        super().__init__()
        self.size = 4
        self.sprites = []
        sprite_sheet = pygame.image.load('Ufo/ufoboss.png')
        for i in range(5):
            sheet = sprite_sheet.subsurface((i * 32,0),(32,32))
            self.sprites.append(sheet)
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(32*self.size, 32*self.size))
        self.life = 70
        
        self.float = 8
        self.an = 0
        self.died = False

        self.rotation = 0
        
        self.rect = self.image.get_rect(center = (a_ufobs,b_ufobs))

        self.collide = False
        self.framespeed = 0.2

        self.dano = 1

        self.drop = 1
        
    def action(self):
        if self.died:
            self.collide = False
            self.rect.centery += 8
            self.rect.centerx += 1.8
            self.rotation += 1
        else:
            if self.rect.centery >= 90:
                self.an += 10
                seno = math.sin(math.radians(self.an))
                self.rect.centery = seno*self.float+100
            else:
                self.rect.centery += 5
        if dallas.bosshand <= 0:
            self.collide = True

    def spawn(self):
        return UfoBoss(largura/2, -110)

    def morte(self, score):
        if self.collide:
            if pygame.sprite.spritecollide(self, bullet, True):
                self.dano = 0
                self.atual = 4
                pygame.mixer.Sound.play(destroy)
                self.life -= dallas.power
                if self.life==0:
                    dallas.bosshand = 2
                    self.atual = 0
        if self.life <= 0:
            self.drop -= 1
            self.died = True
            self.size -= 0.09
            if self.rect.centery >= 400:
                dallas.bonusboss += score+500
                dallas.points = 0
                pygame.mixer.Sound.play(boom)
                self.kill()
                pass

    def update(self, score):
        self.action()
        self.morte(score)
        self.atual += self.framespeed
        if self.atual >= len(self.sprites) - self.dano:
            self.atual = 0
            self.dano = 1
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(32*self.size, 32*self.size))
        self.image = pygame.transform.rotate(self.image, self.rotation)

class UfoHand(pygame.sprite.Sprite):
    def __init__(self, x, y, l, sr, sl):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Ufo/ufohand.png')
        self.sprites.append(sprite_sheet.subsurface((0,0),(20,20)))
        self.sprites.append(sprite_sheet.subsurface((80,0),(20,20)))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(20*4, 20*4))
        self.life = 400

        self.speed = 0
        self.downspeed = 8
        
        self.rect = self.image.get_rect(center = (x,y))

        self.collide = False
        self.framespeed = 0.4

        self.dano = 1
        self.prepare = 14

        self.left = l
        self.speedleft = sl
        self.speedright = sr

        self.coming = True
        self.seeking = False
        self.aiming = False
        self.attacking = False
        self.returning = False

    def action(self):

        self.rect.centery += self.downspeed
        self.rect.centerx += self.speed
        
        if self.coming:
            self.downspeed = 8
            self.speed = 0
            if self.rect.centery >= 190:
                self.seeking = True
                self.coming = False

        if self.seeking:
            self.collide = True
            self.sprites = []
            sprite_sheet = pygame.image.load('Ufo/ufohand.png')
            self.sprites.append(sprite_sheet.subsurface((0,0),(20,20)))
            self.sprites.append(sprite_sheet.subsurface((80,0),(20,20)))
            self.downspeed = 0
            if self.rect.centerx > dallas.rect.centerx + 8:
                self.speed = self.speedleft
            elif self.rect.centerx < dallas.rect.centerx - 8:
                self.speed = self.speedright
            else:
                self.speed = 0
                self.aiming = True
                self.seeking = False

        if self.aiming:
            self.prepare -= 1
            self.framespeed = 0.3
            self.sprites = []
            sprite_sheet = pygame.image.load('Ufo/ufohand.png')
            for i in range(5):
                sheet = sprite_sheet.subsurface((i * 20,0),(20,20))
                self.sprites.append(sheet)
            if self.prepare == 0 or self.atual >= 3.5:
                self.atual = 0
                self.attacking = True
                self.aiming = False

        if self.attacking:
            self.prepare = 14
            self.framespeed = 0.4
            self.sprites = []
            sprite_sheet = pygame.image.load('Ufo/ufohand.png')
            for i in range(6):
                sheet = sprite_sheet.subsurface((i * 20,40),(20,20))
                self.sprites.append(sheet)
            self.downspeed = 15
            if self.rect.centery >= 310:
                pygame.mixer.Sound.play(boom)
                self.rect.centery = 310
                self.returning = True
                self.attacking = False

        if self.returning:
            self.framespeed = 0.15
            self.sprites = []
            sprite_sheet = pygame.image.load('Ufo/ufohand.png')
            self.sprites.append(sprite_sheet.subsurface((80,40),(20,20)))
            self.sprites.append(sprite_sheet.subsurface((60,40),(20,20)))
            self.sprites.append(sprite_sheet.subsurface((40,40),(20,20)))
            self.sprites.append(sprite_sheet.subsurface((20,40),(20,20)))
            self.sprites.append(sprite_sheet.subsurface((0,40),(20,20)))
            self.sprites.append(sprite_sheet.subsurface((100,40),(20,20)))
            self.downspeed = -5
            if self.rect.centery >= 310:
                self.atual = 0
            if self.rect.centery <= 190:
                self.framespeed = 0.4
                self.seeking = True
                self.returning = False
        
        if self.rect.colliderect(dallas.rect) and dallas.hitcooldown == 0 and self.collide:
            dallas.life -= 30
            dallas.hitcooldown = 10

    def spawn(self, x, y, l, sr, sl):
        return UfoHand(x, y, l, sr, sl)

    def morte(self):
        if self.collide:
            if pygame.sprite.spritecollide(self, bullet, True):
                self.dano = 0
                self.atual = len(self.sprites)-1
                pygame.mixer.Sound.play(destroy)
                self.life -= dallas.power
                if self.life==0:
                    self.atual = 0
        if self.life <= 0:
            self.collide = False
            self.speed = 0
            self.downspeed = 0
            self.framespeed = 0.5
            sprite_sheet = pygame.image.load('Ufo/ufohand.png')
            self.sprites = []
            if self.coming or self.seeking or self.aiming:
                for i in range(7):
                    sheet = sprite_sheet.subsurface((i * 20,20),(20,20))
                    self.sprites.append(sheet)
            elif self.attacking or self.returning:
                for i in range(7):
                    sheet = sprite_sheet.subsurface((i * 20,60),(20,20))
                    self.sprites.append(sheet)
            if self.atual >= len(self.sprites)-1:
                dallas.bosshand -= 1
                self.kill()
                pass
            
    def update(self):
        self.action()
        self.morte()
        self.atual += self.framespeed
        if self.atual >= len(self.sprites) - self.dano:
            self.atual = 0
            self.dano = 1
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(20*4, 20*4))
        if self.left:
            self.image = pygame.transform.flip(self.image,True,False)

class Explosion(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        sprite_sheet = pygame.image.load('Background/Explosao.png')
        for i in range(13):
            sheet = sprite_sheet.subsurface((i * 160,0),(160,88))
            self.sprites.append(sheet)
        self.atual = 0
        self.framespeed = 0.3
        self.image = self.sprites[self.atual]
        self.image = pygame.transform.scale(self.image,(160*4, 88*4))
        self.rect = self.image.get_rect(topleft = (0,0))

    def update(self):
        self.atual += self.framespeed
        if self.atual >= len(self.sprites):
            self.atual = 0
            pass
        self.image = self.sprites[int(self.atual)]
        self.image = pygame.transform.scale(self.image,(160*4, 88*4))
        
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

ufoboss = UfoBoss(largura/2, 110)
ufoboss_s = pygame.sprite.Group()

ufohand = UfoHand(largura/3, -85, True, -10, 8)
ufohand_s = pygame.sprite.Group()

bullet = pygame.sprite.Group()

heart = Heart(largura/2, 0, 25, 3)
heart_s = pygame.sprite.Group()

explosion = Explosion()
explosion_s = pygame.sprite.Group()
explosion_s.add(explosion)

life = Life()
life_s = pygame.sprite.Group()
life_s.add(life)

dallas = Dallas()
dallas_s = pygame.sprite.Group()
dallas_s.add(dallas)

button = Button(0, 0)
button_s = pygame.sprite.Group()

gun_s = pygame.sprite.Group()

aim = Aim(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
aim_s = pygame.sprite.Group()
aim_s.add(aim)

floor_s = pygame.sprite.Group()
for i in range(10):
    ground = Ground(i)
    floor_s.add(ground)
    
while True:
    relogio.tick(30)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                if menucooldown <= 0 and start and dallas.life >= 1:
                    pygame.mixer.Sound.play(startm)
                    menucooldown = 15
                    if pause:
                        pause = False
                    else:
                        pause = True
                        for i in range(3):
                            button_s.add(button.spawn((120 * i) + 120, i))
                    
    if start:
        if dallas.life >= 1:
            
            tela.blit(imagem_fundo, (0,0))

            if pygame.display.get_active() == False and pause == False:
                pause = True
                for i in range(3):
                    button_s.add(button.spawn((120 * i) + 120, i))

            if dallas.bonusboss > deathbosscheck:
                if explosion.atual >= 12.9:
                    explosion.atual = 0
                    deathbosscheck = dallas.bonusboss
                score = 0
                explosion_s.draw(tela)
                explosion.update()
            
            if dallas.points < -1:
                dallas.life = 0
            elif dallas.points >= 4000:
                boss = True
                difc = [0,0,0]
            elif dallas.points >= 3500:
                difc = [14,270,450]
            elif dallas.points >= 2000:
                difc = [14,300,500]
            elif dallas.points >= 1000:
                difc = [14,330,0]
            else:
                boss = False
                bosscount = 0
                dallas.bosshand = 0
                difc = [12,0,0]
            
            if dallas.points > score:
                score = dallas.points
                
            dallas_s.draw(tela)
            gun_s.draw(tela)
            ufoaxe_s.draw(tela)
            ufoshield_s.draw(tela)
            ufoball_s.draw(tela)
            ufo_s.draw(tela)
            ufoboss_s.draw(tela)
            ufohand_s.draw(tela)
            heart_s.draw(tela)
            bullet.draw(tela)
            life_s.draw(tela)
            floor_s.draw(tela)

            if pause == False:
                button_s = pygame.sprite.Group()
                dallas.update()
                ufoshield_s.update()
                ufoaxe_s.update()
                ufoball_s.update()
                ufo_s.update()
                ufoboss_s.update(score)
                ufohand_s.update()
                heart_s.update()
                life.update()
                bullet.update()

                gun_s = pygame.sprite.Group()
                gun_s.add(dallas.gun())

                if boss:
                    if bosscount == 0:
                        ufoboss_s.add(ufoboss.spawn())
                        bosscount += 1
                        ufohand_s.add(ufohand.spawn(largura/3, -80, False, 8, -10))
                        ufohand_s.add(ufohand.spawn(largura/1.5, -80, True, 10, -8))
                        dallas.bosshand += 2
                else:
                    if randint(0,difc[0]) == 1:
                        ufo_s.add(ufo.spawn())
                    if randint(0,difc[1]) == 1:
                        ufoaxe_s.add(ufoaxe.spawn())
                    if randint(0,difc[1]) == 1:
                        ufoshield_s.add(ufoshield.spawn())
                    if randint(0,difc[2]) == 1:
                        ufoball_s.add(ufoball.spawn())
                        
                for u in ufoshield_s:
                    if u.drop == 0:
                        if randint(0,4) == 1:
                            heart_s.add(heart.spawn(u.rect.centerx, u.rect.centery, 25, 3))
                for u in ufoaxe_s:
                    if u.drop == 0:
                        if randint(0,4) == 1:
                            heart_s.add(heart.spawn(u.rect.centerx, u.rect.centery, 25, 3))
                for u in ufoball_s:
                    if u.drop == 0:
                        if randint(0,3) == 1:
                            heart_s.add(heart.spawn(u.rect.centerx, u.rect.centery, 25, 3))
                for u in ufoboss_s:
                    if u.drop == 0:
                        heart_s.add(heart.spawn(u.rect.centerx, u.rect.centery, 100, 4))
                        
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

            if dallas.bonusboss + score <= 999:
                score_dallas = score + dallas.bonusboss
                score_text = f'Score: {score_dallas}'
            else:
                score_dallas = (dallas.bonusboss + score)//1000
                fract_score = ((dallas.bonusboss + score)%1000)//100
                score_text = f'Score: {score_dallas}.{fract_score}K'
            
            formatted_score_text = font_score2.render(score_text, True, (39,39,54))
            tela.blit(formatted_score_text, (400,58))

            life_text = f'{dallas.life // 5}'
            if dallas.life < 50:
                life_localx = 35
                life_localy = 36
            else:
                life_localx = 29
                life_localy = 35

            formatted_life_text = font_life.render(life_text, True, (39,39,54))
            tela.blit(formatted_life_text, (life_localx,life_localy))

            if pause:
                black = pygame.Surface((largura,altura))
                black.set_alpha(150)
                black.fill((7,7,10))
                tela.blit(black, (0,0))
            menucooldown -= 1
            if menucooldown < 0:
                menucooldown = 0
            button_s.draw(tela)
            button_s.update()
                
        else:
            tela.blit(fim_de_jogo, (0,0))
            
            score_text = f'Score: {score+dallas.bonusboss}'
            formatted_score_text = font_score.render(score_text, True, (255,240,240))
            tela.blit(formatted_score_text, (160,320))
            
            ufo_s = pygame.sprite.Group()
            ufoaxe_s = pygame.sprite.Group()
            ufoshield_s = pygame.sprite.Group()
            ufoball_s = pygame.sprite.Group()
            ufoboss_s = pygame.sprite.Group()
            ufohand_s = pygame.sprite.Group()
            bullet = pygame.sprite.Group()
            heart_s = pygame.sprite.Group()
                                                
            dallas.rect.x = 260

            dallas.hitcooldown = 0
            dallas.shotcooldown = 0

            morreukk += 0.0001
            if morreukk == 0.0001:
                pygame.mixer.Sound.play(died)
                         
            if pygame.key.get_pressed()[K_SPACE]:
                pygame.mixer.Sound.play(startm)
                deathbosscheck = 0
                boss = False
                bosscount = 0
                score = 0
                dallas.bonusboss = 0
                dallas.life = 100
                dallas.points = 0
                dallas.bosshand = 0
                morreukk = 0

    else:
        tela.blit(titulo, (0,0))
        ufo_s = pygame.sprite.Group()
        ufoaxe_s = pygame.sprite.Group()
        ufoshield_s = pygame.sprite.Group()
        ufoball_s = pygame.sprite.Group()
        ufoboss_s = pygame.sprite.Group()
        ufohand_s = pygame.sprite.Group()
        bullet = pygame.sprite.Group()
        heart_s = pygame.sprite.Group()
        dallas.rect.x = 260
        dallas.hitcooldown = 0
        dallas.shotcooldown = 0
        
        if pygame.key.get_pressed()[K_SPACE]:
            pygame.mixer.Sound.play(startm)
            deathbosscheck = 0
            boss = False
            bosscount = 0
            score = 0
            dallas.bonusboss = 0
            dallas.life = 100
            dallas.points = 0
            dallas.bosshand = 0
            morreukk = 0
            pause = False
            start = True

    if pygame.mouse.get_focused():
        aim_s.draw(tela)
    aim_s.update()
    
    pygame.display.flip()
