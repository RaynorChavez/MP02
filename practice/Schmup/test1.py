import pygame
import random
import pyglet
import os


WIDTH = 800
HEIGHT = 600
FPS = 30

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)\

#setup assets
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'img')

#Objects
class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_folder, "p3_stand.png")).convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.center = (WIDTH/2, HEIGHT/2)
		self.y_speed = 5

	def update(self):
		self.rect.x += 10
		self.rect.y += self.y_speed
		if self.rect.bottom > HEIGHT - 200:
			self.y_speed = -5
		if self.rect.top < 200:
			self.y_speed = 5
		if self.rect.left > WIDTH:
			self.rect.right = 0

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nightmare in DCS")
clock = pygame.time.Clock()

#Sprite groups
all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
#Game Loop
running = True
while running:
	clock.tick(FPS)

	#-----Events-----
	for event in pygame.event.get(): 
		#Terminate the program
		if event.type == pygame.QUIT: 
			running = False

	#-----Updating-----
	all_sprites.update()

	#-----Draw Section-----
	screen.fill(BLUE)
	all_sprites.draw(screen)
	pygame.display.flip() #Flips newly rendered frame to the viewer

pygame.quit()