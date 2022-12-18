import random
import sympy
import itertools
from sympy import Poly
from sympy import GF 

# Initializing symbol x in sympy
x = sympy.symbols('x')


# Picks a list of all binary combinations of length s.
# Used for generating plynomials of degree upto s-1. Returns a list of those polynomials
def getList(s):
	lst = list(itertools.product([0, 1], repeat=s))
	poly_lst = []
	for each in lst:
		val = 0
		for i in range(s):
			val = val + each[i]*x**i
		poly_lst.append(val)
	return poly_lst

# Checks if the polynomial is an irreducible polynomial or not
# Uses brute force method and checks if the polynomial has any factor other than 0,1 and itself
def irreducible(poly,d):
	lst = getList(d+1)
	for each in lst:
		if(each != 0 and each != 1 and poly != each):
			if(sympy.div(poly,each,domain=GF(2,symmetric=False))[1] == 0):
				return 0
	return 1

#Picks a random polynomial of degree 8 and checks if it is ireeducible.
# Loop stops when it finds one and returns the irreducible polynomial
def findIrp():
	b = 0
	while (b==0):
		choicelist = [0, 1]
		a = random.choices(choicelist, weights = [1, 1], k = 8)
		f = x**8 +a[7]*x**7 +a[6]*x**6 +a[5]*x**5 + a[4]*x**4 + a[3]*x**3 + a[2]*x**2 + a[1]*x + a[0]
		if(irreducible(f,sympy.degree(f,gen=x))):
			b=1
			return(f)

# Generates a finite field of polynomials using an irreducible polynomial and returns it
def Finitefield(irp,d):
	lst = getList(d+1)
	poly_lst = []
	for each in lst:
		each = sympy.div(each,irp,domain=GF(2, symmetric=False))[1]
		if each not in poly_lst:
			poly_lst.append(each)
	return poly_lst

# Checks if the polynomial is a primitive element or not
# It does this by generating the powers of the polynomials and check if it generates the finite field or not
def checkPrim(poly,ffield,irp):
	lst = ffield[:]
	new_poly = []
	new_poly = poly
	lst.remove(poly)
	lst.remove(0)
	lst.remove(1)
	for i in range(253):

		new_poly = Poly(poly*new_poly,x,domain=GF(2, symmetric=False)).expr
		new_poly = sympy.div(new_poly,irp,domain=GF(2, symmetric=False))[1]
		if new_poly in lst:
			lst.remove(new_poly)
		else:
			return 0
	if(lst == []):
		new_poly = Poly(poly*new_poly,x,domain=GF(2, symmetric=False)).expr
		new_poly = sympy.div(new_poly,irp,domain=GF(2, symmetric=False))[1]
		# print("beta power 255 = ", new_poly)
		# if(new_poly == sympy.sympify('1')):
		return 1

# Takes each element from finite field and checks if it is a primitive elements.
# It returns one when it finds one
def findprim(irp):
	ffield = Finitefield(irp,sympy.degree(irp,gen=x))
	for each in ffield:
		if(each !=0 and each!=1):
			# print("irreducible is", each)
			if(checkPrim(each,ffield,irp)):
				return each	

# Prints irreducible polynomial and checks beta powers
def run():
	irp = findIrp()
	print("Question 1.a :")
	print('Irreducible Polynomial found => ',irp)
	print('##########')

	beta = findprim(irp)
	print("Question 1.b :")
	print("Primtive element beta =>  ", beta)
	beta34 = beta
	for i in range(33):
		beta34 = Poly(beta*beta34,x,domain=GF(2, symmetric=False)).expr
		beta34 = sympy.div(beta34,irp,domain=GF(2, symmetric=False))[1]
	print("beta34 = ",beta34)
	beta20 = beta
	for i in range(19):
		beta20 = Poly(beta*beta20,x,domain=GF(2, symmetric=False)).expr
		beta20 = sympy.div(beta20,irp,domain=GF(2, symmetric=False))[1]
	print("beta20 = ",beta20)
	print('##########')
	beta54 = beta
	for i in range(53):
		beta54 = Poly(beta*beta54,x,domain=GF(2, symmetric=False)).expr
		beta54 = sympy.div(beta54,irp,domain=GF(2, symmetric=False))[1]
	print("beta54 = ",beta54)
	beta2034 = Poly(beta34*beta20,x,domain=GF(2, symmetric=False)).expr
	beta2034 = sympy.div(beta2034,irp,domain=GF(2, symmetric=False))[1]
	print("beta20 * beta34 = ",beta2034)
	print('##########')

run()