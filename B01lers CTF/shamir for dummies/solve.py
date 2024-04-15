from pwn import remote
from Crypto.Util.number import long_to_bytes,GCD
from sage.all import PolynomialRing, GF

server = remote("gold.b01le.rs", 5006)
server.recvuntil("Let's use \n\n")
n = int(server.recvline(b'n =').strip().split(b"=")[1])
k = int(server.recvline(b'k =').strip().split(b"=")[1])
p = int(server.recvline(b'p =').strip().split(b"=")[1])
print(f"n = {n}\nk = {k}\np = {p}")

def roots_of_unity(e, phi, n):    
    phi_coprime = phi
    while GCD(phi_coprime, e) != 1:
        phi_coprime //=  GCD(phi_coprime, e)

    roots = pow(2, phi_coprime, n) 
    return roots


root= roots_of_unity(n,p-1, p)
print(f"Root of unity: {root}")
count = 0
while count < n:
    server.sendlineafter(b'> ',str((root**count) % p).encode())
    count += 1

server.recvuntil(b'> ')
server.sendline(str(n).encode())
server.recvuntil(b"The shares P(X_i)'s were':\n")
shares = list(map(int,server.recvline().strip().decode()[1:-1].split(", ")))
P = PolynomialRing(GF(p), 'x')
res = P.lagrange_polynomial(list((root**i % p,shares[i]) for i in range(n)))
coefficients = res.coefficients()
print(f"Flag: {long_to_bytes(int(coefficients[0]))}")