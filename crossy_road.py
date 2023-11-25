import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# constant measurements
WIDTH, HEIGHT = 800, 600
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
CAR_WIDTH, CAR_HEIGHT = 50, 30
PLAYER_SPEED = 5
CAR_SPEED = 5
JUMP_HEIGHT = 10

# Makes the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Crossy Road")

# player starting position
player_x, player_y = WIDTH / 2, HEIGHT - 50

# list of cars that will be filled with lists of the attributes of other cars
cars = []

# other variables for the game
level = 1
font = pygame.font.Font(None, 36)
between_cars = 550

# makes the chicken image
chicken = pygame.image.load('chicken.png')
chicken = pygame.transform.scale(chicken, (PLAYER_WIDTH, PLAYER_HEIGHT))

# helps loops the game
clock = pygame.time.Clock()
running = True

# Draws the car 
def draw_car(screen, car_x, car_y):
    pygame.draw.rect(screen, 'red', (car_x, car_y, CAR_WIDTH, CAR_HEIGHT))
    
    # Windshield measurements
    windshield_width = CAR_WIDTH * 0.2
    windshield_height = CAR_HEIGHT * 0.6
    windshield_x = car_x + 10
    windshield_y = car_y + CAR_HEIGHT * 0.2

    # Headlights
    headlight_width = windshield_width - 5
    headlight_height = windshield_width - 4
    headlight_x = car_x
    headlight_y = car_y 

    pygame.draw.rect(screen, 'lightblue', (windshield_x, windshield_y, windshield_width, windshield_height))
    pygame.draw.rect(screen, 'yellow', (headlight_x, headlight_y, headlight_width, headlight_height))
    pygame.draw.rect(screen, 'yellow', (headlight_x, headlight_y + 24, headlight_width, headlight_height))


#calls the draw car function for each car
def draw_cars():
    for car in cars:
        draw_car(screen, car[0], car[1])

#adds the character to the screen
def draw_player():
    screen.blit(chicken, (player_x, player_y))

#makes the cars move
def move_cars():
    for car in cars:
        car[0] -= CAR_SPEED

#makes the cars y position and adds them to the cars list 
def make_car():
    car_x = WIDTH
    car_y1 = random.randint(350, 500 - CAR_HEIGHT)
    car_y2 = random.randint(100, 200 - CAR_HEIGHT)
    cars.append([car_x, car_y1])
    cars.append([car_x, car_y2])


#the game loop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
 
    #player movement
    key = pygame.key.get_pressed()
    
    if key[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if key[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_WIDTH:
        player_x += PLAYER_SPEED
    if key[pygame.K_UP]:
        player_y -= JUMP_HEIGHT
    if key[pygame.K_DOWN]:
        player_y += JUMP_HEIGHT


    # how often/when a car gets made
    if len(cars) == 0 or WIDTH - cars[-1][0] > between_cars:
        make_car()
    
    move_cars()


    for car in cars:
        if (player_x < car[0] + CAR_WIDTH and 
            player_x + PLAYER_WIDTH > car[0] and 
            player_y < car[1] + CAR_HEIGHT and 
            player_y + PLAYER_HEIGHT > car[1]):
# in case you bump into a car, running will be false and the game loop stops
            running = False

    if player_y < 25:
        # Player made it across the level
        level += 1
        player_y = HEIGHT - 50
        between_cars = between_cars - 50

    
    if level == 10:
#this means that the player won
        running = False


#making the background
    screen.fill('lightgreen')
    
    finish_line = pygame.Surface((800, 60))
    finish_line.fill("gold")
    screen.blit(finish_line, (0, 25))
    
    road1 = pygame.Surface((800, 150))
    road1.fill("gray")
    screen.blit(road1, (0, 350))

    road2 = pygame.Surface((800, 150))
    road2.fill("gray")
    screen.blit(road2, (0, 100))
    
    draw_cars()
    draw_player()

    # showing the level
    level_text = font.render(f"level: {level}", True, ("black"))
    screen.blit(level_text, (10, 10))

    pygame.display.flip()
    clock.tick(60) 

#winning/losing messages
if not running and level != 10:
    loser_text = font.render(f"You lost! You got to level {level}", True, "black")
    screen.blit(loser_text, (WIDTH / 2 - loser_text.get_width() / 2, HEIGHT / 2 - loser_text.get_height() / 2))
    pygame.display.flip()
    pygame.time.delay(3000)
if not running and level == 10:
    winner_text = font.render(f"You won! You got to level 10!", True, "black")
    screen.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
    pygame.display.flip()
    pygame.time.delay(3000)

# Quit the game
pygame.quit()
sys.exit()
