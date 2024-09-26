#!/usr/bin/env sage

from Crypto.Util.number import *
from flag import flag

def genkey(nbit):
	k = nbit >> 6
	p, l = getPrime(nbit), k << 1
	while True:
		M = matrix(GF(p), [[randint(0, p) for _ in range(l)] for _ in range(l)])
		if M.is_invertible():
			return p, M

def encrypt(m, key):
	p, M = key
	k = M.nrows() // 2
	u, v = [vector(randint(0, p) for _ in range(k)) for _ in '01']
	u[k - 1], U = m - sum(u[:-1]) % p, []
	for i in range(k):
		U += [(v[i] * u[i]) % p, v[i]]
	return M.inverse() * vector(U)

nbit = 512
key = genkey(nbit)
               
l = len(flag)
m1, m2 = bytes_to_long(flag[:l//2]), bytes_to_long(flag[l//2:])

c1 = encrypt(m1, key)
c2 = encrypt(m2, key)

print(f'p  = {key[0]}')
print(f'M  = {key[1]}')
print(f'c1 = {c1}')
print(f'c2 = {c2}')