import pickle
import os

CompName = 'Comp5'

PuzzleSolved = False

PuzzleLines = [ 'List = [1,1,2,2,4,6]',
				'print("Count of each item: ", countDict)',
				'for item in List:',
				'   else:',
				'   if (item in countDict):',
				'countDict = dict()',
				'      countDict[item] += 1',
				'      countDict[item] = 1',
				'print("Original list: ", List)',
				]


PuzzleAnswer = [0,8,5,2,4,6,3,7,1]


def SaveMyState(screentext):
	with open('Comp5.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp5.pickle"):
		if os.path.getsize('Comp5.pickle') > 0:
			with open('Comp5.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext
