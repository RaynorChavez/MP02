import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tileMap import *
sys.path.insert(0, r'/PuzzleData')
import PuzzleData.Comp0
import PuzzleData.Comp1
import PuzzleData.Comp2
import PuzzleData.Comp3
import PuzzleData.Comp4
import PuzzleData.Comp5

class ComputerUI(pg.sprite.Sprite):
	def __init__(self, game, oncomputer):
		self.reference_no = 0
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((tileSize_puzzle,tileSize_puzzle))
		self.image.fill(black)
		self.rect = self.image.get_rect()

		#Retrieves correct Computer File
		for i in range(len(game.comps)):
			if oncomputer == game.comps[i]:
				self.computer_file = 'Comp{}'.format(i)
				self.m = eval('PuzzleData.Comp{}'.format(i))
				self.reference_no = i

		#Initializes Variables
		self.variables()

		'''
		Here we need to initialize all GUI elements
		1. Left Pane 		- puzzlesprites, 
		2. Right Pane 		- puzzlesprites, 
		3. Instruction Box 	- puzzlesprites, 
		4. Monitor Border 	- puzzlesprites, 
		5. Screen 			- puzzlesprites, 
		6. Hard Disk Bay 	- puzzlesprites, 
		7. Code Buttons 	- puzzlesprites, buttons, codebuttons
		8. Delete Buttons 	- puzzlesprites, buttons, delbutton
		9. Save Button 		- puzzlesprites, buttons, savebutton
		'''

		self.LeftPane = Leftpane(self.game, )
		self.RightPane = Rightpane(self.game, )
		self.Instructions = Instructions(self.game, self.LeftPane.rect.centerx, tileSize_puzzle, self.reference_no)
		self.Monitor = Monitor(self.game, self.RightPane.rect.centerx, 0)
		self.Screen = CompScreen(self.game, self.RightPane.rect.centerx, 3*tileSize_puzzle)
		self.HDD = HardDiskBay(self.game, self.RightPane.rect.centerx, self.Monitor.rect.height)
		self.Delete = DeleteButton(self.game, self.HDD.rect.centerx + 250, self.HDD.rect.centery)
		
		#Generating button Sprites
		for index, puzzleline in enumerate(self.m.PuzzleLines):
			self.CodeButtons.append(CodeButton(self.game, self.LeftPane.rect.centerx, self.Instructions.rect.height + tileSize_puzzle*(len(self.CodeButtons) + 1) + tileSize_puzzle/2, puzzleline))

		#Loading Old Computer State
		start_len = len(self.playanswers)
		for i in range(len(self.playanswers)):
			self.add_Scr_line(self.playanswers[i], False)
			self.playanswers.pop()

		
	def variables(self):
		self.playanswers = self.m.LoadMyMemories()
		self.CodeButtons = []
		self.screen_text = []
		self.playable = True

	def update(self):
		self.save() #saves the state of the computer for when the player goes back to the computer
		if len(self.playanswers) == len(self.m.PuzzleAnswer):
			for i in range(len(self.playanswers)):
				if self.playanswers[i] != self.m.PuzzleAnswer[i]:
					break

			if i == (len(self.m.PuzzleAnswer)-1):
				self.correct_answer()
				self.playable = False
				Computer_States[self.reference_no] = 1

	def PuzzleSolved(self):
		if not self.playable:
			return self.reference_no
		else:
			return False
			
	def add_Scr_line(self, entity, Button = False):
		(x,y) = self.Screen.rect.midbottom

		if self.playable and (self.Screen.rect.y + tileSize/2*len(self.screen_text) + tileSize_puzzle/2) <= (y - tileSize_puzzle):
			if Button:
				index = self.CodeButtons.index(entity)
				entity.Clicked()
			else:
				index = entity
			self.playanswers.append(index)
			screen_txt_centerx = self.Screen.rect.centerx
			screen_txt_centery = self.Screen.rect.y + tileSize/2*len(self.screen_text) + tileSize_puzzle/2

			self.screen_text.append(ScreenText(self.game, screen_txt_centerx, screen_txt_centery, self.m.PuzzleLines[index]))

	def delete_Scr_line(self, entity):
		if self.playable and (len(self.screen_text) - 1) >= 0:
			self.screen_text[len(self.screen_text) - 1].kill()
			entity.Clicked()
			del self.screen_text[len(self.screen_text) - 1]
			del self.playanswers[len(self.playanswers) - 1]

	def correct_answer(self):
		(x,y) = self.Screen.rect.midbottom
		screen_txt_centerx = self.Screen.rect.centerx
		screen_txt_centery = self.Screen.rect.y + tileSize/2*len(self.screen_text) + tileSize_puzzle/2

		if (self.Screen.rect.y + tileSize_puzzle/2*len(self.screen_text) + tileSize_puzzle/2) <= (y - tileSize_puzzle) and self.playable:
			self.screen_text.append(ScreenText(self.game, screen_txt_centerx, screen_txt_centery, '--------------------------------------------------------------------------------'))
			self.screen_text.append(ScreenText(self.game, screen_txt_centerx, screen_txt_centery + tileSize/2, 'ANSWER CORRECT'))
			self.screen_text.append(ScreenText(self.game, screen_txt_centerx, screen_txt_centery + tileSize, 'PASSWORD: {}'.format(Door_Passwords[self.reference_no])))

	def save(self):
		self.m.SaveMyState(self.playanswers)
		
	
#Sprites
class Rightpane(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((right_pane_width, right_pane_height))
		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.rect.topleft = (0,0)

class Leftpane(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((left_pane_width, left_pane_height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.topright = (width,0)

class CompScreen(pg.sprite.Sprite):
	def __init__(self, game, x, y):

		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((screen_width,screen_height))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class CodeButton(pg.sprite.Sprite):
	def __init__(self, game, x, y, puzzleline):
		self.puzzleline = puzzleline
		self.load_images()
		self.click_time = pg.time.get_ticks()
		self.clicked = False

		self.groups = game.puzzlesprites, game.codebuttons, game.buttons # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.normal_img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

	def load_images(self):
		self.gameFolder = path.dirname(__file__)
		self.imageFolder = path.join(self.gameFolder, "images")
		self.normal_img = pg.image.load(path.join(self.imageFolder, 'codebutton.png')).convert()
		self.normal_img = pg.transform.scale(self.normal_img, (int(codebutton_width), int(codebutton_height)))
		self.clicked_img = pg.image.load(path.join(self.imageFolder, 'codebutton_clicked.png')).convert()
		self.clicked_img = pg.transform.scale(self.clicked_img, (int(codebutton_width), int(codebutton_height)))
		self.normal_img.set_colorkey(white)
		self.clicked_img.set_colorkey(white)
		Text_inSprite(self.normal_img, self.puzzleline, 20, greenbutton)

	def Clicked(self):
		self.image = self.clicked_img
		self.click_time = pg.time.get_ticks()
		self.clicked = True

	def update(self):
		now = pg.time.get_ticks()
		if (now - self.click_time) > 100 and self.Clicked:
			self.image = self.normal_img
			self.clicked = False

class ScreenText(pg.sprite.Sprite):
	def __init__(self, game, x, y, text):
		self.groups = game.puzzlesprites, game.screentext # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((stext_width,stext_height))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)
		Text_inSprite(self.image, text, 20, green)

class Monitor(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.load_images()
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.monitor_img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

	def load_images(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, "images")
		self.monitor_img = pg.image.load(path.join(imageFolder, 'Windows_Screen.png')).convert_alpha()
		self.monitor_img = pg.transform.smoothscale(self.monitor_img, (int(monitor_width), int(monitor_height)))
		self.monitor_img.set_colorkey(white)

class HardDiskBay(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.load_images()
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.hdd_img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

	def load_images(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, "images")
		self.hdd_img = pg.image.load(path.join(imageFolder, 'diskbay.png')).convert()
		self.hdd_img = pg.transform.scale(self.hdd_img, (int(hdd_width), int(hdd_height)))

class Instructions(pg.sprite.Sprite):
	def __init__(self, game, x, y, reference_no):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.gameFolder = path.dirname(__file__)
		self.imageFolder = path.join(path.join(self.gameFolder, "images"),"Instructions")
		self.inst_img = pg.image.load(path.join(self.imageFolder, 'Instructions{}.png'.format(reference_no))).convert()
		self.inst_img = pg.transform.smoothscale(self.inst_img, (int(instruction_width), int(instruction_height)))
		self.image = self.inst_img
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class DeleteButton(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites, game.delbuttons, game.buttons # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((delbutton_width,delbutton_height))
		self.image.fill(greenbutton)
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		Text_inSprite(self.image, 'Delete', 20, black, True)
		self.click_time = pg.time.get_ticks()
		self.clicked = False

	def Clicked(self):
		self.image.fill(greenbutton_clicked)
		self.click_time = pg.time.get_ticks()
		self.clicked = True

	def update(self):
		now = pg.time.get_ticks()
		if (now - self.click_time) > 100 and self.Clicked:
			self.image.fill(greenbutton)
			Text_inSprite(self.image, 'Delete', 20, black, True)
			self.clicked = False

class SaveButton(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites, game.delbuttons, game.buttons # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((codebutton_width,codebutton_height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)
		Text_inSprite(self.image, 'Save', 20, white)