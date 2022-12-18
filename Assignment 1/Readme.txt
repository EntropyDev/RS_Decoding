Name : Vaibhav Chimalgi
Roll no : 2020701010

Used Python 3, sympy for doing polynomial algebra in python

I was able to do only the first three questions. As I was getting wrong interpolation in q4, I couldnt solve q4 and q5. Although I did know the algorithm for q4, q5, I was not able to implement it because of errors in linear system of equations solving (to find coefficients of Q(x,y)).

Even in the q3 which decodes correctly for M(x) = x, x**2, x**2+x.
It fails for cases like M(x) = x+1

(This I suspect is due to incorrect parsing of sol for LEs for those cases because the algo works correctly for some cases meaning the algo logic is correct.)
(My algo is supposed to take M(x) after substituting beta values for a general M(x) with coefficients from finite field)

I referred lecture notes, essential coding theory and blogs on berlekamp algo like 
https://jeremykun.com/2014/03/13/programming-with-finite-fields/
https://jeremykun.com/2015/09/07/welch-berlekamp/
https://inst.eecs.berkeley.edu/~cs70/su14/notes/note_8.pdf

and stack exchange for coding the solutions.

Srikar Kale referred to my code and since he is new to python, I helped him understand how to use sympy.

Even though I couldn't implement q4,q5 due to interpolation error, trying to code it did help me in understanding the algorithms better. I got a little more clarity for the idea behind the algorithms. For ex, to get a set of M(x) for list decoding, we had to take polynomial of two variables of form Q(X,Y). We couldn't do it with just N(X) and E(X). We couldn't find a set of M(X) satisfying the condition for any single variable polynomial . Taking Q(X,Y) = YE(X)-N(X) gives a more general polynomial for which we could find all M(X) satisfying it. And applying necessary degree constraints we could achieve appropriate rho value.


Comments : I found the assignment interesting to do. Got more familiar with the course teachings in the process. 

Thank you.

