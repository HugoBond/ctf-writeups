from math import gcd
from pwn import remote
import itertools

io = remote("65.109.192.143" ,13731)
io.recvuntil(b"p = ")
p = int(io.recvline().strip())
print("Prime p:", p)

k = p-2
w = p+1
x = -p-1
v = -p+1
y = p-4
u = p-1
z = pow(4,-1,p)

nbit = 128
io.recvuntil(b"integers:")
io.sendline(f"{u},{v},{w},{x},{y},{z},{k}")
print(io.recvall())
