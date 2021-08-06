import pygame
import random
import math
from pygame import mixer  # for background sounds

# ctrl+alt+L to format everything properly in pycharm
# Intalize the pygame
pygame.init()

# creates screen of width of 800p and height 600p
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.png')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 plays the sound on loop

# Title and icon
pygame.display.set_caption("Space Invaders")
icon1 = pygame.image.load('ufo.png')
pygame.display.set_icon(icon1)

# Player
playerimg = pygame.image.load('player.png')
playerX = 370  # x coordinate of the character(player) relative to the given height
playerY = 480  # y coordinate of the character(player) relative to the given width
playerX_change = 0

# Enemy
# list created for multiple enemies
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 5

for i in range(num_of_enemies):
    enemyimg.append(pygame.image.load('enemy.png'))  # .append is used to write contents in a list
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

# bullet

# ready - you can't see the bullet on the screen
# fire - the bullet is moving
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

# Score
score_value = 0
#  score text's font
font = pygame.font.Font('freesansbold.ttf', 32)  # fresansbold is the font and of size 32px

textX = 10
textY = 10

# Game over text's font
over = pygame.font.Font('freesansbold.ttf', 64)


def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))  # rendering the font method created above
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over.render("GameOver", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))  # to draw(blit means to draw) the player in the screen


def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))  # 16 and 10 are added to make the bullet appear from the centre of the screen and not the left side or upper side


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:

    screen.fill((0, 250, 0))  # R,G,B  #change backgroung color of the screen
    # screen.fill should be written above everything otherwise the screen will be drawn over everything else
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():  # every event is stored in pygame.event.get()
        if event.type == pygame.QUIT:
            running = False

        # IF KEYSTROKE IS PRESSED CHECK WEATHER ITS LEFT OR RIGHT
        if event.type == pygame.KEYDOWN:  # pygame.KEYDOWN checks if any key is pressed while in the game
            if event.key == pygame.K_LEFT:  # checks if left key is pressed
                playerX_change = -5
            if event.key == pygame.K_RIGHT:  # checks if right key is pressed
                playerX_change = 5

        if event.type == pygame.KEYUP:  # checks if key is released from pressing
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')  # bullet sound, .sound is used beacuse its a short sound for specific time only
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

    # to make sure player doesnot go out side the screen
    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:  # nat taken 800 due to the 64px of the player
        playerX = 736

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over
        if enemyY[i] > 450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000  # when enemy crosses 300px take the enemy to 2000px i.e out if the screen
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:  # nat taken 800 due to the 64px of the player
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)  # calling the enemy method created above

    # Bullet movement

    # ends the bulle when it reaches the end of the screen
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # fires the bullet
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)  # calling the player method created above
    show_score(textX, textY)
    pygame.display.update()  # to add the updates
