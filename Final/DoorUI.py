import pygame as pg
from os import path
from settings import *
from sprites import *


'''
What This script does:

1. This is the UI for the door. 
2. This script is called whenever a spacebar is clicked near a door
3. It shows the user a prompt to enter the password
4. If the password is correct, the door will save the state of its screen ('keep the user's text)
5. If the password entered is wrong, the door will tell the user that the password is wrong
6. escape key closes the doorUI
7. backspace deletes previos charaacter
'''

COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')

class DoorUI(pg.sprite.Sprite):
	def __init__(self, game, activated_door):
		self.reference_no = 0
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((width, height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.center = (width/2,height/2)

		#Retrieves Door reference number
		#Retrieves correct Computer File
		for i in range(len(game.doors)):
			if activated_door == game.doors[i]:
				self.reference_no = i

		self.Statusline = Status(self.game, 'Enter Password')
		self.Input = TextBox(self.game,self.reference_no,width/2,height/2,width*11/20,height*1/16)

	def update(self):
		if Door_States[self.reference_no] == 1:
			self.Statusline.kill()
			self.Statusline = Status(self.game, 'Password Correct')

class TextBox(pg.sprite.Sprite):
	def __init__(self, game, door_no, x, y, w, h, text=''):
		#print('textboxinitialized')
		self.groups = game.puzzlesprites, game.textbox # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.door_no = door_no
		self.game = game
		self.font = pg.font.SysFont(font_name, 32)
		self.image = pg.Surface((w,h))
		self.rect = self.image.get_rect()
		self.rect.center = (x,y)
		self.color = COLOR_INACTIVE
		self.text = text
		self.txt_surface = self.font.render(text, True, self.color)
		self.active = False


	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
			if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
				self.active = not self.active
			else:
				self.active = False
            # Change the current color of the input box.
			self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
		if event.type == pg.KEYDOWN:
			if self.active:
				if event.key == pg.K_RETURN:
                	#checks if submitted password is correct
					print(self.text)
					if self.text == Door_Passwords[self.door_no]:
						#print('you got it right')
						Door_States[self.door_no] = 1
					#else:
						#print('you got it wrong')
					self.text = ''
				elif event.key == pg.K_BACKSPACE:
					self.text = self.text[:-1]
				else:
					self.text += event.unicode
                # Re-render the text.
				self.txt_surface = self.font.render(self.text, True, self.color)

	def update(self):
		# Resize the box if the text is too long.
		#width = max(200, self.txt_surface.get_width()+10)
		#self.rect.w = width
		pass

	def draw(self, screen):
		# Blit the text.
		screen.blit(self.txt_surface, (self.rect.x+10, self.rect.y+13))
		# Blit the rect.
		pg.draw.rect(screen, self.color, self.rect, 2)


class Status(pg.sprite.Sprite):
	def __init__(self, game, status):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((width*5/6, 30))
		self.image.fill(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (width/2,height/2 - 80)
		Text_inSprite(self.image, status, 50, green, True)