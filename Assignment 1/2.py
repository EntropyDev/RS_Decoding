import numpy as np
import random
import sympy
import itertools 
from sympy import Poly
from sympy import GF

x = sympy.symbols('x')

# Returns list of all polynomials upto degree s-1
def getList(s):
	lst = list(itertools.product([0, 1], repeat=s))
	poly_lst = []
	for each in lst:
		val = 0
		for i in range(s):
			val = val + each[i]*x**i
		poly_lst.append(val)
	return poly_lst

# Generates Finite field
def Finitefield(irp,d):
	lst = getList(d+1)
	poly_lst = []
	for each in lst:
		each = sympy.div(each,irp,domain=GF(2, symmetric=False))[1]
		if each not in poly_lst:
			poly_lst.append(each)
	return poly_lst

# Calucluates beta powers for the M(x)
def poly_mul(p1,p2,r,irp):
	for i in range(r):
		p2 = Poly(p1*p2,x,domain=GF(2, symmetric=False)).expr
		p2 = sympy.div(p2,irp,domain=GF(2, symmetric=False))[1]
	return p2

# Picks n disntict alpha values and evaluates M(x) at those values to get codeword	
def encode(n,k,ffield,msg,msg_poly,irp):
	codeword = []
	points = msg[:]
	while(len(points) != n):
		point = random.choice(ffield)
		if(point not in points):
			points.append(point)

	for i in range(n):
		val = sympy.expand(msg_poly.subs(x,points[i]))
		val = sympy.div(val,irp,domain=GF(2, symmetric=False))[1]
		codeword.append(ffield.index(val))
	return codeword


def run():
	irp = x**6 + x + 1
	ffield = Finitefield(irp,sympy.degree(irp,gen=x))
	beta = x**4 + x + 1

	print('##########')
	print('[n = 10,k = 4] code, M(X) = 1+β^2X.')
	msg = ffield[0:4]
	msg_poly = 1 + poly_mul(beta,x,2,irp)
	print("Message Polynomial after β substitution => ",msg_poly)
	codeword = encode(10,4,ffield,msg,msg_poly,irp)

	print("Message => ", codeword[0:4])
	print("Encoded Codeword => ", codeword)

	print('##########')
	print('[n = 20,k = 10] code, M(X) = β^4 +β^5X^3 +β^10X^9.')
	msg2 = ffield[0:10]
	msg_poly2 = sympy.expand(beta**4 + x**3*beta**5 + x**9*beta*10)
	msg_poly2 = sympy.div(msg_poly2,irp,domain=GF(2, symmetric=False))[1]
	print("Message Polynomial after β substitution => ",msg_poly2)
	codeword2 = encode(20,10,ffield,msg2,msg_poly2,irp)

	print("Message => ", codeword2[0:10])
	print("Encoded Codeword => ", codeword2)

	print('##########')
	print('[n = 50,k = 25] code, M(X) = β^20 +β^4X^8 +β^44X^12 + β^30X^14 + β^15X^18 + β^3X^23.')
	msg3 = ffield[0:25]
	msg_poly3 = sympy.expand(beta**20 + x**8*beta**4 + x**12*beta*44 + x**14*beta**30 + x**18*beta**15 + x**23*beta**3)
	msg_poly3 = sympy.div(msg_poly3,irp,domain=GF(2, symmetric=False))[1]
	print("Message Polynomial after β substitution => ",msg_poly3)
	codeword3 = encode(50,25,ffield,msg3,msg_poly3,irp)

	print("Message => ", codeword3[0:25])
	print("Encoded Codeword => ", codeword3)
	print('##########')
	return

run()