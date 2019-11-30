import pyglet
import engine
from pyglet.window import mouse
from pyglet.gl import *
from os import path

gameFolder = path.dirname(__file__)
imageFolder = path.join(gameFolder, "images")


class StartButton:
    def __init__(self):
        self.button_image = pyglet.image.load(path.join(imageFolder, "startbutton.png"))
        self.button_image_sprite = pyglet.sprite.Sprite(self.button_image,
                                                        (window_width / 2) - 100, (window_height / 2) + 50)

    def draw(self):
        self.draw()


class QuitButton:
    def __init__(self):
        self.button_image = pyglet.image.load(path.join(imageFolder, "quitbutton.png"))
        self.button_image_sprite = pyglet.sprite.Sprite(self.button_image,
                                                        (window_width / 2) - 100, (window_height / 2) - 10)

    def draw(self):
        self.draw()


class Logo:
    def __init__(self):
        self.button_image = pyglet.image.load(path.join(imageFolder, "Logo.png"))
        self.button_image_sprite = pyglet.sprite.Sprite(self.button_image, (window_width / 2) - 100, 10)

    def draw(self):
        self.draw()


background_animation = pyglet.image.load_animation(path.join(imageFolder,'Mainmenu_background_big.gif'))
background_animation_sprite = pyglet.sprite.Sprite(background_animation)

window_width = background_animation_sprite.width
window_height = background_animation_sprite.height

window = pyglet.window.Window(window_width, window_height, 'Nightmare at DCS')
window.set_minimum_size(window_width, window_height)


@window.event
def on_mouse_press(x, y, button, modifier):
	if button == mouse.LEFT:
		if 170 <= x <= 370 and 410 <= y <= 460:
			window.close()
			engine.StartGame()
		elif 170 <= x <= 370 and 350 <= y <= 400:
			window.close()


@window.event
def on_draw():
	window.clear()
	background_animation_sprite.draw()
	Logo().button_image_sprite.draw()
	StartButton().button_image_sprite.draw()
	QuitButton().button_image_sprite.draw()


pyglet.app.run()
