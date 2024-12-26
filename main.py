from levels.level import Level
from logic.constants import *
from levels.tiles import *
from assets.images.spritesheet import Spritesheet

# Initializations
pygame.init()
canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
TARGET_FPS = 60

# GameStates
STATES = {IN_GAME := "IN_GAME", PAUSED := "PAUSED", MAIN_MENU := "MAIN_MENU", LEVELS_MENU := "LEVELS_MENU",
          SETTINGS_MENU := "SETTINGS_MENU"}

# Loading
spritesheet = Spritesheet('assets/images/spritesheet.jpg')

# GlobalVariables
GAME_STATE = IN_GAME
# LevelSetup
current_level = 1
level = Level(canvas, current_level)

def start_game():
    pass

start_game()

while running:
    dt = clock.tick(60) * .001 * TARGET_FPS
    print(dt)
    pygame.time.delay(GAME_SPEED_DELAY)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if GAME_STATE == IN_GAME and event.key == pygame.K_q:
                level.red.LEFT_KEY = True
            elif GAME_STATE == IN_GAME and event.key == pygame.K_d:
                level.red.RIGHT_KEY = True
            elif GAME_STATE == IN_GAME and event.key == pygame.K_z:
                level.red.jump()
            elif GAME_STATE == IN_GAME and event.key == pygame.K_UP:
                level.blue.UP_KEY = True
            elif GAME_STATE == IN_GAME and event.key == pygame.K_DOWN:
                level.blue.DOWN_KEY = True
            elif GAME_STATE == IN_GAME and event.key == pygame.K_LEFT:
                level.blue.jump()

        if event.type == pygame.KEYUP:
            if GAME_STATE == IN_GAME and event.key == pygame.K_q:
                level.red.LEFT_KEY = False
            elif GAME_STATE == IN_GAME and event.key == pygame.K_d:
                level.red.RIGHT_KEY = False
            elif GAME_STATE == IN_GAME and event.key == pygame.K_z:
                if level.red.is_jumping:
                    # player.velocity.y *= .25
                    level.red.is_jumping = False
            elif GAME_STATE == IN_GAME and event.key == pygame.K_UP:
                level.blue.UP_KEY = False
            elif GAME_STATE == IN_GAME and event.key == pygame.K_DOWN:
                level.blue.DOWN_KEY = False
            elif GAME_STATE == IN_GAME and event.key == pygame.K_LEFT:
                if level.blue.is_jumping:
                    # player.velocity.y *= .25
                    level.blue.is_jumping = False
        if event.type == pygame.MOUSEBUTTONDOWN and level.LEVEL_STATE == 'WON':
            if (150 <= mouse_pos[0] <= 500) and (200 <= mouse_pos[1] <= 350):
                if current_level<= 10:
                    current_level += 1
                    level = Level(canvas, current_level)
                else:
                    GAME_STATE = MAIN_MENU


    # IN GAME
    if GAME_STATE == IN_GAME:
        level.show(dt, mouse_pos)

    screen.fill("purple")
    screen.blit(canvas, (0, 0))
    pygame.display.update()

pygame.quit()
