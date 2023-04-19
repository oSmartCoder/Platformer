import pygame

from main import Main


class MainMenu(Main):
    def __init__(self):
        super().__init__()

        # Assets Initialisation
        self.title = pygame.image.load('Platformer/assets/other/platformer.png')

        self.play = pygame.image.load('Platformer/assets/other/play.png')
        self.play_rect = self.play.get_rect(topleft=(self.win_x/2-self.play.get_width()/2, self.win_y/2-self.play.get_height()/2+60))

        # Variables
        self.bg_colour = (150, 200, 240)
        self.on_main_menu = True


    def background(self):
        self.win.fill(self.bg_colour)
        self.win.blit(self.title, (self.win_x/2-self.title.get_width()/2, self.win_y/2-self.title.get_height()/2-70))
    
    def ui(self):
        pos = pygame.mouse.get_pos()

        if self.play_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0]:
            self.on_main_menu = False
            
            print('clicked!')

        self.win.blit(self.play, self.play_rect)

        
    
        



