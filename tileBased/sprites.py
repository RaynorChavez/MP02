# Sprites for the game
import pygame as pg
from settings import *
vec = pg.math.Vector2

font_name = pg.font.match_font('arial')


class Text_inSprite(pg.sprite.Sprite):
	def __init__(self, surf, text, size, color):
		pg.sprite.Sprite.__init__(self)
		self.font = pg.font.SysFont(font_name, size)
		self.text_surface = self.font.render(text, True, color)
		self.text_rect = self.text_surface.get_rect(center=surf.get_rect().center)
		surf.blit(self.text_surface, self.text_rect)


class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.allSprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = game.playerImage
		self.image = pg.transform.scale(self.image, (int(tileSize*0.7), int(tileSize*0.9)))
		self.rect = self.image.get_rect()
		self.vel = vec(0, 0)
		self.pos = vec(x, y) * tileSize

	def getKeys(self):
		self.vel = vec(0, 0)
		keys = pg.key.get_pressed()
		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.vel.x = -playerSpeed 
		if keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.vel.x = playerSpeed
		if keys[pg.K_w] or keys[pg.K_UP]:
			self.vel.y = -playerSpeed
		if keys[pg.K_s] or keys[pg.K_DOWN]:
			self.vel.y = playerSpeed

	def update(self):
		self.getKeys()
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		self.wallCollide("x")
		self.rect.y = self.pos.y
		self.wallCollide("y")

	def wallCollide(self, direction):
		if direction == "x":
			hits = pg.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				if self.vel.x > 0:
					self.pos.x = hits[0].rect.left - self.rect.width
				if self.vel.x < 0:
					self.pos.x = hits[0].rect.right
				self.vel.x = 0
				self.rect.x = self.pos.x
		if direction == "y":
			hits = pg.sprite.spritecollide(self, self.game.walls, False)
			if hits:
				if self.vel.y > 0:
					self.pos.y = hits[0].rect.top - self.rect.height
				if self.vel.y < 0:
					self.pos.y = hits[0].rect.bottom
				self.vel.y = 0
				self.rect.y = self.pos.y

class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.allSprites, game.walls # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((tileSize, tileSize))
		self.image.fill(pastelGreen)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = self.x * tileSize
		self.rect.y = self.y * tileSize

class Computer(pg.sprite.Sprite):
	def __init__(self, game, x, y, compnum):
		self.groups = game.allSprites, game.walls, game.computers, game.interactable # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((tileSize, tileSize))
		self.image.fill(blue)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = self.x * tileSize
		self.rect.y = self.y * tileSize
		Text_inSprite(self.image, str(compnum), 20, white)

	#def clicked():


class Clickme(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.allSprites, game.clickme
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((tileSize*2, tileSize/2))
		self.image.fill(white)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y - 1
		self.rect.centerx = self.x * tileSize + tileSize/2
		self.rect.y = self.y * tileSize
		Text_inSprite(self.image, 'Press Space', 20, black)


class Wall1(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.allSprites, game.walls, game.interactable # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((tileSize, tileSize))
		self.image.fill(red)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = self.x * tileSize
		self.rect.y = self.y * tileSize