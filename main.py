import pygame, sys
from pygame.locals import *

from src import Game
from settings import *

# Fix order of particles and objects: Add particles to the active_sprites group along with the Player

class Main:
    def __init__(self):
        # Pygame Inits
        pygame.init() 
        pygame.font.init()
        pygame.display.set_caption('Platformer')
        pygame.display.set_icon(pygame.image.load('./assets/other/favicon.png'))
        self.CLOCK = pygame.time.Clock()
        

        self.win = pygame.display.set_mode(SIZE)

        self.game = Game()

    def update(self):
        self.game.setScene()

    def loop(self):
        while True:
            self.update()

            pygame.display.update()
            self.CLOCK.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    main = Main()
    main.loop()


