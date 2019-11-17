import pygame as pg 
from settings import *

class Map:
	def __init__(self, fileName):
		self.data = []
		with open(fileName, "rt") as f:
			for line in f:
				self.data.append(line.strip("\n"))


		self.tileWidth = len(self.data[0])
		self.tileHeight = len(self.data)
		self.width = self.tileWidth * tileSize
		self.height = self.tileHeight * tileSize

class Camera:
	def __init__(self, width, height):
		self.camera = pg.Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def update(self, target):
		x = -target.rect.x + int(width / 2) 
		y = -target.rect.y + int(height / 2)

		# Limit of scrolling Map

		x = min(0, x) # left screen
		y = min(0, y) # Top Screen
		x = max(-(self.width - width), x) # Right Screen
		y = max(-(self.height - height), y) # Bottom Screen
		self.camera = pg.Rect(x, y, self.width, self.height) 
