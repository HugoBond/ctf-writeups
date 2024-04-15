from Crypto.Util.number import *
import random
s = bytes_to_long(b'bctf{aAAAAAAAAAAAAAAAAAAAAAA}')
p = 10549361494019700518858655179175184033380762262831791850365580488539936291258817551214332491242353816597713170112632466763539469104882997370128286381138587
n = 11


r = getPrime(511)
def polynomial_evaluation(coefficients, x):
	at_x = 0
	for i in range(len(coefficients)):
		at_x += coefficients[i] * (x ** i)
		at_x = at_x %p
	return at_x

coefficients = [s]
for i in range(1, n):
    coefficients.append(random.randint(2, p-1))

evaluation_points = [1, 2, 3, 4, 5, 6, 7]
shares = []
shares.append(polynomial_evaluation(coefficients, p - 2))
shares.append(polynomial_evaluation(coefficients, 2))
eq = 2*coefficients[0]
for l,i in enumerate(coefficients[1:]):
    if l % 2 != 0:
        eq += 2**(l+1)*i
    eq = eq % p
    
print(eq)
print(shares[0])	
assert eq == sum(shares) % p
exit()



assert shares[1] == sum(coefficients) % p

    
assert eq == sum(shares) % p
print(s)
print((sum(shares) % p))

'''
for i in evaluation_points:
    shares.append(polynomial_evaluation(coefficients, i))

sum_of_shares = 0

for s_i in shares:
	sum_of_shares += s_i
	sum_of_shares = sum_of_shares % p

sum_of_shares_processed = (sum_of_shares * pow(n, -1, p)) % p
if sum_of_shares_processed == s:
	print("Yep, he got my secret message!\n")
	print("The shares P(X_i)'s were':")

else:
	print("Nope, he did not get my secret message!\n")'''