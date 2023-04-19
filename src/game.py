import pygame
import pickle
from typing import Tuple

from settings import *
from .tiles import Tile
from .player import Player
from .groups import CameraGroup, InteractiveGroup


class Game:
    def __init__(self):
        self.win = pygame.display.get_surface()

        # Game Settings
        self.level = 1
        self.sprite_filters = {
            'collision': [1, 2, 3, 4, 5, 6, 7, 17, 18, 19, 20, 21, 22, 23, 33, 34, 35, 36, 37, 38, 39, 40, 50, 51, 52, 53, 54, 55, 65, 66, 67, 68, 69, 70, 71, 113, 114, 115, 116],
            'interactive': {
                'closed exit': [10, 26, 11, 27, 8],
                'open exit': [12, 28, 13, 29, 9],
                'coin': [158],
                'water': [129, 130, 131, 132, 133, 145, 146, 147, 148, 149],
                'ladder': [77, 93, 125],
                'death': [30, 47, 48],
                'heart': [140],
                'weapon': [141],
                'shield': [142],
                'silver key': [144],
                'golden key': [160],
                'gem': [156]           
            }
        }

        # Initialise Groups
        self.visible_sprites = CameraGroup() # Sprites that is visible to the screen
        self.active_sprites = pygame.sprite.Group() # Players and moving entities
        self.collision_sprites = pygame.sprite.Group() # Sprites that have collision with active sprites
        self.interactive_sprites = InteractiveGroup(self.sprite_filters['interactive']) # Sprites that interact with active sprites

        # Image Imports
        self.bg = pygame.transform.scale(pygame.image.load('Platformer/assets/backgrounds/bg.png'), (1280, WIN_Y))
        self.coin_image = pygame.transform.scale(pygame.image.load('Platformer/assets/tiles/%s.png' % self.sprite_filters['interactive']['coin'][0]), (TILE_SIZE, TILE_SIZE))
        
        # Sounds
        self.music = pygame.mixer.Sound('Platformer/assets/sounds/music.mp3')
        self.music.play(loops=-1, fade_ms=2)

        # Load world
        with open(f'Platformer/level data/level{self.level}_data', 'rb') as file:
            self.world_data = pickle.load(file)
        self.load_world(self.world_data)
    
    
    def display_text(self, text: str, pos: Tuple[int, int], font_size: int=40, colour: str='white') -> None:
        """
        Renders the text and blits it to surface.
        """

        font = pygame.font.Font('Platformer/assets/fonts/font.ttf', font_size)
        image = font.render(text, True, colour)
        self.win.blit(image, pos)

    def load_world(self, world_data):
        for y, row in enumerate(world_data):
            for x, value in enumerate(row):
                if value != 0:
                    pos = (TILE_SIZE * x, TILE_SIZE * y)
                    if value in [data for l in self.sprite_filters['interactive'].values() for data in l]: # Interactive
                        Tile(pos, [self.visible_sprites, self.interactive_sprites], value)

                    elif value in self.sprite_filters['collision']: # Collision
                        Tile(pos, [self.visible_sprites, self.collision_sprites], value) 
                    
                    else:
                        Tile(pos, [self.visible_sprites], value)
                    
        Player((TILE_SIZE * 3, TILE_SIZE * TILE_Y - TILE_SIZE * 4), [self.visible_sprites, self.active_sprites], self.collision_sprites, 'player1')
        Player((TILE_SIZE * 4, TILE_SIZE * TILE_Y - TILE_SIZE * 4), [self.visible_sprites, self.active_sprites], self.collision_sprites, 'player2')

    def display_background(self):
        self.win.blit(self.bg, (0, 0))
        self.win.blit(self.bg, (1280, 0))

    def setScene(self):
        self.display_background()

        self.active_sprites.update() 
        self.visible_sprites.custom_draw(self.active_sprites)

        self.interactive_sprites.update_collision(self.active_sprites)


        self.win.blit(self.coin_image, (10, 10))
        self.display_text(f'x{self.interactive_sprites.coins}', (TILE_SIZE + 16, 23))

        if self.interactive_sprites.has_won and self.level == 1:
            self.display_text('You win!', (550, 450))