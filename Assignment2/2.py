import random
import sympy
import itertools 
from sympy import Poly
from sympy import GF
import re
from collections import Counter

X = sympy.symbols('X')
file_object = open('output2.txt', 'a')

def getEvalVec(s):
	lst = list(itertools.product([0, 1], repeat=s))
	return lst

#generate error vector
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

#Majority Logic Decoding
def mjdecode(rx,m,r,indexs):
	msg_poly = 0
	for l in range(r, -1, -1):
		A = []
		for i in range(m):
			A.append(i)
		setA = set(A)
		subsets = itertools.combinations(A, l)
		for subset in subsets:
			setSub = set(subset)
			setEvl = setA - setSub
			setEvl = list(setEvl)
			setSub = list(setSub)
		
			bs = getEvalVec(m-l)
			mbs = []
			for b in bs:
				mb = 0
				evlK = getEvalVec(l)

				for evk in evlK:
					dum = [0]*m
					t=0
					u=0
					for each in setSub:
						dum[each] = evk[t]
						t =t +1 
					for each in setEvl:
						dum[each] = b[u]
						u = u+1
					v = ''
					for each in dum:
						v = v+str(each)

					indx = int(v,2)
					mb = (mb + rx[indx])%2

				mbs.append(mb)
			c = Counter(mbs)
			value, count = c.most_common()[0]

			if(value and count > pow(2,m-l)/2):
				
				Xs = sympy.symbols('X:'+str(m+1))
				Xs = Xs[1:]
				M = 1
				for i in range(len(setSub)):
					M = M * Xs[setSub[i]]
				msg_poly = msg_poly + M

				codeword = []
				for vector in indexs:
					vals = []
					for j in range(m):
						vals.append((Xs[j],vector[j]))
					evl = M.subs(vals)
					evl = evl % 2
					codeword.append(evl)

				for i in range(pow(2,m)):
					rx[i] = (rx[i]-codeword[i])%2

	codeword = []
	ans = ''
	for vector in indexs:
		vals = []
		for j in range(m):
			vals.append((Xs[j],vector[j]))

		evl = msg_poly.subs(vals)
		evl = evl%2
		ans = ans + ' ' + str(evl)
		codeword.append(evl)
	file_object.write('\nDecoded Codeword\n')
	file_object.write(ans)



def code(m,r):
	Xs = sympy.symbols('X:'+str(m+1))
	dmin = pow(2,m-r)
	er = str(int((dmin-1)/2))
	Xs = Xs[1:]
	msg_poly = input("RM("+str(m)+","+str(r)+") Enter Message Polynomial : ")
	M = sympy.sympify(msg_poly)
	file_object.write("\nUser Entered Message Polynomial : "+str(msg_poly))
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

	mjdecode(rx,m,r,eval_vectors)



def run():
	file_object.write("\n --- RM(5,1) --- \n")
	code(5,1)
	file_object.write("\n\n --- RM(10,4) --- \n")
	code(10,4)
	file_object.write("\n\n --- RM(15,1) --- \n")
	code(15,1)
	file_object.write("\n\n --- RM(20,10) --- \n")
	# code(20,10)
	file_object.close()

run()