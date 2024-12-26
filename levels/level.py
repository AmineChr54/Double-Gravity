import pygame
from assets.images.spritesheet import myspritesheet
from levels.tiles import TileMap
from components.red import Red
from components.blue import Blue
from logic.constants import *

background_image = pygame.image.load("assets/images/game.jpg")


class Level:
    def __init__(self, canvas, level_num):
        self.canvas = canvas
        self.red = Red()
        self.blue = Blue()
        self.level_num = level_num
        self.level_map = TileMap('levels/level{}.csv'.format(level_num), myspritesheet)
        self.LEVEL_INITIALIZED = False
        self.LEVEL_STATE = "PLAYING"

    def win_screen_draw(self, mouse_pos):
        black_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        black_screen.fill((0, 0, 0))
        black_screen.set_alpha(128)

        win_font = pygame.font.SysFont(TITLE_FONT, 30)
        win_text = win_font.render("You Won!", True, WHITE_COLOR)
        continue_font = pygame.font.SysFont(TEXT_FONT, 22)
        continue_text = continue_font.render("Click here to continue to the next level!", True, WHITE_COLOR)

        self.canvas.blit(black_screen, (0, 0))
        if (150 <= mouse_pos[0] <= 500) and (200 <= mouse_pos[1] <= 350):
            pygame.draw.rect(self.canvas, LIGHT_SHADE_COLOR, [150, 200, 350, 150])
        else:
            pygame.draw.rect(self.canvas, DARK_SHADE_COLOR, [150, 200, 350, 150])
        self.canvas.blit(win_text, (SCREEN_WIDTH / 2 - win_text.get_width() / 2, 250))
        self.canvas.blit(continue_text, (SCREEN_WIDTH / 2 - continue_text.get_width() / 2, 280))

    def show(self, dt, mouse_pos):
        if self.LEVEL_INITIALIZED:
            if self.LEVEL_STATE == "PLAYING":
                self.canvas.blit(background_image, (0, 0))
                self.level_map.draw_map(self.canvas)
                self.red.draw(self.canvas)
                self.blue.draw(self.canvas)
                self.red.update(dt, self.level_map.tiles, self.blue)
                self.blue.update(dt, self.level_map.tiles, self.red)
                if self.red.hit_portal(self.level_map.tiles) and self.blue.hit_portal(self.level_map.tiles):
                    self.LEVEL_STATE = "WON"
            elif self.LEVEL_STATE == "WON":
                self.level_map.draw_map(self.canvas)
                self.red.draw(self.canvas)
                self.blue.draw(self.canvas)
                self.red.update(dt, self.level_map.tiles, self.blue)
                self.blue.update(dt, self.level_map.tiles, self.red)
                self.win_screen_draw(mouse_pos)
        else:
            self.canvas.blit(background_image, (0, 0))
            self.red.position.x, self.red.position.y = self.level_map.start_red_x, self.level_map.start_red_y
            self.red.rect.x, self.red.rect.y = self.level_map.start_red_x, self.level_map.start_red_y
            self.blue.position.x, self.blue.position.y = self.level_map.start_blue_x, self.level_map.start_blue_y
            self.blue.rect.x, self.blue.rect.y = self.level_map.start_blue_x, self.level_map.start_blue_y
            self.LEVEL_INITIALIZED = True
            self.level_map.draw_map(self.canvas)
            self.red.draw(self.canvas)
            self.blue.draw(self.canvas)
            self.red.update(dt, self.level_map.tiles, self.blue)
            self.blue.update(dt, self.level_map.tiles, self.red)
