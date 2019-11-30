"""
GAME OPTIONS/SETTINGS
"""
#Countdown
countdown_minutes = 30
countdown_millisec = countdown_minutes*60000

# You can define useful colors that you may need again eg.
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
black = (0, 0, 0)
black1 = (1, 0, 0)
white = (255, 255, 255)
pastelPink = (255, 209, 220)
pastelBlueGreen = (214, 239, 229)
pastelRed = (255, 105, 97)
pastelOrange = (255, 179, 71)
pastelYellow = (253, 253, 150)
pastelGreen = (152, 251, 152)
pastelBlue = (119, 158, 203)
pastelPurple = (177, 156, 217)
greenbutton = (0, 195,61)
greenbutton_clicked = (0,129,40)
brownish = (131,121,81)
codebutton_color = (148,183,0)

# video effects
LIGHTMASK = "light_350_soft.png"
vignette = (30, 30, 30)
lightRadius = (1100, 1100)

# Sound Effects
bgMusic = "Eerie Horror Music - Lurking in the Shadows (Slow Strings Composition).mp3"


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
playerSpeed = 500
playerRotSpeed = 500
playerImg = "Down001.png"

#Door Images
floor1 = "Floor.png"
floor2 = "Floor2.png"
floor3 = "Floor3.png"
floor4 = "Floor4.png"
floor5 = "Floor5.png"

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
instruction_width = left_pane_width - 1*tileSize_puzzle
instruction_height = left_pane_width - 3*tileSize_puzzle

#Hard Disk Bay
hdd_width = right_pane_width
hdd_height = right_pane_height*1/5

#Monitor
monitor_width = right_pane_width
monitor_height = right_pane_height*4/5

#CodeButtons
codebutton_width = left_pane_width*9/10
codebutton_height = tileSize_puzzle

#CodeButtons
delbutton_width = tileSize*1.5
delbutton_height = tileSize_puzzle*0.9

#CompScreen
screen_width = right_pane_width - 4*tileSize_puzzle
screen_height = monitor_height - 4*tileSize_puzzle

#ScreenText
stext_width = screen_width*8/9
stext_height = tileSize_puzzle/2

#Computer and Door States
Computer_States = [0,0,0,0,0,0]
Door_States = [0,0,0,0,0,0,0]


#Door Passwords
Door_Passwords = ['programming', 'is an', 'exercise','in','creative','thinking', 'programming is an exercise in creative thinking']