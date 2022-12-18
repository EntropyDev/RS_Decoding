import random
import sympy
import itertools 
from sympy import Poly
from sympy import GF
import re

x = sympy.symbols('x')
y = sympy.symbols('y')

X = sympy.symbols('X')
Y = sympy.symbols('Y')

b = sympy.symbols('b')

def getList(s):
	lst = list(itertools.product([0, 1], repeat=s))
	poly_lst = []
	for each in lst:
		val = 0
		for i in range(s):
			val = val + each[i]*x**i
		poly_lst.append(val)
	return poly_lst

def Finitefield(irp,d):
	lst = getList(d+1)
	poly_lst = []
	for each in lst:
		each = sympy.div(each,irp,domain=GF(2, symmetric=False))[1]
		if each not in poly_lst:
			poly_lst.append(each)
	return poly_lst

def genF(beta,irp):
	field = []
	field.append(sympy.sympify('0'))
	field.append(sympy.sympify('1'))
	# field.append(beta)
	pol = sympy.sympify('1')
	for i in range(62):
		pol = Poly(pol*beta,x,domain=GF(2, symmetric=False)).expr
		pol = sympy.div(pol,irp,domain=GF(2, symmetric=False))[1]
		field.append(pol)
	return(field)

def encode(n,k,ffield,msg_poly,alphas,irp,beta):
	codeword = []
	# b = sympy.symbols('b')
	for i in range(n):
		val = sympy.expand(msg_poly.subs(x,alphas[i]))
		# val = sympy.expand(val.subs(b,beta))
		val = sympy.div(val,irp,domain=GF(2, symmetric=False))[1]
		codeword.append(ffield.index(val))
	return codeword


def getMsg(n,k,ffield,msg_poly,alphas,irp,beta):
	msg = []
	# b = sympy.symbols('b')
	for i in range(k):
		val = sympy.expand(msg_poly.subs(x,alphas[i]))
		# val = sympy.expand(val.subs(b,beta))
		val = sympy.div(val,irp,domain=GF(2, symmetric=False))[1]
		msg.append(ffield.index(val))
	return msg

def getRx(codeword,ffield,err):
	for each in err:
		new_val = random.choice(ffield)
		while(codeword[each-1] == new_val):
			new_val = random.choice(ffield)
		codeword[each-1] = ffield.index(new_val)
	return codeword

def genF(beta,irp):
	field = []
	field.append(sympy.sympify('0'))
	field.append(sympy.sympify('1'))
	# field.append(beta)
	pol = sympy.sympify('1')
	for i in range(62):
		pol = Poly(pol*beta,x,domain=GF(2, symmetric=False)).expr
		pol = sympy.div(pol,irp,domain=GF(2, symmetric=False))[1]
		field.append(pol)
	return(field)


########################################
###Gaussian Elimination implemented for solving Linear system of equations in terms of beta powers
#### Works
########################################

def isZero(el):
	if(el == sympy.sympify('0')):
		return 1
	return 0

def row_oper(i,t,j,A,ffield,beta,irp):
	# if(A[i,j] and A[t,j]):
	
	
	# sc_st = int(''.join(filter(str.isdigit, str(scalar))))
	ij_st = re.findall(r'[0-9]+', str(A[i,j]))
	tj_st = re.findall(r'[0-9]+', str(A[t,j]))
	if(ij_st and tj_st):
		ij_st = int(ij_st[0])
		tj_st = int(tj_st[0])
		# if(A[i,j] == 1):
		# 	diff = tj_st*(-1)
		# elif(A[t,j] == 1):
		# 	diff = ij_st
		# else:
		diff = ij_st-tj_st
		# print(ij_st,' / ', tj_st)
		if(diff>0):
			scalar = sympy.sympify("b**"+str(diff))
			# print("works")
			for l in range(18):
				dum = A[i,l]
				dum2 = A[t,l]
				op = dum - dum2*scalar
				op = sympy.expand(op.subs(b,beta))
				op = sympy.div(op,irp,domain=GF(2,symmetric=False))[1]
				if(ffield.index(op)):
					A[i,l] = sympy.sympify("b**"+str(ffield.index(op)))
				else:
					A[i,l] = sympy.sympify("0")
					# A[i,l] = op
		else:
			diff = diff*(-1)
			scalar = sympy.sympify("b**"+str(diff))
			# print("yes works")
			for l in range(18):
				dum = A[t,l]
				dum2 = A[i,l]
				op = dum - dum2*scalar
				op = sympy.expand(op.subs(b,beta))
				op = sympy.div(op,irp,domain=GF(2,symmetric=False))[1]
				if(ffield.index(op)):
					A[i,l] = sympy.sympify("b**"+str(ffield.index(op)))
				else:
					A[i,l] = sympy.sympify("0")
					# A[i,l] = op

def row_swap(i,t,A):
	for j in range(18):
		dum = A[i,j]
		A[i,j]=A[t,j]
		A[t,j] = dum


def Gauss(A,ffield,beta,irp):
	print("Performing Gaussian elmination")
	pivot = 0
	for i in range(10):
		
		for j in range(pivot):
			if(isZero(A[i,j])):
				continue
			else:
				t = j
				row_oper(i,t,j,A,ffield,beta,irp)

		if(isZero(A[i,i])):
			if(i+1 != 10):
				row_swap(i,i+1,A)
				i=i-1
		else:
			pivot = pivot+1
			continue
	return(A)

def interpolate(ffield,beta,irp,alphas,rx):
	print("let deg Y of Q be 2 and of X be 5")
	deg_y = 2
	deg_x = 5
	q_s = sympy.symbols('q:'+str((deg_y+1)*(deg_x+1)))

	Qxy = ''
	c = 0
	for i in range(deg_x+1):
		for j in range(deg_y+1):
			Qxy = Qxy + str(q_s[c]) + '*' + 'X**'+str(i) + '*' + 'Y**'+str(j) + "+"
			c = c+1

	Qxy = Qxy[:-1]
	Qxy = sympy.sympify(Qxy)
	print('Q(X,Y) =>', Qxy)
	print('##########')

	M = []
	for i in range(10):
		arr = []
		for j in range((deg_y+1)*(deg_x+1)):
			arr.append(0)
		M.append(arr)


	M = sympy.Matrix(M)
	# print(M)
	print("Coefficient Matrix of Q(X,Y) after Substiuting Q(alpha i, y(i)) => ")
	# Getting equations by Substiuting Q(alpha i, y(i)) = 0
	for i in range(10):
		eq = sympy.expand(Qxy.subs(X,alphas[i]))
		eq = sympy.expand(eq.subs(Y,ffield[rx[i]]))
		eq = sympy.div(eq,irp,domain=GF(2,symmetric=False))[1]
		for j in range((deg_y+1)*(deg_x+1)):
			g = ffield.index(eq.coeff(q_s[j]))
			if(g):
				M[i,j] = sympy.sympify('b**'+str(g-1))
			else:
				M[i,j] = sympy.sympify('0')

	B = []
	for i in range((deg_y+1)*(deg_x+1)):
		B.append(sympy.sympify("0"))
	B = sympy.Matrix(B)
	print(M)

	print('##########')
	M = Gauss(M,ffield,beta,irp)
	print("GE Done")
	# print(M)
	print('##########')
	print("Solving LE to find the Coefficients q0,q1,..q17")
	res = sympy.linsolve((M,B),q_s)
	res = list(list(res)[0])
	print("LE solved")
	print('##########')
	# print(res)
	
	########################################
#### Parsing of the result Not working properly because at the end  
#### not getting a correct Q(X,Y) interpolation
########################################
	print("Parsing..")
	answers = []
	for each in res:
		sa = sympy.sympify(each)
		sa_arr= []
		ans = []
		for i in range(len(q_s)):
			sa_arr.append(sa.coeff(q_s[i]))
		for i in range(len(sa_arr)):
			string = str(sa_arr[i])[1:-1]
			if( string.find(')/(') != -1):

				pos = string.find(')/(') + 3
				v = sympy.sympify(string[:pos-3])
				v = sympy.div(v,sympy.sympify("1"),domain=GF(2,symmetric=False))[0]
				v = sympy.expand(v.subs(b,beta))
				v = sympy.div(v,irp,domain=GF(2,symmetric=False))[1]
				# continue
				p = sympy.sympify(string[pos:])
				p = sympy.div(p,sympy.sympify("1"),domain=GF(2,symmetric=False))[0]
				p = sympy.expand(p.subs(b,beta))
				p = sympy.div(p,irp,domain=GF(2,symmetric=False))[1]

				if(v != 0 and p != 0):
					z = sympy.div(v,p,domain=GF(2,symmetric=False))[0]
					z = sympy.div(z,irp,domain=GF(2,symmetric=False))[1]
				else:
					z = sympy.sympify("0")
				z1 = ffield.index(z)
				if(z1):
					ans.append(sympy.sympify('b**'+str(z1-1)))
				else:
					ans.append(sympy.sympify('0'))
			else:
				
				sa_arr[i] = sympy.div(sa_arr[i]*b,b,domain=GF(2,symmetric=False))[0]
				z = sympy.expand(sa_arr[i].subs(b,beta))
				z = sympy.div(z,irp,domain=GF(2,symmetric=False))[1]
				z1 = ffield.index(z)
				if(z1):
					ans.append(sympy.sympify('b**'+str(z1-1)))
				else:
					ans.append(sympy.sympify('0'))
				# ans.append(sympy)
		answers.append(ans)
	print("Parsing done")
	print('##########')
	# print(answers)

	sols = []
	for each in answers:	
		sol_eq = sympy.sympify('0')
		for l in range(len(each)):
			sol_eq = sol_eq + q_s[l]*each[l]
			# print(Qxy)
		sol_eq = sympy.expand(sol_eq)
		sols.append(sol_eq)
	# return
	new_sol = []

	for i in range(18):
		exp = sympy.sympify('0')
		for j in range(len(q_s)):
			exp = exp + sols[i].coeff(q_s[j])
		exp = sympy.expand(exp.subs(b,beta))
		exp = sympy.div(exp,irp,domain=GF(2,symmetric=False))[1]
		ind = ffield.index(exp)
		if(ind):
			new_sol.append(sympy.sympify('b**'+str(ind-1)))
		else:
			new_sol.append(sympy.sympify('0'))

	for i in range(18):
		Qxy = sympy.expand(Qxy.subs(q_s[i],new_sol[i]))
	print('A solution for Q(X,Y) found =>', Qxy)
	return(Qxy)

	

def getMsgLst(s):
	# lst = []
	l = list(itertools.product([0, 1], repeat=s+1))
	poly_lst = []
	for each in l:
		val = 0
		for i in range(4):
			val = val + each[i]*X**i
		poly_lst.append(val)

	return poly_lst


def findFactors(Qxy,ffield,beta,irp,alphas,rx):
	print("Finding Factors ...")
	all_lst = []
	msg_poly_lst = getMsgLst(3)
	for msg_poly in msg_poly_lst:
		bg = Y - msg_poly
		q,r = sympy.div(Qxy,bg,domain=GF(2,symmetric=False))
		if(r!=0):
			continue
		else:
			all_lst.append(msg_poly)
	print(msg_poly)

	return

# def checkInterpol(Qxy,alphas,rx,beta,irp,ffield):
# 	Qxy = sympy.expand(Qxy.subs(b,beta))
# 	for i in range(len(alphas)):
# 		eq = sympy.expand(Qxy.subs(X,alphas[i]))
# 		eq = sympy.expand(eq.subs(Y,ffield[rx[i]]))
# 		eq = sympy.div(eq,irp,domain=GF(2,symmetric=False))[1]
# 		print(eq)

# 	return

def run():
	irp = x**6 + x + 1
	ffield = Finitefield(irp,sympy.degree(irp,gen=x))
	beta = x**5
	ffield = genF(beta,irp)
	alphas = ffield[:10]
	print('(n = 10,k = 4) code and M(x) = x chosen to generate codeword')
	msg_poly = x

	msg = getMsg(10,4,ffield,msg_poly,alphas,irp,beta)
	print('Message Vector =>', msg)
	codeword = encode(10,4,ffield,msg_poly,alphas,irp,beta)
	print('Codeword =>', codeword)
	print("Introducing 4 errors at positions 2,3,4,6. The number of errors is greater than (n-k)/2 .")
	rx = getRx(codeword,ffield,[2,3,4,6])
	print('Recieved Codeword => ',rx)
	print('##########')
	print("Interpolating Q(X,Y)...")
	Qxy = interpolate(ffield,beta,irp,alphas,rx)
	# Qxy = X**5*Y**2 + X**5*Y + X**5 + X**4*Y**2 + X**4*Y + X**4 + X**3*Y**2*b**16 + X**3*Y + X**3 + X**2*Y**2*b**8 + X**2*Y*b**16 + X**2*b**12 + X*Y*b**10 + X*b**27 + Y**2*b**28 + Y*b**35
	factors = findFactors(Qxy,ffield,beta,irp,alphas,rx)

	return

run()