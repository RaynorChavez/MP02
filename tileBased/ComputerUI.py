import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tileMap import *


class ComputerUI(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.puzzlesprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((width,height))
		self.image.fill(black)
		self.rect = self.image.get_rect()
