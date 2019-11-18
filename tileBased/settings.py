"""
GAME OPTIONS/SETTINGS
"""

# You can define useful colors that you may need again eg.
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
pastelPink = (255, 209, 220)
pastelBlueGreen = (214, 239, 229)
pastelRed = (255, 105, 97)
pastelOrange = (255, 179, 71)
pastelYellow = (253, 253, 150)
pastelGreen = (152, 251, 152)
pastelBlue = (119, 158, 203)
pastelPurple = (177, 156, 217)

# initialize the dimension of your screen
width = int(1024)
height = int(768)
FPS = 60
title = "Tile Based Game"
backgroundColor = pastelPink
dynamic_width = int(width/1024)		#Fix this (for the Computer UI)
dynamic_height = int(height/768)	#Fix this (for the Computer UI)

# Map Grid Settings
tileSize = int(34)
gridWidth = width / tileSize
gridHeight = height / tileSize

#Player settings
playerSpeed = 350
playerRotSpeed = 300
playerImg = "tile005.png"

