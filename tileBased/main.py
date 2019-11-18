# Pygame template - skeleton for any new project

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tileMap import *
from ComputerUI import *

class Game():

	def __init__(self):
		# summary: Initialize game and create the window
		pg.init() # initializes pygame and gets it ready to go
		pg.mixer.init() # if you wish to add sound
		self.screen = pg.display.set_mode((width, height)) # this will display the window
		pg.display.set_caption(title)
		self.clock = pg.time.Clock() # keeps track of speed and how fast things are going
		self.loadData()
		self.CompON = False

	def loadData(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, "images")
		self.map = Map(path.join(gameFolder, "map.txt"))
		self.playerImage = pg.image.load(path.join(imageFolder, playerImg)).convert_alpha()

	def new(self):
		# Game restart
		compnum = 0
		self.comps = []
		self.allSprites = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		self.computers = pg.sprite.Group()
		self.clickme = pg.sprite.Group()
		self.interactable = pg.sprite.Group()
		self.puzzlesprites = pg.sprite.Group()
		for row, tiles in enumerate(self.map.data):
			for column, tile in enumerate(tiles):
				if tile == "W":
					Wall(self, column, row)
				if tile == "P":
					self.player = Player(self, column, row)
				if tile == 'C':
					self.comps.append(Computer(self, column, row, compnum))
					print(compnum, self.comps[compnum])
					compnum += 1
				if tile == 'I':
					Wall1(self, column, row)
		
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
		self.space = False
		for event in pg.event.get(): #for all events that occur
		# Checks for closing the window
			if event.type == pg.QUIT: # pygame.QUIT is just a pygame thing for closing window
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.CompUI.kill()
					self.CompON = False
				if event.key == pg.K_SPACE:
					self.space = True


	def update(self):
		# Game loop - update
		if not self.CompON: #Freezes all sprites within the game except puzzlesprites
			self.allSprites.update()
		self.puzzlesprites.update()
		#check if player hits an interactable and Spawns a Clickme Popup
		self.hits = pg.sprite.spritecollide(self.player,self.interactable, False, pg.sprite.collide_circle)
		for hit in self.hits:
			Clickme(self, hit.x, hit.y) #Calls a Clickme Popup
			if (self.computers in hit.groups) and self.space and not self.CompON: #Checks if a computer was hit and if spacebar is pressed
				self.CompON = True
				Text_inSprite(hit.image, 'Spaced', 20, black)
				self.CompUI = ComputerUI(self)


		#Checks if player is hitting something, if not, delete all objects in clickme group
		if len(self.hits) == 0:
			for sprite in self.clickme:
				sprite.kill()

		self.camera.update(self.player)

	def draw(self):
		# Game loop - draw
		self.screen.fill(backgroundColor)
		self.drawGrid()
		for sprite in self.allSprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))

		for sprite in self.puzzlesprites:
			self.screen.blit(sprite.image, sprite.rect)
			
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