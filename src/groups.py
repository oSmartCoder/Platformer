import pygame
from pygame.math import Vector2

from settings import *


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        """
        My personal explaination regarding to how this CameraGroup inheritence works.

        If there wasn't a camera that follows the player, the player would be going off the screen, and those values are what is stored directly in the player's attrs.
        The offset is calculated to then get the values of what would be to the user's screen. Real attrs are stored within their own objects, and the offsets are to get the 'camera' values.
        - the self.camera_rect attr in this object is to depict the 'real' values on where the game is at.
        """

        super().__init__()

        self.win = pygame.display.get_surface()

        self.offset = Vector2(0, 0)

        self.borders = {
            'left': 200,
            'right': 400,
            'top': 200,
            'bottom': 200
        }

        self.width = WIN_X - (self.borders['left'] + self.borders['right'])
        self.height = WIN_Y - (self.borders['top'] + self.borders['bottom'])

        self.camera_rect = pygame.Rect(TILE_SIZE, self.borders['top'], self.width, self.height)
    
    def custom_draw(self, active_sprites: pygame.sprite.Group):
        player = active_sprites.sprites()[0]
        
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        self.offset = Vector2(self.camera_rect.left - self.borders['left'], self.camera_rect.top - self.borders['top'])

        
        # Stop camera at borders
        if self.offset.x <= 0:
            self.offset.x = 0
        elif self.offset.x >= (end:=TILE_SIZE * TILE_X - WIN_X):
            self.offset.x = end

        if self.offset.y <= 0:
            self.offset.y = 0
        elif self.offset.y >= (end:=TILE_SIZE * TILE_Y - WIN_Y):
            self.offset.y = end        

        # Stop player at borders
        if player.rect.left <= 0:
            player.rect.x = self.offset.x
        elif player.rect.right >= (end:=TILE_SIZE * TILE_X):
            player.rect.right = end

        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.win.blit(sprite.image, offset_pos)


class InteractiveGroup(pygame.sprite.Group):
    def __init__(self, interactives: dict):
        """
        Group for the interaction with active sprites
        """

        super().__init__()

        self.win = pygame.display.get_surface()

        self.interactives = interactives

        self.coin_sound = pygame.mixer.Sound('Platformer/assets/sounds/coin_received.mp3')
        self.item_sound = pygame.mixer.Sound('Platformer/assets/sounds/item_received.mp3')
        self.item_sound.set_volume(0.8)

        self.has_key = False
        self.has_won = False
        self.has_lost = False
        self.coins = 0

    
    def update_collision(self, active_sprites: pygame.sprite.Group):
        for player in active_sprites.sprites():
            if player.rect.bottom >= TILE_SIZE * TILE_Y:
                # player.reset()
                self.has_lost = True

            for sprite in self.sprites():
                if sprite.rect.colliderect(player):
                    if sprite.value in self.interactives['silver key']:
                        self.has_key = True
                        self.item_sound.play()
                        sprite.kill()
                        continue

                    elif sprite.value in self.interactives['coin']:
                        self.coins += 1
                        self.coin_sound.play()
                        sprite.kill()
                        continue

                    elif sprite.value in (l:=self.interactives['closed exit']) and self.has_key:
                        self.has_won = True
                        sprite.value = self.interactives['open exit'][l.index(sprite.value)]

                sprite.image = pygame.transform.scale(pygame.image.load(f'Platformer/assets/tiles/{sprite.value}.png'), (TILE_SIZE, TILE_SIZE))
