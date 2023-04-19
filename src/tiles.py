import pygame
from pygame import Surface

from settings import TILE_SIZE


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: list, value: int):
        """
        Attributes for each individual tiles.
        """
        super().__init__(groups) # Appends tile to various groups associated with the tile

        self.value = value
        self.image = pygame.transform.scale(pygame.image.load(f'Platformer/assets/tiles/{self.value}.png'), (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)
        


        


    
    

