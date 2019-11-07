import pygame
import random
import pyglet
import os

WIDTH = 360
HEIGHT = 480
FPS = 30

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nightmare in DCS")
clock = pygame.time.Clock()

#Sprite groups
all_sprites = pygame.sprite.Group()

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
	screen.fill(BLACK)
	all_sprites.draw(screen)
	pygame.display.flip() #Flips newly rendered frame to the viewer

pygame.quit()