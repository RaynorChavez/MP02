# Pygame template - skeleton for any new project

import pygame as pg
import sys
import os
from os import path
from settings import *
from sprites import *
from tileMap import *
from ComputerUI1 import *
from DoorUI import *

class Game():
	def __init__(self):
		#print('here1')
		self.mouseclick = (0,0)
		self.start_time = pg.time.get_ticks()

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
		mapFolder = path.join(gameFolder, "maps")

		self.map = TiledMap(path.join(mapFolder, "map.tmx"))
		self.mapImg = self.map.makeMap()
		self.mapRect = self.mapImg.get_rect()
		self.playerImage = pg.image.load(path.join(imageFolder, playerImg)).convert()
		self.playerImage.set_colorkey(white)
		self.clickme_img = pg.image.load(path.join(imageFolder, 'clickme.png')).convert()
		self.clickme_img = pg.transform.scale(self.clickme_img, (int(tileSize*2), int(tileSize/2)))
		self.clickme_img.set_colorkey(white)
	
	def new(self):
		# Game restart
		self.comps = [0,0,0,0,0,0]
		self.doors = [0,0,0,0,0,0]
		self.allSprites = pg.sprite.Group()
		self.walls = pg.sprite.Group()
		self.computers = pg.sprite.Group()
		self.clickme = pg.sprite.Group()
		self.interactable = pg.sprite.Group()
		self.puzzlesprites = pg.sprite.Group()
		self.codebuttons = pg.sprite.Group()
		self.controlbutton = pg.sprite.Group()
		self.buttons = pg.sprite.Group()
		self.screentext = pg.sprite.Group()
		self.delbuttons = pg.sprite.Group()
		self.savebuttons = pg.sprite.Group()
		self.doorgroup = pg.sprite.Group()
		self.textbox = pg.sprite.Group()
		self.timegroup = pg.sprite.Group()
		self.gameovergroup = pg.sprite.Group()

		for tileObject in self.map.tmxdata.objects:
			if tileObject.name == "player":
				self.player = Player(self, tileObject.x, tileObject.y)
			if tileObject.name == "wall":
				Obstacle(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			for i in range(6):
				if tileObject.name == "computer {}".format(i):
					self.comps[i] = Computer(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
				if tileObject.name == "door {}".format(i):
					self.doors[i] = Door(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)

		self.timer = Timer(self, self.start_time)

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
		#print('here3')
		self.space = False
		for event in pg.event.get(): #for all events that occur
		# Checks for closing the window
			if event.type == pg.QUIT: 
				for i in range(6):
					if os.path.exists("Comp{}.pickle".format(i)):
						os.remove("Comp{}.pickle".format(i))
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					for sprites in self.puzzlesprites:
						sprites.kill()
					self.CompON = False
				if event.key == pg.K_SPACE:
					self.space = True
			if event.type == pg.MOUSEBUTTONUP:
      				self.mouseclick = pg.mouse.get_pos()
			for textbox in self.textbox:
				textbox.handle_event(event)
      				

	def update(self):
		# Game loop - update

		if self.timer.gameover():
			self.playing = False
			self.timer.kill()
		if not self.CompON and self.playing: #Freezes all sprites within the game except puzzlesprites
			self.allSprites.update()
		if self.playing:
			self.puzzlesprites.update()
			self.timer.update()


		#If puzzle is solved on COmputer x, corresponding door is killed
		for i in range(6):
			if Door_States[i] == 1:
				self.doors[i].kill()

		#check if player clicks a codebutton in Computer GUI
		self.clickedbutton = [button for button in self.codebuttons if button.rect.collidepoint(self.mouseclick)]
		for button in self.clickedbutton:
			self.CompUI.add_Scr_line(button, True)
			self.mouseclick = (0,0)

		#check if player clicks a delbutton in Computer GUI
		self.clickedbutton = [button for button in self.delbuttons if button.rect.collidepoint(self.mouseclick)]
		for button in self.clickedbutton:
			self.CompUI.delete_Scr_line(button)
			self.mouseclick = (0,0)

		#check if player hits an interactable and Spawns a Clickme Popup
		self.hits = pg.sprite.spritecollide(self.player,self.interactable, False, pg.sprite.collide_circle)
		for hit in self.hits:
			Clickme(self, hit.rect.centerx, hit.rect.y, self.clickme_img) #Calls a Clickme Popup
			if (self.computers in hit.groups) and self.space and not self.CompON: #Checks if a computer was hit and if spacebar is pressed
				self.CompON = True
				self.CompUI = ComputerUI(self, hit)
			if (self.doorgroup in hit.groups) and self.space:
				self.DoorUI = DoorUI(self, hit)
				self.CompON = True

		#Checks if player is hitting something, if not, delete all objects in clickme group
		if len(self.hits) == 0:
			for sprite in self.clickme:
				sprite.kill()

		self.camera.update(self.player)

	def draw(self):
		# Game loop - draw
		#self.screen.fill(backgroundColor)
		self.drawGrid()
		self.screen.blit(self.mapImg, self.camera.applyRect(self.mapRect))
		for sprite in self.allSprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		for sprite in self.puzzlesprites:
			self.screen.blit(sprite.image, sprite.rect)
		for sprite in self.timegroup:
			self.screen.blit(sprite.image, sprite.rect)
		for textbox in self.textbox:
			textbox.draw(self.screen)
		for sprite in self.gameovergroup:
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
		###### DITO IPASOK ANG MAIN MENU ######
		self.kill()
		pass

g = Game()
g.showStartScreen()

while True:
	g.new()
	g.run()
	g.showGameOver()