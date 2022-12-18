import random
import sympy
import itertools 
from sympy import Poly
from sympy import GF
import re
from collections import Counter
import numpy as np

X = sympy.symbols('X')
file_object = open('output3.txt', 'a')

def getEvalVec(s):
	lst = list(itertools.product([0, 1], repeat=s))
	return lst

def err_vector(e,m):
	lst = []
	while(len(lst)<e):
		p = random.randint(0,pow(2,m)-1)
		if p not in lst:
			lst.append(p)

	err_vect = []
	for i in range(pow(2,m)):
		if i not in lst:
			err_vect.append(0)
		else:
			err_vect.append(1)
	return err_vect

#get Hadamard 2^m matrix
def getH(m):
	H2 = np.array([[1,1],[1,-1]])
	H2m = np.array([[1,1],[1,-1]])
	for i in range(m-1):
		H2m = np.kron(H2,H2m)
	return H2m

#Hadamard Transform
def HT(H2m,y,m):
	res = []
	res_s = ''
	count = 0
	for i in range(pow(2,m)):
		s = 0
		for j in range(pow(2,m)):
			s = s + H2m[i,j]*y[j]
			count = count + 1
		res_s = res_s + ' ' + str(s)
		res.append(s)
	file_object.write('\n# Hadamard transform\n')
	file_object.write('\nC.Y = ')
	file_object.write(res_s)
	file_object.write('\nOperations = ')
	file_object.write(str(count))

#Fast Hadamard Transform
def FHT(H2m,y,m):
	H2 = np.array([[1,1],[1,-1]])
	count = 0
	Hm2 = np.identity(pow(2,m),int)
	res_s = ''

	for i in range(m,0,-1):
		I1 = np.identity(pow(2,int(m-i)),int)
		I2 = np.identity(pow(2,i-1),int)
		M = np.kron(H2,I2)
		M = np.kron(I1,M)

		ans = []
		for k in range(pow(2,m)):
			s = 0
			for l in range(pow(2,m)):
				if(M[k,l] != 0):
					s = s + M[k,l]*y[l]
					count = count + 1
			ans.append(s)
		for n in range(pow(2,m)):
			y[n] = ans[n]
	
	for i in range(len(y)):
		res_s = res_s + ' ' + str(y[i])

	file_object.write('\n\n# Fast Hadamard transform\n')
	file_object.write('\nC.Y = ')
	file_object.write(res_s)
	file_object.write('\nOperations = ')
	file_object.write(str(count))

	return(y,count)


#Decode RM(m,1) using Fast Hadamard Transform
def decode(m,r):
	Xs = sympy.symbols('X:'+str(m+1))
	Xs = Xs[1:]
	dmin = pow(2,m-r)
	er = str(int((dmin-1)/2))
	msg_poly = input("RM("+str(m)+","+str(r)+")Enter Message Polynomial : ")
	file_object.write("\nUser Entered Message Polynomial : "+str(msg_poly))
	M = sympy.sympify(msg_poly)
	e = input("Enter No of Errors less than "+er+" : ")
	file_object.write("\nNo of errors : "+str(e) + "(<"+er+")")
	eval_vectors = getEvalVec(m)
	codeword = []
	code_w = ''
	for vector in eval_vectors:
		vals = []
		for j in range(m):
			vals.append((Xs[j],vector[j]))
		evl = M.subs(vals)
		evl = evl%2
		code_w = code_w + ' '+ str(evl)
		codeword.append(evl)
	file_object.write('\nCodeword\n')
	file_object.write(code_w)
	print("Codeword\n",code_w)

	err_v = err_vector(int(e),m)
	err_vec = ''
	for each in err_v:
		err_vec = err_vec + ' ' + str(each)
	file_object.write('\nError Vector\n')
	file_object.write(err_vec)

	rx = []
	rx_v = ''
	for i in range(pow(2,m)):
		g = (err_v[i]+codeword[i])%2
		rx.append(g)
		rx_v = rx_v + ' ' + str(g)
	file_object.write('\nRecieved Vector\n')
	file_object.write(rx_v)
	print('Rx\n',rx_v)

	for i in range(len(rx)):
		if(rx[i] == 1):
			rx[i] = -1
		else:
			rx[i] = 1

	H = getH(m)

	res,count = FHT(H,rx,m)

	max1 = max(res)
	min1 = min(res)
	
	fans = []
	final = ''
	if(max1 >= (-1*min1)):
		for intg in H[res.index(max1)]:
			fans.append(intg)
			if(intg == -1):
				intg = 1
			else:
				intg = 0
			final = final+ ' ' +str(intg)
	else:
		
		for intg in H[res.index(min1)]:
			fans.append((-1*intg))
			intg = -1*intg
			if(intg == -1):
				intg = 1
			else:
				intg = 0

			final = final+ ' ' +str(intg)
	file_object.write("\nDecoded Codeword\n")
	file_object.write(final)


def run():
	H3 = getH(5)
	y = [1,1,-1,1,-1,1,-1,1,1,1,-1,1,-1,1,-1,1,1,1,-1,1,-1,1,-1,1,1,1,-1,1,-1,1,-1,1]
	HT(H3,y,5)
	res,count  = FHT(H3,y,5)
	file_object.write('\n\n --- RM(5,1) --- \n')
	decode(5,1)
	file_object.write('\n\n --- RM(10,1) --- \n')
	decode(10,1)
	file_object.close()


run()