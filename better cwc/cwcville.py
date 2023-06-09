import pygame
import time
pygame.init()

win = pygame.display.set_mode((800,500))

pygame.display.set_caption("DooomerCrawl")

clock = pygame.time.Clock()

bulletSound = pygame.mixer.Sound('bullet.mp3')
hitSound = pygame.mixer.Sound('hit.mp3')

music = pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)


walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]
walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]
bg = pygame.image.load('bg.jpg')
char = pygame.image.load('standing.png')

class Player(object):
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.vel = 5
        self.isJump = False
        self.jumpCount = 9
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 20, self.y, 28, 60)
        
    def draw(self,win):
        if self.walkCount >= 27:
            self.walkCount = 0
        if not(self.standing):
            if self.left == True:
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
                
            elif self.right == True:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
                
            else:
                win.blit(walkLeft[0], (self.x, self.y))
                
        self.hitbox = (self.x + 18, self.y + 10, 28, 54)
        
    def hit(self):
        self.isJump = False
        self.jumpCount = 9
        self.x = 60
        self.y = 410
        walkCount = 0
        font1 = pygame.font.SysFont('timesnewroman', 100)
        text = font1.render('-5, You Died', 1, (255, 0, 0))
        win.blit(text, (400 - (text.get_width()/2), 100))
        pygame.display.update()
        i = 0
        while i < 100:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()
#         pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
                
                
class Enemy(object):
    walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]
    
    def __init__(self,x,y,width,height,end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 18, self.y + 10, 28, 54)
        self.health = 10
        self.visible = True
        self.door = 50
        
    def draw(self,win):
        self.move(win)
        if self.visible:
            if self.walkCount + 1 >= 33:
                self.walkCount = 0
                
            if self.vel > 0:
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
                
            pygame.draw.rect(win, (255,0,0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            pygame.draw.rect(win, (0, 125,0), (self.hitbox[0], self.hitbox[1] - 20, 50 - 5 * (10 - (self.health)), 10))
            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
#         pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
    
    def move(self,win):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
                
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
                
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
                
    def hit(self):
        if self.health > 0:
            self.health -= 1
            hitSound.play()
            
        else:
            self.visible = False
        print('hit')
                

            
class Projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing
        
    def draw(self,win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius) 
    

scrwid = 800
run = True
man = Player(60, 410, 64, 64)
goblin = Enemy(100, 415, 64, 64, 650)
shootloop = 0
bullets = []
score = 0
facing = -1
font = pygame.font.SysFont('timesnewroman', 30, True)

def reDrawGameWindow():
    win.blit(bg, (0, 10))
    text = font.render('Score: ' + str(score), 1, (0,0,0))
    win.blit(text, (650, 10))
    man.draw(win)
    goblin.draw(win)
    for bullet in bullets:
        bullet.draw(win)
    pygame.display.update()
    


while run == True:
    clock.tick(50)
    pygame.time.delay(30)
    if goblin.visible:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5

    
    if shootloop > 0:
        shootloop += 1
        
    if shootloop > 3:
        shootloop = 0
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    for bullet in bullets:
        if goblin.visible == True:
            
            if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
                if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                    goblin.hit()
                    score += 1
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < 800 and bullet.x > 0:
            bullet.x += bullet.vel
            
        else:
            bullets.pop(bullets.index(bullet))
            
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE] and shootloop == 0:
        
        if man.left:
            facing = -1
            
        elif man.right:
            facing =1
            
        if len(bullets) < 10:
            bulletSound.play()
            bullets.append(Projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0,0,0), facing))
        
        shootloop = 1
        
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
        
    elif keys[pygame.K_RIGHT] and man.x < scrwid - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        man.standing = False
        
    else:
        man.standing = True
        man.walkCount = 0
        
    if not(man.isJump):
            
        if keys[pygame.K_UP]:
            man.isJump = True
            
    else:
        if man.jumpCount >= -9:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
            
        else:
            man.isJump = False
            man.jumpCount = 9
            
    reDrawGameWindow()
    
pygame.quit()

