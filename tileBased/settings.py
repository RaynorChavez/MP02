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
width = 1024
height = 768
FPS = 60
title = "Nightmare in DCS"
backgroundColor = pastelPink

# Map Grid Settings
tileSize = 64
tileSize_puzzle = 34
gridWidth = width / tileSize
gridHeight = height / tileSize

#Player settings
playerSpeed = 250
playerRotSpeed = 500
playerImg = "Down001.png"

#Constants for ComputerGUI

#Rightpane
right_pane_width = width*2/3
right_pane_height = height
right_pane_topleft = (0,0)

#Leftpane
left_pane_width = width/3
left_pane_height = height
left_pane_topright = (width, 0)

#Instruction Box
instruction_width = left_pane_width - 2*tileSize_puzzle
instruction_height = left_pane_width - 2*tileSize_puzzle

#Hard Disk Bay
hdd_width = right_pane_width
hdd_height = right_pane_height*1/5

#Monitor
monitor_width = right_pane_width
monitor_height = right_pane_height*4/5

#CodeButtons
codebutton_width = left_pane_width*2/3
codebutton_height = tileSize_puzzle/2

#CompScreen
screen_width = right_pane_width - 4*tileSize_puzzle
screen_height = monitor_height - 4*tileSize_puzzle

#ScreenText
stext_width = screen_width
stext_height = tileSize_puzzle/2

#Computer States
Computer_States = [0,0,0,0,0,0]
