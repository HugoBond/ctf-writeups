#!/usr/bin/env python3

from Crypto.Util.number import *
import sys
flag = "flag{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}"

def die(*args):
	pr(*args)
	quit()
	
def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()
	
def sc(): 
	return sys.stdin.buffer.readline()

def ADD(A, B):
	s = (B[1] - A[1]) * inverse(B[0] - A[0], p) % p
	x = (s ** 2 - A[0] - B[0]) % p
	y = (s * (A[0] - x) - A[1]) % p
	return (x, y)

def DOUBLE(A):
	s = ((3 * A[0] **2 + a) * inverse(2 * A[1], p)) % p
	x = (s ** 2 - 2 * A[0]) % p
	y = (s * (A[0] - x) - A[1]) % p
	return (x, y)

def MUL(A, d):
	_B = bin(d)[2:]
	_Q = A
	for i in range(1, len(_B)):
		_Q = DOUBLE(_Q)
		if _B[i] == '1':
			_Q = ADD(_Q, A)
	return _Q

def GENKEY():
	skey = getRandomRange(1, p)
	assert (G[1] ** 2 - G[0] ** 3 - a * G[0] - b) % p == 0
	pubkey = MUL(G, skey)
	if pubkey[1] % 2 == 0:
		pkey = "02" + hex(pubkey[0])[2:].zfill(64)
	else:
		pkey = "03" + hex(pubkey[0])[2:].zfill(64)
	return (pkey, skey)

def main():
	border = "┃"
	pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr(border, "Welcome to the Goliver World! You can play with ECC points on BTC ", border)
	pr(border, "curve. Your mission is to find the secret key and sweep wallets!  ", border)
	pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
	global p, a, b, G
	p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
	a, b = 0, 7
	n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
	x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
	y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
	G = (x, y)
	pkey, skey = GENKEY()
	level, STEP, _b = 0, 10, False
	while True:
		pr("| Options: \n|\t[E]ncrypt point \n|\t[G]et the flag \n|\t[P]ublic key \n|\t[Q]uit")
		ans = sc().decode().strip().lower()
		if ans == 'e':
			pr(border, f"Please provide your desired point `H` on the Secp256k1 curve:")
			inp = sc().decode()
			try:
				_x, _y = [int(_) for _ in inp.split(',')]
				if (_x**3 + a * _x + b - _y**2) % p < 0x0f:
					_b = True
			except:
				die(border, f"The input point you provided is not valid!")
			if _b:
				_Q = MUL((_x, y), skey)
				print(border, f"skey * H = {_Q}")
				if level == STEP:
					die(border, f'You have only {STEP} rounds to compute.')
				else:
					level += 1
			else:
				die(border, f'The input point is not on the curve! Bye!!')
		elif ans == 'g':
			pr(border, 'Please send the private key: ')
			_skey = sc().decode()
			try:
				_skey = int(_skey)
			except:
				die(border, 'The private key is incorrect! Quitting...')
			if _skey == skey:
				die(border, f'Congrats, you got the flag: {flag}')
			else:
				die(border, f'The private key is incorrect! Quitting...')
		elif ans == 'p':
			pr(border, f'pubkey = {pkey}')
		elif ans == 'q':
			die(border, "Quitting...")
		else:
			die(border, "Bye...")

if __name__ == '__main__':
	main()