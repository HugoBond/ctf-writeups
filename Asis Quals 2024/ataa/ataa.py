#!/usr/bin/env python3

import sys
from Crypto.Util.number import *
from string import *
from random import *
from math import gcd
from secret import p, flag
	
def die(*args):
	pr(*args)
	quit()
	
def pr(*args):
	s = " ".join(map(str, args))
	sys.stdout.write(s + "\n")
	sys.stdout.flush()
	
def sc(): 
	return sys.stdin.buffer.readline()

def check(u, v, w, x, y, z, k, p):
	if len(set([u, v, w, x, y, z])) == 6:
		if all(map(lambda t: t % p != 0, [u, v, w, x, y, z, k])):
			if gcd(u, v, w, x, y, z, k, p) == 1:
				if (pow(u, k, p) + v * w * x * y * z) % p + (pow(v, k, p) + u * w * x * y * z) % p + \
				   (pow(w, k, p) + v * u * x * y * z) % p + (pow(x, k, p) + v * w * u * y * z) % p + \
				   (pow(y, k, p) + v * w * x * u * z) % p + (pow(z, k, p) + v * w * x * y * u) % p == 0:
					return True
	return False

def main():
	border = "┃"
	pr(        "┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓")
	pr(border, ".:: Welcome to ATAA task! Your mission is pass only one level! ::.", border)
	pr(        "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛")
	nbit, _b = 128, False
	pr(border, f'p = {p}')
	pr(border, f"Please provide your desired {nbit}-integers:")
	inp = sc().decode()
	try:
		u, v, w, x, y, z, k = [int(_) for _ in inp.split(',')]
		if u.bit_length() == v.bit_length() == w.bit_length() == x.bit_length() == \
		   y.bit_length() == z.bit_length() == nbit and k.bit_length() >= nbit:
			_b = True
	except:
		die(border, f"The input you provided is not valid!")
	if _b:
		if check(u, v, w, x, y, z, k, p):
			die(border, f'Congrats, you got the flag: {flag}')
		else:
			die(border, f'The input integer is not correct! Bye!!')
	else:
		die(border, f"Your input does not meet the requirements!!!")

if __name__ == '__main__':
	main()