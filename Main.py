# IMPORT ------------------------------------------- #

# imports pygame - the module that we use in this project
import pygame
pygame.init()

# assign some functions - it makes coding easier
image = pygame.image.load
scale = pygame.transform.scale


# SETUP WINDOW ------------------------------------- #

# sets window basic proporties
screen_width = 1300
screen_height = 700
screen_title = "Pygame Pong"

# it makes the basic window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption(screen_title)


# GLOBAL VARIABLES ----------------------------------#

# it contains some basic colors stored in a dictionary
color = {
            "black" : [29, 30, 34],
            "white" : [255, 255, 255]
        }

# declarate game variables and inputs
keys_pressed = pygame.key.get_pressed()
clock = pygame.time.Clock()
framerate = 60
show_framerate = True


# GLOBAL CLASSES ------------------------------------#
class Player():

    # some basic movement script
    def movement():

        if keys_pressed[pygame.K_w]:    # handles up movement
            Player.box.y -= 5

        if keys_pressed[pygame.K_s]:    # handles down movement
            Player.box.y += 5

        if Player.box.top <= 0:    # makes player can't bypass top of the window
            Player.box.top = 0

        if Player.box.bottom >= screen_height:    # makes player can't bypass bottom of the window
            Player.box.bottom = screen_height


    # setup basic code for player
    box = pygame.Rect(60, 275, 20, 150)    # creates player box
    image = scale(image('Assets\\Player.png'), (20, 150))    # loads player image from the 'Assets' folder

    score = 0


class Enemy():

    # some basic enemy AI script
    def movement():

        if Ball.velocity_x > 1:

            if (Ball.box.y + Ball.box.height / 2) - (Enemy.box.y + Enemy.box.height / 2) > 0:    # move down if ball is there
                Enemy.box.y += 5

            if (Ball.box.y + Ball.box.height / 2) - (Enemy.box.y + Enemy.box.height / 2) < 0:    # move up if ball is there
                Enemy.box.y -= 5

            if Enemy.box.top <= 0:    # makes enemy can't bypass top of the window
                Enemy.box.top = 0

            if Enemy.box.bottom >= screen_height:    # makes enemy can't bypass bottom of the window
                Enemy.box.bottom = screen_height


    # setup basic code for enemy
    box = pygame.Rect(1240, 275, 20, 150)    # creates enemy box
    image = scale(image('Assets\\Player.png'), (20, 150))    # loads enemy image from the 'Assets' folder

    score = 0


class Ball():

    # some basic movement and collisions script
    def movement():

        # moves the ball
        Ball.box.x += Ball.velocity_x
        Ball.box.y += Ball.velocity_y

        if Ball.box.top <= 0 or Ball.box.bottom >= screen_height:    # makes ball bounce if it goes outside of the window
            Ball.velocity_y *= -1

        if Ball.box.colliderect(Player.box):    # handle collision for player
            Ball.velocity_x *= -1
            Ball.velocity_y = ((Ball.box.y + Ball.box.height / 2) - (Player.box.y + Player.box.height / 2)) / 10 * Ball.speed_y

        if Ball.box.colliderect(Enemy.box):    # handle collision for enemy
            Ball.velocity_x *= -1
            Ball.velocity_y = ((Ball.box.y + Ball.box.height / 2) - (Enemy.box.y + Enemy.box.height / 2)) / 10 * Ball.speed_y

        if Ball.box.right >= screen_width:    # makes game restart if player win
            restart_game(True)

        if Ball.box.left <= 0:    # makes game restart if player loose
            restart_game(False)


    # setup basic code for the ball
    speed_x = 10
    speed_y = 1.5
    velocity_x = speed_x
    velocity_y = 0

    box = pygame.Rect(620, 335, 30, 30)    # creates ball box
    image = scale(image('Assets\\Ball.png'), (30, 30))    # loads ball image from the 'Assets' folder


class Line():

    # some code for line at the middle of the screen
    image = scale(image('Assets\\Line.png'), (screen_width, screen_height))    # loads line image from the 'Assets' folder


# RESTART GAME ------------------------------------- #
def restart_game(win: bool):

    # resets game objects variables
    Player.box.y = 275
    Enemy.box.y = 275
    Ball.box.x = 620
    Ball.box.y = 335
    Ball.velocity_y = 0

    # adds score to the player or enemy
    if win:
        Player.score += 1
    else:
        Enemy.score += 1

# RENDER TEXT -------------------------------------- #

# helps render some basic text
def text(content, size: int):

    font = pygame.font.Font('Assets\\Font.ttf', size)    # loads font from 'Assets' folder
    display = font.render(str(content), True, color['white'])    # renders actual font

    return display    # returns rendered font ready to display


# DRAW WINDOW -------------------------------------- #

# draw things on the window, it's called once per frame
def draw_window():

    screen.fill(color["black"])    # fills background

    screen.blit(Line.image, (0, 0))    # displays line in the middle of the screen

    screen.blit(Player.image, (Player.box.x, Player.box.y))    # draws player
    screen.blit(Enemy.image, (Enemy.box.x, Enemy.box.y))    # draws enemy
    screen.blit(Ball.image, (Ball.box.x, Ball.box.y))    # draws ball

    screen.blit(text(Player.score, 46), (300, 50))    # displays player score
    screen.blit(text(Enemy.score, 46), (950, 50))    # displays enemy score

    framerate_text = "FPS: " + str(int(clock.get_fps()))    # set framerate display text
    if show_framerate: screen.blit(text(framerate_text, 20), (50, 635))    # displays framerate (if 'show_framerate' option is turn on)


    pygame.display.update()    # displays update


# GAME LOOP ---------------------------------------- #

# contains code that is called once per frame
def main():

    run = True    # gives program info to run

    while run:    # executes main code

        clock.tick(framerate)    # caps framerate

        # handles quiting
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        # gets pressed keys
        global keys_pressed
        keys_pressed = pygame.key.get_pressed()

        # make every object move
        Player.movement()
        Enemy.movement()
        Ball.movement()

        # hmm... what i can do ;)
        draw_window()

    pygame.quit()    # quits when program ends


# run WHOLE code
if __name__ == '__main__':
    main()