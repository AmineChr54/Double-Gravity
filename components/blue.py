import pygame
from assets.images.spritesheet import Spritesheet
from logic.constants import *


class Blue(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.DOWN_KEY, self.UP_KEY = False, False
        self.is_jumping, self.on_ground = False, False
        self.image = Spritesheet('assets/images/spritesheet.jpg').parse_sprite("blue.jpg")
        self.rect = self.image.get_rect()
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(GRAVITY, 0)

    def draw(self, canvas):
        canvas.blit(self.image, (self.rect.x, self.rect.y))
        print(f"drawing blue at x={self.rect.x} y={self.rect.y}")

    def update(self, dt, tiles, player):
        self.vertical_movement(dt)
        self.checkCollisionsy(tiles, player)
        self.horizontal_movement(dt)
        self.checkCollisionsx(tiles, player)
        print("updating blue")

    def vertical_movement(self, dt):
        self.acceleration.y = 0
        if self.DOWN_KEY:
            self.acceleration.y += 0.5
        elif self.UP_KEY:
            self.acceleration.y -= 0.5
        self.acceleration.y += self.velocity.y * FRICTION
        self.velocity.y += self.acceleration.y * dt
        self.limit_velocity(8)
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 1.2) * (dt * dt)
        self.rect.y = self.position.y

    def horizontal_movement(self, dt):
        self.velocity.x += self.acceleration.x * dt
        if self.velocity.x > 7:
            self.velocity.x = 7
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.x -= 13.5
            self.on_ground = False

    def checkCollisionsx(self, tiles, player):
        self.on_ground = False
        collisions = self.get_hits(tiles, player)

        for tile in collisions:
            if self.velocity.x > 0:  # mechya lel imin
                self.on_ground = True
                self.is_jumping = False
                self.velocity.x = 0
                self.position.x = min(self.position.x, tile.rect.x - tile.rect.width)
                self.rect.x = self.position.x
            elif self.velocity.x < 0:  # mechya lel isar
                self.position.x = max(self.position.x, tile.rect.x + tile.rect.width)
                self.rect.x = self.position.x

    def checkCollisionsy(self, tiles, player):
        collisions = self.get_hits(tiles, player)
        for tile in collisions:
            if self.velocity.y > 0:  # mechya louta
                self.position.y = min(self.position.y, tile.rect.y - tile.rect.height)
                self.rect.y = self.position.y
            elif self.velocity.y < 0:  # mechya lfouk
                self.position.y = max(self.position.y, tile.rect.y + tile.rect.height)
                self.rect.y = self.position.y

    def limit_velocity(self, max_vel):
        self.velocity.y = max(-max_vel, min(self.velocity.y, max_vel))
        if abs(self.velocity.y) < 0.01:
            self.velocity.y = 0

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
                return True
        return False
