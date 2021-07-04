import pygame
import random
import math
from pygame import mixer

#Initialize Pygame
pygame.init()

#Setting up the Display
screen = pygame.display.set_mode((800,600))
background = pygame.image.load('./images/BackgroundScreen.jpg')


#Background Sound
mixer.music.load('./Sounds/BackgroundMusic.wav')
mixer.music.play(-1)

#Setting up the Caption
pygame.display.set_caption('Space Impact')

#Setting up the Game Icon
icon = pygame.image.load('./images/Logo.png')
pygame.display.set_icon(icon)

#Loading up the Player
playerImg = pygame.image.load('./images/battleship.png')
x_coord = 370
y_coord = 480
changeX = 0

#Loading up the Enemy
enemyImg = []
enemyX = []
enemyY = []
enemy_changeX = []
enemy_changeY = []
num = 10

for i in range(num):
    enemyImg.append(pygame.image.load('./images/enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemy_changeX.append(2)
    enemy_changeY.append(30)

    

#Loading up the Bullet
bullet = pygame.image.load('./images/bullet.png')
bulletX = 0
bulletY = 480
bullet_changeX = 0
bullet_changeY = 10
bullet_state = "ready"

score = 0

font = pygame.font.Font('./Font/hello.ttf',32)
textX = 10
textY = 10

gameover_font = pygame.font.Font('freesansbold.ttf',64)


#Functions to draw in pygame
def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet,(x,y))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False

def show_score(x,y):
    score_val = font.render("Score : "+str(score),True,(255,255,255))
    screen.blit(score_val,(x,y))

def game_over():
    gameover_text = gameover_font.render("GAME OVER",True,(255,255,255))
    screen.blit(gameover_text,(200,250))


running = True

while running:

    #Setting up the Background Propertu
    screen.fill((0,0,0))
    screen.blit(background,(0,0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Assigning the Values for Keystroke
    if event.type == pygame.KEYDOWN:
        
        if event.key == pygame.K_LEFT:
            changeX -= 0.8

        if event.key == pygame.K_RIGHT:
            changeX += 0.8
        if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bullet_sound = mixer.Sound('./Sounds/laser.wav')
                bullet_sound.play()
                bulletX = x_coord
                fire(bulletX,bulletY)
            

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            changeX = 0
    

    x_coord += changeX
    

    #Assigning the Boundary Conditions for Player
    if x_coord <= 0:
        x_coord = 0
    elif x_coord >= 736:
        x_coord = 736

    #Assigning the Boundary Conditions for Enemy
    for i in range(num):

        #For Gameover detection
        if enemyY[i] > 440:
            for j in range(num):
                enemyY[j] = 2000
            game_over()
            break

        #Enemy Movement and Speed
        enemyX[i] += enemy_changeX[i]
        if enemyX[i] <= 0:
            enemy_changeX[i] += 4
            enemyY[i] += enemy_changeY[i]
        elif enemyX[i] >= 736:
            enemy_changeX[i] -= 4
            enemyY[i] += enemy_changeY[i]

        #Collision Detection for bullets
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            explode = mixer.Sound('./Sounds/explosion.wav')
            explode.play()
            bullet_state = "ready"
            score += 1
            bulletY = 480
            enemyX[i] = random.randint(0,736)
            enemyY[i] = random.randint(50,150)

        enemy(enemyX[i],enemyY[i],i)
    
    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480

    if bullet_state is "fire":
        fire(bulletX,bulletY)
        bulletY -= bullet_changeY


    
    
        
    #Enabling the Movement
    player(x_coord,y_coord)
    show_score(textX,textY)
    
    pygame.display.update()
