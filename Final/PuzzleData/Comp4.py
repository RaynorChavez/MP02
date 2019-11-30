import pickle
import os

CompName = 'Comp4'

PuzzleSolved = False

PuzzleLines = [ 'for char in inputStr:',
				'inputStr = "pynativepynvepynative"',
				'print(countDict)',
				'   count = inputStr.count(char)',
				'   countDict[char]=count',
				'countDict = dict()',
				]


PuzzleAnswer = [1,5,0,3,4,2]


def SaveMyState(screentext):
	with open('Comp4.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp4.pickle"):
		if os.path.getsize('Comp4.pickle') > 0:
			with open('Comp4.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext