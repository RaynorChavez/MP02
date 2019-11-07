import pygame
import random
from os import path
import pyglet

WIDTH = 480
HEIGHT = 600
FPS = 60

#define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0,0, 255)
YELLOW = (255,255,0)

#initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nightmare in DCS")
clock = pygame.time.Clock()

#setup assets
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

#functions
font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
	font = pygame.font.Font(font_name,size)
	text_surface = font.render(text, True, WHITE)
	text_rect = text_surface.get_rect()
	text_rect.midtop = (x, y)
	surf.blit(text_surface, text_rect)

def newmob():
	m = mob()
	all_sprites.add(m)
	mobs.add(m)

def draw_shield_bar(surf, x, y, pct):
	if pct < 0:
		pct = 0
	BAR_LENGTH = 100
	BAR_HEIGHT = 10
	fill = (pct/100)*BAR_LENGTH
	outline_rect = pygame.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
	fill_rect = pygame.Rect(x,y,fill,BAR_HEIGHT)
	pygame.draw.rect(surf, GREEN, fill_rect)
	pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, x, y, lives,img):
	for i in range(lives):
		img_rect = img.get_rect()
		img_rect.x = x + 30*i
		img_rect.y = y
		surf.blit(img, img_rect)




#Objects

class Player(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.transform.scale(player_img, (50,38))
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.radius = 20
		self.rect.centerx = WIDTH / 2
		self.rect.bottom = HEIGHT - 10
		self.speedx = 0
		self.shield = 100
		self.shoot_delay = 250
		self.last_shot = pygame.time.get_ticks()
		self.lives = 3
		self.hidden = False
		self.hide_timer = pygame.time.get_ticks()

	def update(self):
		#unhide if hidden
		if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
			self.hidden = False
			self.rect.centerx = WIDTH / 2
			self.rect.bottom = HEIGHT - 10

		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -10
		if keystate[pygame.K_RIGHT]:
			self.speedx = 10
		if keystate[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedx
		if self.rect.right > WIDTH:
			self.rect.right = WIDTH
		if self.rect.left < 0:
			self.rect.left = 0

	def shoot(self):
		now = pygame.time.get_ticks()
		if now - self.last_shot > self.shoot_delay:
			self.last_shot = now
			bullet = Bullet(self.rect.centerx, self.rect.top)
			all_sprites.add(bullet)
			bullets.add(bullet)
			shoot_sound.play()

	def hide(self):
		#hide player temporarily
		self.hidden = True
		self.hide_timer = pygame.time.get_ticks()
		self.rect.center = (WIDTH/2, HEIGHT+200)

class mob(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image_orig = random.choice(meteor_images)
		self.image_orig.set_colorkey(BLACK)
		self.image = self.image_orig.copy()
		self.rect = self.image.get_rect()
		self.radius = int(self.rect.width *0.85 / 2)
		self.rect.x = random.randrange(WIDTH - self.rect.width)
		self.rect.y = random.randrange(-150, -100)
		self.speedy = random.randrange(1,8)
		self.speedx = random.randrange(-3,3)
		self.rot = 0
		self.rot_speed = random.randrange(-8,8)
		self.last_update = pygame.time.get_ticks()

	def rotate(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > 50:
			self.last_update = now
			self.rot = (self.rot + self.rot_speed) % 360
			new_image = pygame.transform.rotate(self.image_orig, self.rot)
			old_center = self.rect.center
			self.image = new_image
			self.rect = self.image.get_rect()
			self.rect.center = old_center

	def update(self):
		self.rotate()
		self.rect.x += self.speedx
		self.rect.y += self.speedy
		if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > (WIDTH +25):
			self.rect.x = random.randrange(WIDTH - self.rect.width)
			self.rect.y = random.randrange(-150, -100)
			self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = bullet_img
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.bottom = y
		self.speedy = -10

	def update(self):
		self.rect.y += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class Explosion(pygame.sprite.Sprite):
	def __init__(self, center, size):
		pygame.sprite.Sprite.__init__(self)
		self.size = size
		self.image = explosion_anim[self.size][0]
		self.rect = self.image.get_rect()
		self.rect.center = center
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = 75

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame += 1
			if self.frame == len(explosion_anim[self.size]):
				self.kill()
			else:
				center = self.rect.center
				self.image = explosion_anim[self.size][self.frame]
				self.rect = self.image.get_rect()
				self.rect.center = center

#Loading all game graphics
#background
background = pygame.image.load(path.join(img_dir, 'blue.jpg')).convert()
background_rect = background.get_rect()
#explosions
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
	filename = 'explosion0{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	img_lg = pygame.transform.scale(img, (75,75))
	explosion_anim['lg'].append(img_lg)
	img_sm = pygame.transform.scale(img, (32,32))
	explosion_anim['sm'].append(img_sm)
	filename = 'sonicExplosion0{}.png'.format(i)
	img = pygame.image.load(path.join(img_dir, filename)).convert()
	img.set_colorkey(BLACK)
	explosion_anim['player'].append(img)
#meteors
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png', 'meteorBrown_med1.png', 'meteorBrown_med2.png', 'meteorBrown_small1.png', 'meteorBrown_small2.png', 'meteorBrown_tiny1.png']
for img in meteor_list:
	meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
#player
player_img = pygame.image.load(path.join(img_dir, 'playerShip1_red.png')).convert()
#life (playermini)
player_mini_img = pygame.transform.scale(player_img, (25,19))
player_mini_img.set_colorkey(BLACK)
#bullet
bullet_img = pygame.image.load(path.join(img_dir, 'laserRed16.png')).convert()



#Loading all game sound
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'gun_shoot.wav'))
expl_sounds = []
for snd in ['Laser_Shoot1.wav', 'Laser_Shoot2.wav']:
	expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

#Sprite Groups
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

#initializing objects
player = Player()
all_sprites.add(player)
for i in range(8):
	newmob()

score = 0
pygame.mixer.music.play(loops = -1)
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

	#check to see if bullet hits a mob
	hits = pygame.sprite.groupcollide(mobs,bullets, True, True)
	for hit in hits:
		score += 50 - hit.radius
		random.choice(expl_sounds).play()
		expl = Explosion(hit.rect.center, 'lg')
		all_sprites.add(expl)
		newmob()

	#check for mob collision with player
	hits = pygame.sprite.spritecollide(player,mobs, True, pygame.sprite.collide_circle)
	for hit in hits:
		newmob()
		player.shield -= hit.radius*2
		expl = Explosion(hit.rect.center, 'sm')
		all_sprites.add(expl)
		if player.shield <= 0:
			death_explosion = Explosion(player.rect.center, 'player')
			all_sprites.add(death_explosion)
			player.hide()
			player.lives -= 1
			player.shield = 100

	#if player dead and explosion is finished
	if player.lives == 0 and not death_explosion.alive():
		running = False

	#-----Draw Section-----
	screen.fill(BLACK)
	screen.blit(background, background_rect)
	all_sprites.draw(screen)
	draw_text(screen, str(score), 18, WIDTH / 2, 10)
	draw_shield_bar(screen, 5, 5, player.shield)
	draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)
	pygame.display.flip() #Flips newly rendered frame to the viewer

pygame.quit()