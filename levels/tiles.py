import csv
import os
import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet, name=None):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = spritesheet
        self.image = spritesheet.parse_sprite(image)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.name = name

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))



class TileMap:
    def __init__(self, filename, spritesheet):
        self.tile_size = 50
        self.start_red_x, self.start_red_y = 0, 0
        self.start_blue_x, self.start_blue_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename), newline='', encoding='utf-8-sig') as data:
            data = csv.reader(data, delimiter=';')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        level_map = self.read_csv(filename)
        # print(map)
        x, y = 0, 0
        for row in level_map:
            # print(row)
            x = 0
            for tile in row:
                # print(tile)
                if tile == '1':
                    tiles.append(Tile('wall.jpg', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2':
                    self.start_red_x, self.start_red_y = x * self.tile_size, y * self.tile_size
                elif tile == '3':
                    self.start_blue_x, self.start_blue_y = x * self.tile_size, y * self.tile_size
                elif tile == '4':
                    tiles.append(Tile('portal_inactive.jpg', x * self.tile_size, y * self.tile_size, self.spritesheet,
                                      "portal_inactive"))
                x += 1

            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
