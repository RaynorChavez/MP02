# Sprites for the game
import pygame as pg
from settings import *
from os import path
from engine import *
vec = pg.math.Vector2

font_name = pg.font.match_font('arial')

class Text_inSprite(pg.sprite.Sprite):
	def __init__(self, surf, text, size, color, center = False):
		pg.sprite.Sprite.__init__(self)
		self.font = pg.font.SysFont(font_name, size)
		self.text_surface = self.font.render(text, True, color)
		if center == True:
			self.text_rect = self.text_surface.get_rect(center=surf.get_rect().center)
		else:
			self.text_rect = self.text_surface.get_rect().move(20,surf.get_rect().height/2 - self.text_surface.get_rect().height/2)
		surf.blit(self.text_surface, self.text_rect)

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.allSprites # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.walking = False
		self.currentFrame = 0
		self.lastUpdate = 0
		self.loadImages()
		self.image = game.playerImage
		self.image = pg.transform.scale(self.image, (int(tileSize*1.2), int(tileSize*1.4)))
		self.rect = self.image.get_rect()
		self.vel = vec(0, 0)
		self.pos = vec(x, y)

	def loadImages(self):
		gameFolder = path.dirname(__file__)
		imageFolder = path.join(gameFolder, "images")
		rightFolder = path.join(imageFolder, "Right")
		leftFolder = path.join(imageFolder, "Left")
		upFolder = path.join(imageFolder, "Up")
		downFolder = path.join(imageFolder, "Down")

		self.right = []
		for i in range(1, 5):
			fileName = f"Right00{i}.png"
			img = pg.image.load(path.join(rightFolder, fileName)).convert()
			img.set_colorkey(white)
			rightImage = pg.transform.scale(img, (int(tileSize*1.2), int(tileSize*1.4)))
			self.right.append(rightImage)

		self.left = []
		for i in range(1, 5):
			fileName = f"Left00{i}.png"
			img = pg.image.load(path.join(leftFolder, fileName)).convert()
			img.set_colorkey(white)
			leftImage = pg.transform.scale(img, (int(tileSize*1.2), int(tileSize*1.4)))
			self.left.append(leftImage)

		self.up = []
		for i in range(1, 5):
			fileName = f"Up00{i}.png"
			img = pg.image.load(path.join(upFolder, fileName)).convert()
			img.set_colorkey(white)
			upImage = pg.transform.scale(img, (int(tileSize*1.2), int(tileSize*1.4)))
			self.up.append(upImage)

		self.down = []
		for i in range(1, 5):
			fileName = f"Down00{i}.png"
			img = pg.image.load(path.join(downFolder, fileName)).convert()
			img.set_colorkey(white)
			downImage = pg.transform.scale(img, (int(tileSize*1.2), int(tileSize*1.4)))
			self.down.append(downImage)


	def getKeys(self):
		self.vel = vec(0, 0)
		keys = pg.key.get_pressed()
		if keys[pg.K_a] or keys[pg.K_LEFT]:
			self.vel.x = -playerSpeed 
		elif keys[pg.K_d] or keys[pg.K_RIGHT]:
			self.vel.x = playerSpeed
		elif keys[pg.K_w] or keys[pg.K_UP]:
			self.vel.y = -playerSpeed
		elif keys[pg.K_s] or keys[pg.K_DOWN]:
			self.vel.y = playerSpeed

	def update(self):
		self.animate()
		self.getKeys()
		self.pos += self.vel * self.game.dt
		self.rect.x = self.pos.x
		self.wallCollide("x")
		self.rect.y = self.pos.y
		self.wallCollide("y")
		#Clickme(self.game,self.rect.x, self.rect.y)

	def animate(self):
		now = pg.time.get_ticks()
		if self.vel.x != 0 or self.vel.y != 0:
			self.walking = True
		else:
			self.walking = False

		if self.walking:
			if now - self.lastUpdate > 200:
				self.lastUpdate = now
				self.currentFrame = (self.currentFrame + 1) % len(self.right)
				bottom = self.rect.bottom
				if self.vel.x > 0:
					self.image = self.right[self.currentFrame]
				elif self.vel.x < 0:
					self.image = self.left[self.currentFrame]
				elif self.vel.y > 0:
					self.image = self.down[self.currentFrame]
				elif self.vel.y < 0:
					self.image = self.up[self.currentFrame]
				self.rect = self.image.get_rect()
				self.rect.bottom = bottom

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

class Obstacle(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.walls # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

class Computer(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.walls, game.computers, game.interactable # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

class Door(pg.sprite.Sprite):
	def __init__(self, game, x, y, w, h):
		self.groups = game.walls, game.interactable, game.doorgroup # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

class Clickme(pg.sprite.Sprite):
	def __init__(self, game, x, y, myimage):
		self.groups = game.allSprites, game.clickme # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = myimage
		self.image = pg.transform.scale(self.image, (int(tileSize*2), int(tileSize/2)))
		self.image.set_colorkey(white)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.midbottom = (self.x, self.y)

		Text_inSprite(self.image, 'Press Space', 20, black)
		self.spawn_time = pg.time.get_ticks()

	def update(self):
		if pg.time.get_ticks() - self.spawn_time > 100:
			self.kill()


class Movable(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.walls # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.rect = pg.Rect(x, y, w, h)
		self.x = x
		self.y = y
		self.rect.x = x
		self.rect.y = y

class Timer(pg.sprite.Sprite):
	def __init__(self, game, start_time): 
		self.groups = game.timegroup # initializes what group you'll be part of
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((width, 20))
		self.image.set_colorkey(black)
		self.rect = self.image.get_rect()
		self.rect.midtop = (width/2,10)

		self.start_time = start_time
		self.remain_time = countdown_millisec
		

	def update(self):
		self.remain_time = countdown_millisec - (pg.time.get_ticks() - self.start_time)
		self.minutes = int(self.remain_time/1000/60)
		self.seconds = int(self.remain_time/1000 - self.minutes*60)
		self.image.fill(black)
		Text_inSprite(self.image, '{} : {}'.format(self.minutes,self.seconds), 35, red, True)
		#print('{} : {}'.format(self.minutes,self.seconds))

	def gameover(self):
		if self.remain_time <= 0:
			return True
		else:
			return False

class GameOverScreen(pg.sprite.Sprite):
	def __init__(self, game):
		self.groups = game.gameovergroup
		pg.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pg.Surface((width, height))
		self.image.set_colorkey(red)
		self.rect = self.image.get_rect()
		self.rect.midtop = (0,0)