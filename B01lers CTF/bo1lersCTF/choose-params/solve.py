from pwn import remote
from Crypto.Util.number import long_to_bytes
from sage.all import crt,factor
from tqdm import tqdm

server = remote('gold.b01le.rs', 5001)

def get_params():
    server.recvuntil('primes> ')
    server.sendline(b'90')
    server.recvuntil(b'n = ')
    n = int(server.recvline().strip(),16)
    server.recvuntil(b'e = ')
    e = int(server.recvline().strip(),16)
    server.recvuntil(b'c = ')
    c = int(server.recvline().strip(),16)
    return n,e,c


messages = []
modules  =[]
ns  =[]
cs = []	
for i in tqdm(range(28)):
    n,e,c = get_params()
    ns.append(n)
    cs.append(c)

e = 0x10001
for n,c in zip(ns,cs):
    factors = factor(n)
    p = int(factors[0][0])
    q = int(factors[1][0])
    phi = (p-1)*(q-1)
    d = pow(e,-1,phi)
    m = pow(c,d,n)
    messages.append(m)
    modules.append(n)

flag = crt(messages,modules)
print(flag)
print(long_to_bytes(flag))