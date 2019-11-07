#Jump Platform game
import pygame as pg
import random
import pyglet as pyg
import os
from settings import *

class Game:
	def __init__(self):
		#initialize game window
		pg.init()
		pg.mixer.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.running = True

	def new(self):
		#start a new game
		self.all_sprites = pg.sprite.Group()
		#self.player = Player()
		#self.all_sprites.add(self.player)
		self.run()

	def run(self):
		#game Loop
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()

	def update(self):
		#Game Loop Update
		self.all_sprites.update()

	def events(self):
		# Game Loop Events
		for event in pg.event.get(): 
			#Terminate the program
			if event.type == pg.QUIT: 
				self.playing = False
				self.running = False

	def draw(self):
		#Game Loop draw
		self.screen.fill(BLACK)
		self.all_sprites.draw(self.screen)
		pg.display.flip() #Flips newly rendered frame to the viewer

	def show_start_screen(self):
		# Game splash/start screen
		pass

	def show_go_screen(self):
		#game over/continue
		pass

g = Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()

pg.quit()