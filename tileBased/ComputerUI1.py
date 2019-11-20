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
				#print(self.computer_file)
				self.m = eval('PuzzleData.Comp{}'.format(i))
				#print(self.m.CompName)
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
		self.Instructions = Instructions(self.game, self.LeftPane.rect.centerx, tileSize_puzzle)
		self.Monitor = Monitor(self.game, self.RightPane.rect.centerx, 0)
		self.Screen = CompScreen(self.game, self.RightPane.rect.centerx, 2*tileSize_puzzle)
		self.HDD = HardDiskBay(self.game, self.RightPane.rect.centerx, self.Monitor.rect.height)
		self.Delete = DeleteButton(self.game, self.HDD.rect.centerx, self.HDD.rect.y)
		
		#Generating button Sprites
		for index, puzzleline in enumerate(self.m.PuzzleLines):
			self.CodeButtons.append(CodeButton(self.game, self.LeftPane.rect.centerx, self.Instructions.rect.height + tileSize_puzzle*(len(self.CodeButtons) + 1) + tileSize_puzzle/2))
			Text_inSprite(self.CodeButtons[index].image, puzzleline, 20, white)

		#Loading Old Computer State
		start_len = len(self.playanswers)
		for i in range(len(self.playanswers)):
			self.add_Scr_line(self.playanswers[i], False)
			self.playanswers.pop()

		
	def variables(self):
		self.playanswers = self.m.LoadMyMemories()
		#print('playanswers', self.playanswers)
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
				#self.game.doors[i].kill()
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
			else:
				index = entity
			self.playanswers.append(index)
			self.screen_text.append(ScreenText(self.game, self.Screen.rect.centerx, self.Screen.rect.y + tileSize/2*len(self.screen_text) + tileSize_puzzle/2))
			Text_inSprite(self.screen_text[len(self.screen_text)-1].image, self.m.PuzzleLines[index], 20, green)

	def delete_Scr_line(self):
		if self.playable and (len(self.screen_text) - 1) >= 0:
			self.screen_text[len(self.screen_text) - 1].kill()
			del self.screen_text[len(self.screen_text) - 1]
			del self.playanswers[len(self.playanswers) - 1]

	def correct_answer(self):
		(x,y) = self.Screen.rect.midbottom

		if (self.Screen.rect.y + tileSize_puzzle/2*len(self.screen_text) + tileSize_puzzle/2) <= (y - tileSize_puzzle) and self.playable:
			self.screen_text.append(ScreenText(self.game, self.Screen.rect.centerx, self.Screen.rect.y + tileSize/2*len(self.screen_text) + tileSize/2))
			Text_inSprite(self.screen_text[len(self.screen_text)-1].image, 'YOUR ANSWER IS CORRECT', 30, green)

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
		self.image.fill(pastelBlue)
		self.rect = self.image.get_rect()
		self.rect.topright = (width,0)


class CompScreen(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((screen_width,screen_height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class CodeButton(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites, game.codebuttons, game.buttons # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((codebutton_width,codebutton_height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class ScreenText(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites, game.screentext # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((stext_width,stext_height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class Monitor(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((monitor_width,monitor_height))
		self.image.fill(pastelBlueGreen)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class HardDiskBay(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((hdd_width, hdd_height))
		self.image.fill(red)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class Instructions(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((instruction_width, instruction_height))
		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)

class DeleteButton(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.puzzlesprites, game.delbuttons, game.buttons # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((codebutton_width,codebutton_height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (x,y)
		Text_inSprite(self.image, 'Delete', 20, white)

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