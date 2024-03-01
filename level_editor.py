import pygame
import pickle
import os, sys
from math import floor
from typing import Tuple
from pygame.locals import *

from settings import *


class Editor:
	def __init__(self):
		self.s = './assets/'
		
		# Pygame Inits
		pygame.init()
		pygame.font.init()
		pygame.display.set_caption('Level Editor')
		pygame.display.set_icon(pygame.image.load(f'{self.s}other/favicon.png'))
		self.clock = pygame.time.Clock()
		self.FPS = 999

		self.tile_size = 50
		self.margin_bottom = 100
		self.size = self.win_x, self.win_y = 1400, 600
		self.win_tile_x, self.win_tile_y = (num / self.tile_size for num in self.size)
		self.win = pygame.display.set_mode((self.win_x, self.win_y + self.margin_bottom))
		
		self.bg = pygame.transform.scale(pygame.image.load(f'{self.s}backgrounds/bg.png'), (1280, self.win_y))

		self.tiles = 0
		self.hotbar_data = [0 for _ in range(10)]
		self.inputs = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]
		self.save_button = Button(self.win, pygame.image.load(f'{self.s}other/save button.png'), (100, self.win_y + self.margin_bottom - 70))
		self.load_button = Button(self.win, pygame.image.load(f'{self.s}other/load button.png'), (200, self.win_y + self.margin_bottom - 70))
		self.up_arrow = Button(self.win, pygame.transform.scale(pygame.image.load(f'{self.s}other/up arrow.png'), (40, 40)), (300, self.win_y + self.margin_bottom - 92))
		self.down_arrow = Button(self.win, pygame.transform.scale(pygame.image.load(f'{self.s}other/down arrow.png'), (40, 40)), (300, self.win_y + self.margin_bottom - 47))

		self.world_data = [[0 for _ in range(TILE_X)] for _ in range(TILE_Y)]
		self.clicked = False
		self.set_value = 0                
		self.world_shift_x, self.world_shift_y = 0, 0
		self.shift_vel = 20

		# Margin Rect
		self.margin_rect = pygame.Rect(0, self.win_y, self.win_x, self.margin_bottom)

		self.level = 1

	def display_text(self, text, pos, font='Futura', font_size=24, colour='white') -> None:
		image = pygame.font.SysFont(font, font_size).render(text, 1, colour)
		self.win.blit(image, pos)

	def display_background(self):
		self.win.blit(self.bg, (0, 0))
		self.win.blit(self.bg, (1280, 0))
	
	def get_shift_values(self) -> Tuple[int, int]:
		shiftx = self.world_shift_x / self.tile_size * -1 # change in world_shift
		shifty = TILE_Y - (-self.world_shift_y / self.tile_size * -1) - self.win_tile_y
		return shiftx, shifty

	def create_grid(self):
		for x in range(TILE_X): # Top to bottom
			pygame.draw.line(self.win, (211, 211, 211), (self.tile_size * x + self.world_shift_x, 0), (self.tile_size * x + self.world_shift_x, self.win_y))
		
		for y in range(TILE_Y): # Left to right
			pygame.draw.line(self.win, (211, 211, 211), (0, self.win_y - self.tile_size * y + self.world_shift_y), (self.win_x, self.win_y - self.tile_size * y + self.world_shift_y))
	
	def update_mouse(self):
		pos = _, posy = pygame.mouse.get_pos()
		keys = pygame.key.get_pressed()

		absx, absy = (num / self.tile_size for num in pos)

		shiftx, shifty = self.get_shift_values()

		x = floor(absx + shiftx)
		y = floor(absy + shifty)

		if pygame.mouse.get_pressed()[0] and posy <= self.win_y and not self.clicked:
			self.clicked = True
			
			self.world_data[y][x] -= 1

			if self.world_data[y][x] < 0:
				self.world_data[y][x] = 160

		elif pygame.mouse.get_pressed()[2] and posy <= self.win_y and not self.clicked:
			self.clicked = True
			self.world_data[y][x] += 1
			if self.world_data[y][x] > 160:
				self.world_data[y][x] = 0
		
		elif pygame.mouse.get_pressed()[1] and posy <= self.win_y and not self.clicked:
			self.world_data[y][x] = self.set_value

		elif not any(pygame.mouse.get_pressed()):
			self.clicked = False

		for i, key in enumerate(self.inputs):
			if keys[key] and posy <= self.win_y:
				self.hotbar_data[i] = self.world_data[y][x]

	def update_world(self):
		tt_tiles = 0
		for y, row in enumerate(self.world_data):
			t_tiles = 0
			if any(row):
				tiles = 0
				for x, value in enumerate(row):
					if value != 0:
						tiles += 1
						
						# actual actual position in surface (even if its not displayed on window) regardless of all the diff factors like shifts etc
						
						image = pygame.transform.scale(pygame.image.load(f'{self.s}tiles/{value}.png'), (self.tile_size, self.tile_size))
						self.win.blit(image, (self.tile_size * x + self.world_shift_x, y * self.tile_size - (self.tile_size * TILE_Y - self.win_y) + self.world_shift_y))
				t_tiles += tiles
			
			tt_tiles += t_tiles
			
		self.tiles = tt_tiles

	def camera_scroll(self):
		keys = pygame.key.get_pressed()

		shiftx, shifty = self.get_shift_values()

		if (keys[pygame.K_a] or keys[pygame.K_LEFT]) and shiftx > 0:
			self.world_shift_x += self.shift_vel
		if (keys[pygame.K_d] or keys[pygame.K_RIGHT]) and shiftx < TILE_X - self.win_tile_x:
			self.world_shift_x -= self.shift_vel
		if (keys[pygame.K_w] or keys[pygame.K_UP]) and shifty > 0:
			self.world_shift_y += self.shift_vel
		if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and shifty < TILE_Y - self.win_tile_y:
			self.world_shift_y -= self.shift_vel
	
	def display_margin(self):
		pygame.draw.rect(self.win, (48, 140, 207), self.margin_rect)
		pygame.draw.rect(self.win, 'white', self.margin_rect, 1)

	def button_detection(self):
		file_path = f'Platformer/level data/level{self.level}_data'

		if self.save_button.update():
			with open(file_path, 'wb') as file:
				pickle.dump(self.world_data, file)
		
		if self.load_button.update() and os.path.exists(file_path):
			with open(file_path, 'rb') as file:
				self.world_data = pickle.load(file)
		
		if self.up_arrow.update() and self.level < 999:
			self.level += 1
		if self.down_arrow.update() and self.level > 1:
			self.level -= 1
	
	def update_hotbars(self):
		mouse_pos = pygame.mouse.get_pos()

		for i, value in enumerate(self.hotbar_data):
			pos = posx, posy = self.win_x / 3 - 30 + (self.tile_size + 20) * i, self.win_y + self.margin_bottom / 2 - self.tile_size / 2

			if pygame.mouse.get_pressed()[1] and pygame.Rect(posx, posy, self.tile_size, self.tile_size).collidepoint(mouse_pos):
				self.set_value = value

			if value != 0:
				image = pygame.transform.scale(pygame.image.load(f'{self.s}tiles/{value}.png'), (self.tile_size, self.tile_size))
				self.win.blit(image, pos)

			pygame.draw.rect(self.win, 'white', pygame.Rect(posx - 8, posy - 8, self.tile_size + 16, self.tile_size + 16), 2, border_radius=10)
	
	def update(self):
		self.display_background()
		self.create_grid()
		self.update_world()
		self.update_mouse()
		self.camera_scroll()
		
		self.display_margin()
		self.display_text(f'Level {self.level}', (20, self.win_y + self.margin_bottom / 2 - 6))
		self.display_text(f'FPS: {round(self.clock.get_fps())}  TILES: {self.tiles}', (5, 5))
		self.button_detection()
		self.update_hotbars()

	def loop(self):
		while True:

			self.update()
			
			pygame.display.update()
			self.clock.tick(self.FPS)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()


class Button:
	def __init__(self, surface, image, pos):
		self.surface = surface
		self.image = image
		self.rect = self.image.get_rect(topleft=pos)
		self.clicked = False

	def update(self):
		pos = pygame.mouse.get_pos()
		action = False

		if self.rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] and not self.clicked:
			action = True
			self.clicked = True
			
		if not pygame.mouse.get_pressed()[0]:
			self.clicked = False
		
		self.surface.blit(self.image, self.rect)

		return action


if __name__ == '__main__':
	editor = Editor()
	editor.loop()