import pygame
from pygame.math import Vector2

from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: list, collision_sprites: pygame.sprite.Group):
        super().__init__(groups)

        # General Settings
        self.win = pygame.display.get_surface()
        self.visible_sprites = groups[0]

        # -- Player Surface --
        self.scale_factor = 2.3

        # Load Images + Sounds
        self.import_character_assets()
        self.collision_sprites = collision_sprites

        self.jump_sound = pygame.mixer.Sound('Platformer/assets/sounds/jump_sound.mp3')
        self.jump_sound.set_volume(0.8)

        # -- Player Attrs --
        self.pos = pos
        self.reset()
        self.vel = 6
        self.gravity = 0.8
        self.jump_vel = 16
    
    def import_character_assets(self):
        path = 'Platformer/assets/characters/player1/'

        self.animations = {
            'idle': [pygame.transform.scale((image := pygame.image.load(f'{path}idle{x}.png')), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for x in range(1, 5)],
            'run': [pygame.transform.scale((image := pygame.image.load(f'{path}run{x}.png')), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for x in range(1, 7)],
            'jump': [pygame.transform.scale((image := pygame.image.load(f'{path}jump{x}.png')), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for x in range(1, 9)],
            'run_particles': [pygame.transform.scale((image := pygame.image.load(f'{path}run_particles{x}.png')), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for x in range(1, 7)],
            'jump_particles': [pygame.transform.scale((image := pygame.image.load(f'{path}jump_particles{x}.png')), (image.get_width() * self.scale_factor, image.get_height() * self.scale_factor)) for x in range(1, 6)]
        }
    
    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        
        image = self.animations[self.status][int(self.frame_index)]

        if self.facing_right:
            self.image = image
        elif not self.facing_right:
            self.image = pygame.transform.flip(image, True, False)
    
    def animate_particles(self, status):
        if self.status == status:
            self.particle_frame_index += self.animation_speed
            if self.particle_frame_index >= len(self.animations[f'{status}_particles']):
                self.particle_frame_index = 0
            
            particle = self.animations[f'{status}_particles'][int(self.particle_frame_index)]

            if status == 'run':
                points = (self.rect.midleft, self.rect.midright)
            elif status == 'jump':
                points = (self.rect.bottomleft + Vector2(particle.get_width(), 0), self.rect.bottomright - Vector2(particle.get_width(), 0))

            if self.facing_right:
                pos = (points[0][0] - particle.get_width(), points[0][1]) - self.visible_sprites.offset
                self.win.blit(particle, pos)
            else:
                pos = points[1] - self.visible_sprites.offset
                self.win.blit(pygame.transform.flip(particle, True, False), pos)

    
    def user_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.facing_right = True
            self.status = 'run'
        elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.facing_right = False
            self.status = 'run'
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump_sound.play()
            self.direction.y = -self.jump_vel
            self.status = 'jump'
        
        if not (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and not (keys[pygame.K_a] or keys[pygame.K_LEFT]) and not keys[pygame.K_SPACE]:
            self.status = 'idle'

    def horizontal_collision(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.x < 0: 
                    self.rect.left = sprite.rect.right
                if self.direction.x > 0: 
                    self.rect.right = sprite.rect.left

    def vertical_collision(self):
        for sprite in self.collision_sprites.sprites():
            if sprite.rect.colliderect(self.rect):
                if self.direction.y > 0:
                    self.rect.bottom = sprite.rect.top
                    self.direction.y = 0
                    self.on_ground = True
                if self.direction.y < 0:
                    self.rect.top = sprite.rect.bottom
                    self.direction.y = 0

        if self.on_ground and self.direction.y != 0:
            self.on_ground = False

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    
    def check_borders(self):
        if self.rect.bottom >= TILE_SIZE * TILE_Y:
            self.reset()
    
    def reset(self):
        print('reset')
        self.status = 'idle'    
        self.facing_right = True
        self.animation_speed = 0.1
        self.frame_index = 0
        self.particle_frame_index = 0

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(topleft = self.pos)
        self.on_ground = False
        self.direction = Vector2()
    



    def update(self):
        self.user_input()
        self.rect.x += self.direction.x * self.vel
        self.horizontal_collision()
        self.apply_gravity()
        self.vertical_collision()
        self.check_borders()
        self.animate()
        self.animate_particles('run')
        self.animate_particles('jump')