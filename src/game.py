import pygame
import pickle
from pygame import Vector2

from settings import *
from .tiles import Tile
from .player import Player


class Game():
    def __init__(self):
        super().__init__()

        # General Settings
        self.win = pygame.display.get_surface()

        # Image Imports
        self.s = 'Platformer/assets/'
        self.bg = self.bg = pygame.transform.scale(pygame.image.load(f'{self.s}backgrounds/bg.png'), (1280, WIN_Y))

        # Game Settings
        self.level = 1
        self.actives = [1, 2, 3, 4, 5, 6, 7, 17, 18, 19, 20, 21, 22, 23, 33, 34, 35, 36, 37, 38, 39, 40, 50, 51, 52, 53, 54, 55, 65, 66, 67, 68, 69, 70, 71, 113, 114, 115, 116]
        self.visible_sprites = CameraGroup()
        self.active_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()

        # Music
        self.music = pygame.mixer.Sound(f'{self.s}sounds/music.mp3')
        self.music.play(loops=-1, fade_ms=2)


        
        with open(f'Platformer/level data/level{self.level}_data', 'rb') as file:
            self.world_data = pickle.load(file)

        self.load_world(self.world_data)

    def load_world(self, world_data):
        for y, row in enumerate(world_data):
            for x, value in enumerate(row):
                if value != 0:
                    image = pygame.transform.scale(pygame.image.load(f'{self.s}tiles/{value}.png'), (TILE_SIZE, TILE_SIZE))
                    pos = (TILE_SIZE * x, TILE_SIZE * y)
                    if value in self.actives:
                        Tile(pos, image, [self.visible_sprites, self.collision_sprites])
                    
                    else:
                        Tile(pos, image, [self.visible_sprites])

        self.player = Player((TILE_SIZE * 3, TILE_SIZE * TILE_Y - TILE_SIZE * 4), [self.visible_sprites, self.active_sprites], self.collision_sprites)

    def display_background(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(self.bg, (1280, 0))

    def setScene(self):
        self.display_background()

        self.active_sprites.update() 
        self.visible_sprites.custom_draw(self.player)


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        self.win = pygame.display.get_surface()

        self.offset = Vector2(0, 0)

        self.borders = {
            'left': 400,
            'right': 400,
            'top': 200,
            'bottom': 200
        }

        self.width = WIN_X - (self.borders['left'] + self.borders['right'])
        self.height = WIN_Y - (self.borders['top'] + self.borders['bottom'])

        self.camera_rect = pygame.Rect(TILE_SIZE, self.borders['top'], self.width, self.height)
    
    def custom_draw(self, player: pygame.sprite.Sprite):
        # pygame.draw.rect(self.win, 'white', pygame.Rect(*(self.camera_rect.topleft - self.offset), *self.camera_rect.size), 2)
        # pygame.draw.rect(self.win, 'white', pygame.Rect(*(player.rect.topleft - self.offset), *player.rect.size), 2)
        
        if player.rect.left < self.camera_rect.left:
            self.camera_rect.left = player.rect.left
        if player.rect.right > self.camera_rect.right:
            self.camera_rect.right = player.rect.right
        if player.rect.top < self.camera_rect.top:
            self.camera_rect.top = player.rect.top
        if player.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = player.rect.bottom

        # print(self.camera_rect.x)

        self.offset = pygame.math.Vector2(self.camera_rect.left - self.borders['left'], self.camera_rect.top - self.borders['top'])




        if self.camera_rect.x < 0:
            self.camera_rect.x = 0
            player.rect.x = 0
        elif self.camera_rect.x > (end:=TILE_X * TILE_SIZE):
            self.camera_rect.x = end
            player.rect.x = end



        for sprite in self.sprites():
            offset_pos = sprite.rect.topleft - self.offset
            self.win.blit(sprite.image, offset_pos)
