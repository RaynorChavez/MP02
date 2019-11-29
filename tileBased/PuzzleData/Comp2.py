import pickle
import os

CompName = 'Comp2'

PuzzleSolved = False

PuzzleLines = [ 'n2 = int(input("Enter second number"))',
				'print("The result is", result)',
				'   product = num1 * num2',
				'   else:',
				'def multiplication_or_sum(num1, num2)',
				'   if (product < 1000):',
				'n1 = int(input("Enter first number"))',
				'      return product',
				'      return num1 + num2',
				'result = multiplication_or_sum(n1, n2)',
				]


PuzzleAnswer = [4,2,5,7,3,8,6,9,1]


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
