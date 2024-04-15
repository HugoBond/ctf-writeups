# Choose Params

The challenge use RSA to encrypt the padded flag but the user can select the bit length of the primes used to create the modulus $N$.

```python
while True:
    bits = input("Enter the bit length of your primes> ")
    try:
        bit_len = int(bits)
    except:
        print("please enter a valid intergar")
        continue
    p1 = getPrime(bit_len)
    p2 = getPrime(bit_len)
    n = p1 * p2
    e = 65537
    c = pow(m, e, n)
    print(f"n = {n:x}")
    print(f"e = {e:x}")
    print(f"c = {c:x}")
```

My approach to solving this challenge was to get a bunch of ciphertexts by factors small enough to be factored and then recover the flag with the Chinese Remainder Theorem (CRT). I just had to guess the approximate size of the flag to know how many requests to make to the server.

The flag had 400 bytes + the flag bytes so  $28 * 2*90= 5040\ bits$ , so I choose primes of 90 bits. 

### Solve Script

```python
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
print(long_to_bytes(flag))
```