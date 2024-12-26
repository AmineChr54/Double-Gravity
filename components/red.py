import pygame

from assets.images import spritesheet
from assets.images.spritesheet import Spritesheet
from levels.tiles import Tile
from logic.constants import *


class Red(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.is_jumping, self.on_ground = False, False
        self.image = Spritesheet('assets/images/spritesheet.jpg').parse_sprite("red.jpg")
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, GRAVITY)

    def draw(self, canvas):
        canvas.blit(self.image, (self.rect.x, self.rect.y))
        print(f"drawing red at x={self.rect.x} y={self.rect.y}")

    def update(self, dt, tiles, player):
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles, player)
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles, player)
        print("updating red")

    def horizontal_movement(self, dt):
        self.acceleration.x = 0
        if self.LEFT_KEY:
            self.acceleration.x -= 0.5
        elif self.RIGHT_KEY:
            self.acceleration.x += 0.5
        self.acceleration.x += self.velocity.x * FRICTION
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(8)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 1.2) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        self.rect.y = self.position.y

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 13.5
            self.on_ground = False

    def checkCollisionsx(self, tiles, player):
        collisions = self.get_hits(tiles, player)
        for tile in collisions:
            if self.velocity.x > 0: # mechi imin
                self.position.x = min(self.position.x, tile.rect.x - tile.rect.width)
                self.rect.x = self.position.x
            elif self.velocity.x < 0: # mechi isar
                self.position.x = max(self.position.x, tile.rect.x + tile.rect.width)
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles, player):
        self.on_ground = False
        self.rect.bottom += 1
        collisions = self.get_hits(tiles, player)
        for tile in collisions:
            if self.velocity.y > 0: # habet louta
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = min(self.position.y, tile.rect.y - tile.rect.height)
                self.rect.y = self.position.y
            elif self.velocity.y < 0: # talaa lfouk
                self.velocity.y = 0
                self.position.y = max(self.position.y, tile.rect.bottom)
                self.rect.y = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < 0.01:
            self.velocity.x = 0

    def get_hits(self, tiles, player):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile) and tile.name is None:
                hits.append(tile)
        if self.rect.colliderect(player):
            hits.append(player)
        return hits
    def hit_portal(self, tiles):
        for tile in tiles:
            if self.rect.colliderect(tile) and tile.name == "portal_inactive":
                """                     
                print("changing")
                tile = Tile('portal_active.jpg', tile.rect.x, tile.rect.y, tile.spritesheet,
                                      "portal_active")
                """
                return True
        return False

