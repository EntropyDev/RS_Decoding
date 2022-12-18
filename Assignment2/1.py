import random
import sympy
import itertools 
from sympy import Poly
from sympy import GF
import re

X = sympy.symbols('X')
file_object = open('output1.txt', 'a')

def getEvalVec(s):
	lst = list(itertools.product([0, 1], repeat=s))
	return lst

def func1a(m,r):
	Xs = sympy.symbols('X:'+str(m+1))
	Xs = Xs[1:]
	# print(Xs)
	M = Xs[0] + Xs[1] + Xs[2] + Xs[3]
	eval_vectors = getEvalVec(m)
	codeword = []
	ans = ''
	for vector in eval_vectors:
		evl = M.subs([(Xs[0],vector[0]),(Xs[1],vector[1]),(Xs[2],vector[2]),(Xs[3],vector[3])])
		evl = evl%2
		codeword.append(evl)
		ans = ans + ' ' + str(evl)
	print("---- RM(5,1) ----")
	print('Message Polynomial ==>',M)
	print('Codeword ==>',codeword)
	file_object.write("---- RM(5,1) ----\nMessage Polynomial\n")
	file_object.write(str(M))
	file_object.write('\nCodeword\n')
	file_object.write(ans)
	# writefile.write("This is line B\n")


def func1b(m,r):
	Xs = sympy.symbols('X:'+str(m+1))
	Xs = Xs[1:]
	# print(Xs)
	M = Xs[0] * Xs[1] * Xs[2] * Xs[3]
	eval_vectors = getEvalVec(m)
	codeword = []
	wht = 0
	for vector in eval_vectors:
		evl = M.subs([(Xs[0],vector[0]),(Xs[1],vector[1]),(Xs[2],vector[2]),(Xs[3],vector[3])])
		evl = evl%2
		wht = wht + evl
		codeword.append(evl)
	print("---- RM(10,4) ----")
	print('Message Polynomial ==>',M)
	print('Minimum Weight ==>',wht)
	file_object.write("\n---- RM(10,4) ----\nMessage Polynomial\n")
	file_object.write(str(M))
	file_object.write('\nMinimum Weight\n')
	file_object.write(str(wht))
 
	# print(eval_vectors)

def func1c(m,r):
	Xs = sympy.symbols('X:'+str(m+1))
	Xs = Xs[1:]
	# print(Xs)
	M = Xs[3] + Xs[4] + Xs[7] + 1
	eval_vectors = getEvalVec(m)
	codeword = []
	ans = ''
	for vector in eval_vectors:
		evl = M.subs([(Xs[0],vector[0]),(Xs[1],vector[1]),(Xs[2],vector[2]),(Xs[3],vector[3]),(Xs[4],vector[4]),(Xs[5],vector[5]),(Xs[6],vector[6]),(Xs[7],vector[7]),(Xs[8],vector[8]),(Xs[9],vector[9]),(Xs[10],vector[10]),(Xs[11],vector[11]),(Xs[12],vector[12]),(Xs[13],vector[13]),(Xs[14],vector[14])])
		evl = evl%2
		ans = ans + ' ' + str(evl)
		codeword.append(evl)
	print("---- RM(15,1) ----")
	print('Message Polynomial ==>',M)
	print('Codeword ==>',codeword)
	file_object.write("\n---- RM(15,1) ----\nMessage Polynomial\n")
	file_object.write(str(M))
	file_object.write('\nCodeword\n')
	file_object.write(ans)
	# print(M)
	# print(codeword)

def func1d(m,r):
	Xs = sympy.symbols('X:'+str(m+1))
	Xs = Xs[1:]
	# Xs = set(Xs)
	X_s = set(Xs[0:10])
	subsets = itertools.combinations(X_s, 9)
	M = 0
	for each in subsets:
		M = M + each[0]*each[1]*each[2]*each[3]*each[4]*each[5]*each[6]*each[7]*each[8]
		# print(each[0])
	eval_vectors = getEvalVec(m)
	codeword = []
	ans = ''
	for vector in eval_vectors:
		evl = M.subs([(Xs[0],vector[0]),(Xs[1],vector[1]),(Xs[2],vector[2]),(Xs[3],vector[3]),(Xs[4],vector[4]),(Xs[5],vector[5]),(Xs[6],vector[6]),(Xs[7],vector[7]),(Xs[8],vector[8]),(Xs[9],vector[9]),(Xs[10],vector[10]),(Xs[11],vector[11]),(Xs[12],vector[12]),(Xs[13],vector[13]),(Xs[14],vector[14]),(Xs[15],vector[15]),(Xs[16],vector[16]),(Xs[17],vector[17]),(Xs[18],vector[18]),(Xs[19],vector[19])])
		evl = evl%2
		ans = ans + ' ' + str(evl)
		codeword.append(evl)
	# print("---- RM(20,10) ----")
	# print('Message Polynomial ==>',M)
	# print('Codeword ==>',codeword)
	file_object.write("\n---- RM(20,10) ----\nMessage Polynomial\n")
	file_object.write(str(M))
	file_object.write('\nCodeword\n')
	file_object.write(ans)

def run1():
	print("#")
	print("Running 1.a ======>")
	func1a(5,1)
	print("#")
	print("Running 1.b ======>")
	func1b(10,4)
	print("#")
	print("Running 1.c ======>")
	func1c(15,1)
	print("#")
	print("Running 1.d ======>")
	func1d(20,10)
	file_object.close()
	return

run1()