import pygame
from pygame import Surface


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, image: Surface, groups: list):
        """
        Attributes for each individual tiles.
        """
        super().__init__(groups)

        self.image = image
        self.rect = self.image.get_rect(topleft = pos)


    
    

