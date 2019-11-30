import pickle
import os

CompName = 'Comp1'

PuzzleSolved = False

PuzzleLines = [ 'n3 = int( "%s%s%s" % (a,a,a) )',
				'a = int(input("Input an integer : "))',
				'print(n1 + n2 + n3)',
				'n1 = int( "%s" % a)',
				'n2 = int( "$s$s" % (a,a) )'
				]


PuzzleAnswer = [1,3,4,0,2]


def SaveMyState(screentext):
	with open('Comp1.pickle', 'wb') as f:
		pickle.dump(screentext, f)

def LoadMyMemories():
	screentext = []
	if os.path.exists("Comp1.pickle"):
		if os.path.getsize('Comp1.pickle') > 0:
			with open('Comp1.pickle', 'rb') as f:
				screentext = pickle.load(f)
	#print('screentext',screentext)
	return screentext