# Pygame template - skeleton for any new project

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tileMap import *


class Game():
	def __init__(self):
		# summary: Initialize game and create the window
		pg.init() # initializes pygame and gets it ready to go
		pg.mixer.init() # if you wish to add sound
		self.screen = pg.display.set_mode((width, height)) # this will display the window
		pg.display.set_caption(title)
		self.clock = pg.time.Clock() # keeps track of speed and how fast things are going
		self.loadData()

	def loadData(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, "images")
		mapFolder = path.join(gameFolder, "maps")

		self.map = TiledMap(path.join(mapFolder, "map.tmx"))
		self.mapImg = self.map.makeMap()
		self.mapRect = self.mapImg.get_rect()
		self.playerImage = pg.image.load(path.join(imageFolder, playerImg)).convert()
		self.playerImage.set_colorkey(white)
	
	def new(self):
		# Game restart
		self.allSprites = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		#for row, tiles in enumerate(self.map.data):
		#	for column, tile in enumerate(tiles):
		#		if tile == "W":
		#			Wall(self, column, row)
		#		if tile == "P":
		#			self.player = Player(self, column, row)

		for tileObject in self.map.tmxdata.objects:
			if tileObject.name == "player":
				self.player = Player(self, tileObject.x, tileObject.y)
			if tileObject.name == "wall":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "computer 0":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "computer 1":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "computer 2":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "computer 3":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "computer 4":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "computer 5":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			#if tileObject.name == "door 0":
				#Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			#if tileObject.name == "door 1":
				#Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			#if tileObject.name == "door 2":
				#Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			#if tileObject.name == "door 3":
				#Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			#if tileObject.name == "door 4":
				#Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			#if tileObject.name == "door 5":
				#Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
		self.camera = Camera(self.map.width, self.map.height)

	def run(self):
		# Game loop
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()

	def quit(self):
		pg.quit()
		sys.exit()

	def events(self):
		# Game loop - events
		for event in pg.event.get(): #for all events that occur
		# Checks for closing the window
			if event.type == pg.QUIT: # pygame.QUIT is just a pygame thing for closing window
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()

	def update(self):
		# Game loop - update
		self.allSprites.update()
		self.camera.update(self.player)

	def draw(self):
		# Game loop - draw
		#self.screen.fill(backgroundColor)
		self.drawGrid()
		self.screen.blit(self.mapImg, self.camera.applyRect(self.mapRect))
		for sprite in self.allSprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pg.display.flip() # ALWAYS DO THIS LAST *After you draw everything*

	def drawGrid(self):
		for x in range(0, width, tileSize):
			pg.draw.line(self.screen, pastelBlue, (x, 0), (x, height))
		for y in range(0, height, tileSize):
			pg.draw.line(self.screen, pastelBlue, (0, y), (width, y))

	def showStartScreen(self):
		# game splash / start screen
		pass

	def showGameOver(self):
		# Game over / continue
		pass

g = Game()

g.showStartScreen()

while True:
	g.new()
	g.run()
	g.showGameOver()