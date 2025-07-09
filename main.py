import pygame
import random

# initialize pygame
pygame.init()

# create a display surface
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
HUD_LINE = 80
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Burger Dog")

# load images
shiba_left = pygame.image.load("shiba.png").convert_alpha()
#shiba_right = pygame.transform.scale(shiba_right, (48, 48))
shiba_right = pygame.transform.flip(shiba_left, True, False)
shiba_image = random.choice([shiba_right, shiba_left])
shiba_image = shiba_right
shiba_rect = shiba_image.get_rect(midbottom=(WINDOW_WIDTH//2, WINDOW_HEIGHT))


burger_image = pygame.image.load("burger.png").convert_alpha()
burger_image = pygame.transform.scale(burger_image, (48, 48))
burger_rect = burger_image.get_rect(bottomleft=(random.randint(0,WINDOW_WIDTH-48),10))
burger_hit_rect = burger_rect.inflate(-10, -10)
print(f"burger_rect: {burger_rect} burger_hit_rect: {burger_hit_rect}")

burger_points = 0
score = 0
burgers_eaten = 0
lives = 5
boost = 100
shiba_speed = 5
burger_speed = 3


# load a game font
game_font = pygame.font.Font("game_font.ttf", 24)

# game texts
burger_points_text = game_font.render(f"Burger Points: {burger_points}", True, 'orange')
burger_points_rect = burger_points_text.get_rect(topleft=(5, 10))
score_text = game_font.render(f"Score: {score}", True, 'orange')
score_rect = score_text.get_rect(topleft=(5, 45))
title_text = game_font.render(f"Burger Dog", True, 'green')
title_rect = title_text.get_rect(midtop=(WINDOW_WIDTH//2, 10))
burgers_eaten_text = game_font.render(f"Burgers Eaten: {burgers_eaten}", True, 'orange')
burgers_eaten_rect = burgers_eaten_text.get_rect(midtop=(WINDOW_WIDTH//2, 45))

lives_text = game_font.render(f"Lives: {lives}", True, 'orange')
lives_rect = lives_text.get_rect(topright=(WINDOW_WIDTH-5, 10))
boost_text = game_font.render(f"Boost: {boost}", True, 'orange')
boost_rect = boost_text.get_rect(topright=(WINDOW_WIDTH-5, 45))


# load sounds and a music
pygame.mixer.music.load("game_music.wav")
pygame.mixer.music.set_volume(0.1)
missed_sound = pygame.mixer.Sound("missed_sound.mp3")
missed_sound.set_volume(0.2)
hit_sound = pygame.mixer.Sound('hit_sound.mp3')
hit_sound.set_volume(0.2)

# set FPS and the clock
FPS = 60
clock = pygame.time.Clock()

# main game loop
pygame.mixer.music.play(loops=-1, start=0.0)

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # shiba's movement
    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and shiba_rect.right < WINDOW_WIDTH:
        shiba_image = shiba_right
        shiba_rect.x += shiba_speed
    if keys[pygame.K_LEFT]and shiba_rect.left > 0:
        shiba_image = shiba_left
        shiba_rect.x += -shiba_speed
    if keys[pygame.K_DOWN] and shiba_rect.bottom < WINDOW_HEIGHT:
       shiba_rect.y += shiba_speed
    if keys[pygame.K_UP] and shiba_rect.top > HUD_LINE:
        shiba_rect.y += -shiba_speed

    # burger's movement
    burger_rect.y += burger_speed
    burger_hit_rect.center = burger_rect.center

    # shiba misses a burger
    if burger_rect.top > WINDOW_HEIGHT:
        missed_sound.play()
        burger_rect.left = random.randint(0, WINDOW_WIDTH-48)
        burger_rect.bottom = -10
    
    # shiba catches a burger
    if shiba_rect.colliderect(burger_hit_rect):
        hit_sound.play()
        
        score += 1
        burger_rect.left = random.randint(0, WINDOW_WIDTH-48)
        burger_rect.bottom = -10
    

    
    # fill the background of the display
    display_surface.fill('black')

    # inside hud
    score_text = game_font.render(f"Score: {score}", True, 'orange')

    # blit the assetes
    display_surface.blit(shiba_image, shiba_rect)
    pygame.draw.line(display_surface, 'white', (0,HUD_LINE), (WINDOW_WIDTH, HUD_LINE))
    display_surface.blit(burger_image, burger_rect)
    display_surface.blit(burger_points_text, burger_points_rect)
    display_surface.blit(score_text, score_rect)
    display_surface.blit(title_text, title_rect)
    display_surface.blit(burgers_eaten_text, burgers_eaten_rect)
    display_surface.blit(lives_text, lives_rect)
    display_surface.blit(boost_text, boost_rect)

    pygame.draw.rect(display_surface,'red', burger_hit_rect, width=1)
    pygame.display.update()

    clock.tick(FPS)

# end the game
pygame.quit()
