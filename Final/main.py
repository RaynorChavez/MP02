import pyglet
import engine
from pyglet.window import mouse
from pyglet.gl import *
from os import path



gameFolder = path.dirname(__file__)
imageFolder = path.join(gameFolder, "images")

window = pyglet.window.Window(500,500)
x, y = window.get_location()
window.set_location(x + 390, y + 50)

class StartGameButton(pyglet.sprite.Sprite):
	def __init__(self, width,height):
		img = pyglet.image.load(path.join(imageFolder, "start1.png"))
		pyglet.sprite.Sprite.__init__(self, img, x = 250 - width/2, y = 100 - height/2)

class Logo(pyglet.sprite.Sprite):
	def __init__(self, width,height):
		img = pyglet.image.load(path.join(imageFolder, "logo.png"))
		pyglet.sprite.Sprite.__init__(self, img, x = 250 - width/2, y = 300 - height/2)


@window.event
def on_draw():
	glClearColor(0, 0, 0, 0)
	glClear(GL_COLOR_BUFFER_BIT)
	StartGame_Button.draw()
	Logo.draw()

@window.event
def on_mouse_press(x,y,button,modifiers):
	if button == mouse.LEFT:
		#print('left mouse button clicked')
		#print(x,y)
		if (150 <= x <= 350) and (67 <= y <= 133):
			#print('you clicked start game')
			window.close()
			engine.StartGame()
			#print('end')


StartGame_Button = StartGameButton(200,65)
Logo = Logo(200,200)
pyglet.app.run()