import random
import sympy
import itertools 
from sympy import Poly
from sympy import GF
import re

x = sympy.symbols('x')
b = sympy.symbols('b')
y = sympy.symbols('y')

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

# Generates Finite field using beta powers
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
	for i in range(n):
		val = sympy.expand(msg_poly.subs(x,alphas[i]))
		val = sympy.div(val,irp,domain=GF(2, symmetric=False))[1]
		codeword.append(val)
	return codeword

# Returns the message vector by substituting first k alpha values in message polynomial
def getMsg(n,k,ffield,msg_poly,alphas,irp,beta):
	msg = []
	for i in range(k):
		val = sympy.expand(msg_poly.subs(x,alphas[i]))
		val = sympy.div(val,irp,domain=GF(2, symmetric=False))[1]
		msg.append(val)
	return msg

# Returns the error positions by finding the roots of the error polynomial
def getError(n,k,alphas,err_poly,irp):
	err_pos = sympy.solve(err_poly)
	n_err = []
	for each in err_pos:
		if each < 0:
			each = each*(-1)
		n_err.append(each+1)
	err_pos = list(set(n_err))
	return err_pos

# returns a recieved vector by introducing error values at the error positions
def getRx(codeword,ffield,err):
	for each in err:
		new_val = random.choice(ffield)
		while(codeword[each-1] == new_val):
			new_val = random.choice(ffield)
		codeword[each-1] = new_val
	return codeword


########################################
###Gaussian Elimination implemented for solving Linear system of equations in terms of beta powers
#### Not working properly
########################################


# def isZero(el):
# 	if(el == sympy.sympify('0')):
# 		return 1
# 	return 0

# def row_oper(i,t,j,A,ffield,beta,irp,l):
# 	# if(A[i,j] and A[t,j]):
	
	
# 	# sc_st = int(''.join(filter(str.isdigit, str(scalar))))
# 	ij_st = re.findall(r'[0-9]+', str(A[i,j]))
# 	tj_st = re.findall(r'[0-9]+', str(A[t,j]))
# 	# ij_st = int((''.join(filter(str.isdigit, str(A[i,j])))?(''.join(filter(str.isdigit, str(A[i,j])))):0)
# 	# tj_st = int((''.join(filter(str.isdigit, str(A[t,j]))))?(''.join(filter(str.isdigit, str(A[t,j])))):0)
# 	ij_st = int(ij_st[0])
# 	tj_st = int(tj_st[0])
# 	print(ij_st,' / ',tj_st)
# 	# return
# 	if(ij_st and tj_st):
# 		ij_st = int(ij_st[0])
# 		tj_st = int(tj_st[0])
# 		print(ij_st,' / ',tj_st)
# 		return
# 		if(A[i,j] == 1):
# 			diff = tj_st*(-1)
# 		elif(A[t,j] == 1):
# 			diff = ij_st
# 		else:
# 			diff = ij_st-tj_st
# 		# print(ij_st,' / ', tj_st)
# 		if(diff>0):
# 			scalar = sympy.sympify("b**"+str(diff))
# 			# print("works")
# 			for l in range(l):
# 				dum = A[i,l]
# 				dum2 = A[t,l]
# 				op = dum - dum2*scalar
# 				op = sympy.expand(op.subs(b,beta))
# 				op = sympy.div(op,irp,domain=GF(2,symmetric=False))[1]
# 				if(ffield.index(op)):
# 					A[i,l] = sympy.sympify("b**"+str(ffield.index(op)))
# 				else:
# 					A[i,l] = sympy.sympify("0")
# 					# A[i,l] = op
# 		else:
# 			diff = diff*(-1)
# 			scalar = sympy.sympify("b**"+str(diff))
# 			# print("yes works")
# 			for l in range(l):
# 				dum = A[t,l]
# 				dum2 = A[i,l]
# 				op = dum - dum2*scalar
# 				op = sympy.expand(op.subs(b,beta))
# 				op = sympy.div(op,irp,domain=GF(2,symmetric=False))[1]
# 				if(ffield.index(op)):
# 					A[i,l] = sympy.sympify("b**"+str(ffield.index(op)))
# 				else:
# 					A[i,l] = sympy.sympify("0")
# 					# A[i,l] = op

# def row_swap(i,t,A,l):
# 	for j in range(l):
# 		dum = A[i,j]
# 		A[i,j]=A[t,j]
# 		A[t,j] = dum


# def Gauss(A,ffield,beta,irp,l):
# 	print("Performing Gaussian elmination")
# 	pivot = 0
# 	for i in range(l):
		
# 		for j in range(pivot):
# 			if(isZero(A[i,j])):
# 				continue
# 			else:
# 				t = j
# 				row_oper(i,t,j,A,ffield,beta,irp,l)

# 		if(isZero(A[i,i])):
# 			if(i+1 != l):
# 				row_swap(i,i+1,A,l)
# 				i=i-1
# 		else:
# 			pivot = pivot+1
# 			continue
# 	return(A)


# Decoding by getting M(X) using recieved vector, alpha values and finite field
# This function doesnot know the error polynomial and the message polynomial.
# Hence works at the decoder end
def decode(rx,ffield,alphas,irp,n,k,t,beta):
	print("Decoding...")
	# creates symbols for coefficients of E(X) and N(Xs) i.e e0,e1,..,n0,n1,..
	var_e = sympy.symbols('e:'+str(t))
	var_n = sympy.symbols('n:'+str(n-t))

	# creates E(Y) using those coefficients
	E = ''
	for i in range(t):
		E = E + str(var_e[i])+'*y**'+str(i) +' + '
	E = E + "y**"+str(t)
	E = sympy.sympify(E)

	# creates N(Y) using those coefficients
	N = ''
	for i in range(n-t-1):
		N = N + str(var_n[i])+'*y**'+str(i) +' + '
	N = N + str(var_n[n-t-1])+"*y**"+str(n-t-1)
	N = sympy.sympify(N)

	# substituting alpha i values in E(Y) and N(Y) and 
	# finding n equations rx(i)E(alpha i) - N(alpha i) = 0
	eqs = []
	for i in range(n):
		exp1 = sympy.expand(E.subs(y,alphas[i]))
		exp1 = sympy.div(exp1,irp,domain=GF(2, symmetric=False))[1]
		exp2 = sympy.expand(N.subs(y,alphas[i]))
		exp2 = sympy.div(exp2,irp,domain=GF(2, symmetric=False))[1]
		val = sympy.expand(rx[i]*(exp1) - exp2)
		val = sympy.div(val,irp,domain=GF(2, symmetric=False))[1]
		eqs.append(val)
	# creating a list of coefficients of E and N. Getting X matrix in AX=B
	symbs = []
	for each in var_e:
		symbs.append(each)
	for each in var_n:
		symbs.append(each)

	# Converting n equations to matrix for linear system solving
	G,H = sympy.linear_eq_to_matrix(eqs, symbs)
	A_lst = []
	for i in range(n):
		row = G.row(i)
		A_lst.append(row)


	Ary = []
	for i in range(n):
		arr = []
		for j in range(n):
			c = ffield.index(sympy.div(A_lst[i][j],irp,domain=GF(2, symmetric=False))[1])
			if(c != 0):
				arr.append(sympy.sympify("b**"+str(c-1)))
			else:
				arr.append(sympy.sympify("0"))
			
		Ary.append(arr)
	B = []
	for i in range(n):
		d = ffield.index(sympy.div(H.row(i)[0],irp,domain=GF(2, symmetric=False))[1])
		if(d != 0):
			B.append(sympy.sympify("b**"+str(d-1)))
		else:
			B.append(sympy.sympify("0"))
	
	A = sympy.Matrix(Ary)
	B = sympy.Matrix(B)
	
	# A = Gauss(A,ffield,beta,irp,len(Ary))
	# print(A)
	# return
	# Linear System of equations Solving
	print("LE solving...")
	res = sympy.linsolve((A,B),symbs)
	res = list(list(res)[0])
	print("LE solved")

	# Parsing the result of LE solution and getting the sol in terms of beta powers
	ans = []
	for i in range(n):
		string = str(res[i])[1:-1]
		if( string.find(')/(') != -1):

			pos = string.find(')/(') + 3
			v = sympy.sympify(string[:pos-3])
			v = sympy.div(v,sympy.sympify("1"),domain=GF(2,symmetric=False))[0]
			v = sympy.expand(v.subs(b,beta))
			v = sympy.div(v,irp,domain=GF(2,symmetric=False))[1]
			p = sympy.sympify(string[pos:])
			p = sympy.div(p,sympy.sympify("1"),domain=GF(2,symmetric=False))[0]
			p = sympy.expand(p.subs(b,beta))
			p = sympy.div(p,irp,domain=GF(2,symmetric=False))[1]

			if(v):
				z = sympy.div(v,p,domain=GF(2,symmetric=False))[0]
			else:
				z = sympy.sympify("0")
			z = sympy.div(z,irp,domain=GF(2,symmetric=False))[1]
			ans.append(str(ffield.index(z)))
			
		else:
			if(res[i] != sympy.sympify('0')):
				res[i] = sympy.div(res[i]*b,b,domain=GF(2,symmetric=False))[0]
			z = sympy.expand(res[i].subs(b,beta))
			z = sympy.div(z,irp,domain=GF(2,symmetric=False))[1]
			ans.append(str(ffield.index(z)))

	res = ans

	# substituting coefficient values in E(Y)
	E = ''
	for i in range(t):
		if(int(res[i])):
			E = E + str((res[i])) + '*y**' + str(i) + " + "
		else:
			E = E + str(res[i]) + '*y**' + str(i) + " + "
		
	E = E + "y**"+str(t)
	E = sympy.sympify(E)

	print('E => ',E)

	# substituting coefficient values in N(Y)
	N= ''
	for i in range(len(res)-t):
		if(int(res[i+t])):
			N = N + str(int(res[i+t])) + '*y**' + str(i) + " + "
		else:
			N = N + str((res[i+t])) + '*y**' + str(i) + " + "
	N=N[0:-2]
	N = sympy.sympify(N)

	print('N => ',N)

	# Finding M(Y) by dividing N(X)/E(X)
	M,r = sympy.div(N,E)
	# print(M)
	# return
	if(r != 0):
		print("Error occurred at LE solving. Please try again")
		return
	M = str(M)
	M = M.replace('y','x')
	M = sympy.sympify(M)

	print('M  =>',M)

	answer = encode(n,k,ffield,M,alphas,irp,beta)

	code_vector = ''
	for each in answer:
		code_vector = code_vector + ' ' + str(ffield.index(each))
	print("Decoded Vector => ", code_vector)

	return


def nkcode(n,k,beta,irp,ffield):
	print('##########')
	alphas = ffield[0:n]
	print("(Message polynomial must be of max degree ",str(k-1),") ")
	print("For ex: x, x**2, x**2 + x ")
	msg_poly = input("Enter Message Polynomial after substituting β values : ")
	msg_poly = sympy.sympify(msg_poly)
	print("Message Poly is => " + str(msg_poly))
	print("(Error polynomial must be of max degree ",str(int((n-k)/2)),") ")
	print("For ex: x, x**2 + 3*x + 2, x**2 + 8*x + 15 ")
	err_poly = input("Enter error polynomial : ")
	print("Error Poly is => "+err_poly)
	err_poly = sympy.sympify(err_poly)

	
	msg = getMsg(n,k,ffield,msg_poly,alphas,irp,beta)
	msg_vector = ''
	for each in msg:
		msg_vector = msg_vector + ' ' + str(ffield.index(each))
	print("Message vector => ",msg_vector)

	codeword = encode(n,k,ffield,msg_poly,alphas,irp,beta)
	code_vector = ''
	for each in codeword:
		code_vector = code_vector + ' ' + str(ffield.index(each))
	print("Codeword Vector => ", code_vector)

	err = getError(n,k,alphas,err_poly,irp)
	print('Error at positions => ',err)

	rx = getRx(codeword,ffield,err)
	rx_vector = ''
	for each in rx:
		rx_vector = rx_vector + ' ' + str(ffield.index(each))
	print("Recieved Vector =>", rx_vector)

	decode(rx,ffield,alphas,irp,n,k,len(err),beta)
	print('##########')



def run():
	irp = x**6 + x + 1
	ffield = Finitefield(irp,sympy.degree(irp,gen=x))
	beta = x**5
	ffield = genF(beta,irp)

	nkcode(10,4,beta,irp,ffield)
	nkcode(20,10,beta,irp,ffield)
	nkcode(50,25,beta,irp,ffield)


run()