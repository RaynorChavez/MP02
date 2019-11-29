import pickle
import os

CompName = 'Comp3'

PuzzleSolved = False

PuzzleLines = [ '   middleIndex = int(len(sampleStr) /2)',
				'   middleThree = sampleStr[middleIndex-1:middleIndex+2',
				'   print("Middle three chr", middleThree)',
				'   print("Original String is", sampleStr)',
				'def getMiddlethreechr(sampleStr)',
				'getMiddlethreechr("JhonDipPeta)'
				]


PuzzleAnswer = [4,0,3,1,2,5]


def SaveMyState(screentext):
	with open('Comp3.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp3.pickle"):
		if os.path.getsize('Comp3.pickle') > 0:
			with open('Comp3.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext
