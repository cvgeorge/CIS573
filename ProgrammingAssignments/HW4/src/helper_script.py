

def myFunc(f0, f1, f2, f3):

	factor1 = [1.5, 1.5]
	factor2 = [0.3, 0.7, 2.9, 0.1]
	factor3 = [2.8, 1.2, 0.2, 2.8]
	factor4 = [1.5, 2.5, 1.1, 0.9]

	return factor1[f0] * factor2[2 * f2 + f1] * factor3[2 * f0 + f2] * factor4[2 * f2 + f3]


for a in range(2):
	for b in range(2):
		for c in range(2):
			for d in range(2):
				print str(myFunc(a, b, c, d)) + " + ",
