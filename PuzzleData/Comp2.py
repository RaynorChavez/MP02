import pickle
import os

CompName = 'Comp2'

PuzzleSolved = False

PuzzleLines = [ 'Test Line 1',
				'      Test Line 2',
				'          Test Line 3',
				':',
				'Test Line 5'
				]


PuzzleAnswer = [4,3,2,1,0]


def SaveMyState(screentext):
	with open('Comp2.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp2.pickle"):
		if os.path.getsize('Comp2.pickle') > 0:
			with open('Comp2.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext
