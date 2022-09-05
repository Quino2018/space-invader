# Import libraries
from turtle import distance
import pygame
import random
import math
from pygame import mixer

# Initializate pygame
pygame.init()

# window size
screen_width = 800
screen_height = 600

# Size variable
size = (screen_width, screen_height)

# Display window
screen = pygame.display.set_mode(size)

#background image
background = pygame. image.load("estrellas.jpg")

mixer.music.load("8-bit-moonlight-sonata-music-loop-20436.wav")
mixer.music.play( -1)

#title
pygame.display.set_caption("Space invaders barato")

#Icon
icon = pygame.image.load("ufo icon.png")
pygame.display.set_icon(icon)

# Player
player_img = pygame.image.load("nave-espacial.png")
player_x = 363
player_y = 495
player_x_change = 0


# Enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []

# Number of enemies
number_enemies = 8

#Create multiple enemies 
for item in range( number_enemies ):
    enemy_img.append  (pygame.image.load("ufo.png"))
    enemy_x.append (random.randint(0, 735))
    enemy_y.append (random.randint(50, 150))
    enemy_x_change.append (0.5)
    enemy_y_change.append (30)

#Bullet
bullet_img =  pygame.image.load("bala.png")
bullet_x = 0
bullet_y = 480       #the same player y
bullet_x_change = 0
bullet_y_change = 2
bullet_state = "ready"

# Score
score = 0

#Font variable
score_font = pygame.font.Font( "PluranonPro-ow5VV.ttf", 32 )

# Text position
text_x = 10
text_y = 10

# game over text
go_font = pygame.font.Font( "PluranonPro-ow5VV.ttf", 64 )
go_x = 150
go_y = 250

# Bonificación de velocidad
speed_img = pygame.image.load("speed.png")
speed_x = random.randint(64, 736)
speed_y = 0
speed_y_change = 0.5

# speed boost collision fuction
def is_collision( speed_x, speed_y, player_x, player_y ):
    distance_speed = math.sqrt( (speed_x - player_x ) ** 2 + (speed_y - player_y) **2)

      
# speed boost fuction
def boost(x, y):
    screen.blit(speed_img, (x, y))
    
        

# Game over fuction
def game_over(x, y):
    go_text = go_font.render( "Game Over", True, (255, 255, 255))
    screen.blit( go_text , ( x, y ) )

# Score text function
def show_text(x, y):
    score_text = score_font.render("SCORE:   " + str(score), True, (255, 255, 255))
    screen.blit( score_text, (x, y))

# Player funtion
def player(x, y):
    screen.blit(player_img, (x, y))

# Enemy Function
def enemy(x, y, item):
    screen.blit(enemy_img[item], (x, y))

# Fire function
def fire(x, y):
    global  bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 16))

# Collision function
def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt( (enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)

    if distance < 40:
        return True
    else:
        return False

 

# Game loop
running = True
while running:

   

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False

        # If keystroke is pressed
        # checks wheter its right or left

        # Si "key a" es presionada 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player_x_change = -1
                
        # Si "key a" es sualta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player_x_change = 0

        # Si "key d" es presionada
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                player_x_change = +1

        # Si "key space" es presionada
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound=mixer.Sound("disparo 2(MP3_128K).wav")
                    bullet_sound.play()

                    bullet_x = player_x
                fire( bullet_x, bullet_y)

        # Si "key d" es sualta
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player_x_change = 0
      
    # Color RGB: Red - Green - Blue
    rgb = (0,0,0)
    screen.fill(rgb)

    # Show backgraud image
    screen.blit( background, (0,0))

    

    # call player function
    player_x += player_x_change
    player(player_x, player_y)

    # Enemy moment
    for item in range( number_enemies ):

        #game over zone
        if enemy_y[ item ] > 440:
            for j in range( number_enemies ):
                enemy_x [ j ] = 2000
            
            # Call game over fuction
            game_over( go_x, go_y )

            #Game over
            break

        enemy_x[item] += float(enemy_x_change[item])

        if enemy_x[item] <= 0:
            #enemy_x[item] = 1
            enemy_x_change[item] = 0.5
            enemy_y[item] += enemy_y_change[item]

        elif enemy_x[item] >= 736:
            #enemy_x[item] >= 735
            enemy_x_change[item] = -0.5
            enemy_y[item] += enemy_y_change[item]

        # Call collision function
        collision = is_collision(enemy_x[item], enemy_y[item], bullet_x, bullet_y)

        if collision:
            explosion_sound = mixer.Sound("muerte.wav")
            bullet_y = 480
            bullet_state = "ready"
            score += 1
            #print (score)
            enemy_x[item] = random.randint(0, 735)
            enemy_y[item] = random.randint(50, 150)

        # Call enemy function
        enemy(enemy_x[item], enemy_y[item], item)

    if collision:
        bullet_y = 480
        bullet_state = "ready"
        score += 1


    # bullet movent
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # player x buondaries left
    if player_x <= 0:
        player_x = 0 
    
    # player x buondaries right
    if player_x >= 736:
        player_x = 736

    # añanir enemigos 
    if score == 8:
        number_enemies + 10

    # aperecer boost speed
    if score == 45:
        distance_speed = True
            



    #Call the text fuction
    show_text(text_x, text_y)

    # Update Window
    pygame.display.update()