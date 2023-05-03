import pygame
pygame.init()

win = pygame.display.set_mode((500,500))

pygame.display.set_caption("DooomerCrawl")

clock = pygame.time.Clock()


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
        self.jumpCount = 8
        self.left = False
        self.right = False
        self.walkCount = 0
        
    def draw(self,win):
        if self.walkCount >= 27:
            self.walkCount = 0
        
        if self.left == True:
            win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            
        elif self.right == True:
            win.blit(walkRight[self.walkCount//3], (self.x,self.y))
            self.walkCount += 1
            
        else:
            win.blit(char, (self.x,self.y))
            
            
        
    

scrwid = 500
run = True
man = Player(300, 410, 64, 64)

def reDrawGameWindow():
    win.blit(bg, (0, 10))
    man.draw(win)
    pygame.display.update()
    


while run == True:
    clock.tick(50)
    pygame.time.delay(35)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        
    elif keys[pygame.K_RIGHT] and man.x < scrwid - man.width - man.vel:
        man.x += man.vel
        man.right = True
        man.left = False
        
    else:
        man.right = False
        man.left = False
        man.walkCount = 0
        
    if not(man.isJump):
            
        if keys[pygame.K_SPACE]:
            man.isJump = True
            
    else:
        if man.jumpCount >= -8:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
            
        else:
            man.isJump = False
            man.jumpCount = 8
            
    reDrawGameWindow()
    
pygame.quit()