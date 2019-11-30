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
import importlib

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

	def draw_text(self, text, font_name, size, color, x, y, align="nw"):
		font = pg.font.Font(font_name, size)
		text_surface = font.render(text, True, color)
		text_rect = text_surface.get_rect()
		if align == "nw":
			text_rect.topleft = (x, y)
		if align == "ne":
			text_rect.topright = (x, y)
		if align == "sw":
			text_rect.bottomleft = (x, y)
		if align == "se":
			text_rect.bottomright = (x, y)
		if align == "n":
			text_rect.midtop = (x, y)
		if align == "s":
			text_rect.midbottom = (x, y)
		if align == "e":
			text_rect.midright = (x, y)
		if align == "w":
			text_rect.midleft = (x, y)
		if align == "center":
			text_rect.center = (x, y)
		self.screen.blit(text_surface, text_rect)

	def loadData(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, "images")
		mapFolder = path.join(gameFolder, "maps")
		soundFolder = path.join(gameFolder, "SFX")
		fontFolder = path.join(gameFolder, "Fonts")

		# Map loading
		self.map = TiledMap(path.join(mapFolder, "map.tmx"))
		self.mapImg = self.map.makeMap()
		self.mapRect = self.mapImg.get_rect()

		# Image Loading
		self.playerImage = pg.image.load(path.join(imageFolder, playerImg)).convert()
		self.floor1Image = pg.image.load(path.join(imageFolder, floor1)).convert_alpha()
		self.floor2Image = pg.image.load(path.join(imageFolder, floor2)).convert_alpha()
		self.floor3Image = pg.image.load(path.join(imageFolder, floor3)).convert_alpha()
		self.floor4Image = pg.image.load(path.join(imageFolder, floor4)).convert_alpha()
		self.floor5Image = pg.image.load(path.join(imageFolder, floor5)).convert_alpha()
		self.floor1Image.set_colorkey(white)
		self.floor2Image.set_colorkey(white)
		self.floor3Image.set_colorkey(white)
		self.floor4Image.set_colorkey(white)
		self.floor5Image.set_colorkey(white)
		self.playerImage.set_colorkey(white)

		# Fog of war
		self.fog = pg.Surface((width, height))
		self.fog.fill(vignette)
		self.lightMask = pg.image.load(path.join(imageFolder, LIGHTMASK)).convert_alpha()
		self.lightMask = pg.transform.scale(self.lightMask, lightRadius)
		self.lightRect = self.lightMask.get_rect()

		# Sound Loading
		pg.mixer.music.load(path.join(soundFolder, bgMusic))

		# Fonts loading
		self.titleFont = path.join(fontFolder, "Old School Adventures.ttf")


		self.clickme_img = pg.image.load(path.join(imageFolder, 'clickme.png')).convert()
		
		
	def new(self):
		# Game restart
		self.comps = [""]*6
		self.doors = [""]*7
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
				if tileObject.name == f"computer {i}":
					self.comps[i] = Computer(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
				if tileObject.name == f"door {i}":
					self.doors[i] = Door(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)
			if tileObject.name == "door 6":
				self.doors[6] = Door(self, tileObject.x, tileObject.y, tileObject.width, tileObject.height)

		self.timer = Timer(self, self.start_time)
		#self.clickmetest = Clickme(self, 5, 5, self.clickme_img)

		self.camera = Camera(self.map.width, self.map.height)
		self.darkMode = True
		self.pause = False


	def run(self):
		# Game loop
		self.playing = True
		pg.mixer.music.play(loops = -1)
		pg.mixer.music.set_volume(0.35)
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			if not self.pause:
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
				if event.key == pg.K_p and event.key == (pg.K_LCTRL or pg.KRCTRL):
					self.pause = not self.pause
			if event.type == pg.MOUSEBUTTONUP:
      				self.mouseclick = pg.mouse.get_pos()
			for textbox in self.textbox:
				textbox.handle_event(event)
      				

	def update(self):
		# Game loop - update

		if self.timer.gameover():
			print('quitting')
			self.playing = False
			self.timer.kill()
		if not self.CompON and self.playing: #Freezes all sprites within the game except puzzlesprites
			self.allSprites.update()
			self.darkMode = True
		else:
			self.darkMode = False
		if self.playing:
			self.puzzlesprites.update()
			self.timer.update()


		#If puzzle is solved on Computer x, corresponding door is killed
		for i in range(7):
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

	def renderFog(self):
		# Draws the lightmask gradient onto fog image
		self.fog.fill(vignette)
		self.lightRect.center = self.camera.apply(self.player).center
		self.fog.blit(self.lightMask, self.lightRect)
		self.screen.blit(self.fog, (0,0), special_flags = pg.BLEND_MULT)

	def draw(self):
		# Game loop - draw
		#self.screen.fill(backgroundColor)
		self.screen.blit(self.mapImg, self.camera.applyRect(self.mapRect))

		for i in range(7):
			if Door_States[i] == 1:
				if i == 0:
					self.mapImg.blit(self.floor1Image, (832, 576))
				elif i == 1:
					self.mapImg.blit(self.floor1Image, (832, 1984))
				elif i == 2:
					self.mapImg.blit(self.floor2Image, (1664, 2368))
				elif i == 3:
					self.mapImg.blit(self.floor3Image, (3328, 1152))
				elif i == 4:
					self.mapImg.blit(self.floor4Image, (4544, 896))
				elif i == 5:
					self.mapImg.blit(self.floor4Image, (5120, 896))
				elif i == 6:
					self.mapImg.blit(self.floor5Image, (2752, 2560))

		for sprite in self.allSprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		for sprite in self.puzzlesprites:
			self.screen.blit(sprite.image, sprite.rect)
		
		
		for sprite in self.gameovergroup:
			self.screen.blit(sprite.image, sprite.rect)

		if self.darkMode:
			self.renderFog()

		for textbox in self.textbox:
			textbox.draw(self.screen)

		for sprite in self.timegroup:
			self.screen.blit(sprite.image, sprite.rect)

		if self.pause:
			self.draw_text("PAUSED", self.titleFont, 105, white, width/2, height/2, align = "center")

		pg.display.flip() # ALWAYS DO THIS LAST *After you draw everything*

	def showStartScreen(self):
		# game splash / start screen
		pass

	def showGameOver(self):
		# Game over / continue
		###### DITO IPASOK ANG MAIN MENU ######
		print('gameover')
		self.quit()

def StartGame():
	g = Game()
	g.showStartScreen()

	while True:
		g.new()
		g.run()
		g.showGameOver()
	