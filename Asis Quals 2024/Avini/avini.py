#!/usr/bin/env python3

import sys
from random import *
from Crypto.Util.number import *
from Crypto.PublicKey import ECC

flag = "AVINI{y0u_4r3_4_5t4r_0f_3ll1pt1c_curv3s}"

def die(*args):
	pr(*args)
	quit()
	
def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()
	
def sc(): 
	return sys.stdin.buffer.readline()

def genon(nbit):
	R = list(range(1, nbit))
	shuffle(R)
	B = ['1'] + ['0'] * (nbit - 1)
	u = randint(nbit // 2 + 5, 2 * nbit // 3)
	for i in range(0, u):
		B[R[i]] = '1'
	return int(''.join(B), 2)

def is_genon(n, nbit):
	return n.bit_length() == nbit and bin(n)[2:].count('1') >= nbit // 2 + 1

def main():
	border = "┃"
	pr("┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr("┃ Welcome to AVINI challenge! Here we can double your points on ECC! ┃")
	pr("┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")

	nbit = 256
	key = ECC.generate(curve='P-256')
	order = ECC._curves['NIST P-256'][2]
	Q = key.pointQ
	O = ECC.EccPoint(Q.x, Q.y, curve='p256').point_at_infinity()

	pr(border, f"Please provide your desired integer `n' or even the binary ")
	pr(border, f"representation of it, [D]ecimal or [B]inary?")
	
	ans = sc().decode().strip().lower()
	if ans == 'd':
		pr(border, "So send the integer n: ")
		_n = sc().decode()
		try:
			_n = int(_n)
		except:
			die(border, 'Your input is not integer!')
		if is_genon(_n, nbit):
			R, P, c = O, Q.copy(), 0
			for _b in bin(_n)[2:][::-1]:
				if _b == '1':
					R = R + P
					c += 1
				P = P.double()
				c += 1
				if 18 * c >= 19 * nbit:
					break
			if R == Q * _n and _n < order:
				die(border, f'Congrats, you got the flag: {flag}')
			else:
				die(border, f'The calculations failed! Sorry!!')
		else:
			die(border, 'Your integer does not satisfy the requirements!')
	elif ans == 'b':
		pr(border, "Now send the binary representation of n separated by comma: ")
		_B = sc().decode()
		try:
			_B = [int(_) for _ in _B.split(',')]
			_flag = all(abs(_) <= 1 for _ in _B) and len(_B) == nbit
		except:
			die(border, 'Your input is not corr3ct!')
		if _flag:
			R, P, c, i, _n = O, Q.copy(), 0, 0, 0
			for _b in _B[::-1]:
				if _b != 0:
					_n += 2 ** i * _b
					R += P if _b > 0 else -P
					c += 1
				P = P.double()
				c += 1
				i += 1
				if 71 * c >= 72 * nbit:
					break
			if _n.bit_length() == nbit and _n < order and R == Q * _n:
				die(border, f'Congrats, you got the flag: {flag}')
			else:
				die(border, f'The calculations failed! Sorry!!')
		else:
			die(border, f'Your binary representation does not satisfy the requirements!!')
	else:
		die(border, "Your choice is not correct, Goodbye!!")	

if __name__ == '__main__':
	print(genon(256))
	main()