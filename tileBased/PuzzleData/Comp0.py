import pickle
import os

CompName = 'Comp0'

PuzzleSolved = False

PuzzleLines = [ 'V = 4.0/3.0*n1*n2**3',
				'n2 = 6.0',
				'n1 = 3.1415',
				'print("The volume of the sphere is: ", V)',
				]


PuzzleAnswer = [2,1,0,3]


def SaveMyState(screentext):
	with open('Comp0.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp0.pickle"):
		if os.path.getsize('Comp0.pickle') > 0:
			with open('Comp0.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext
