# Count The Counter

In this challenge you have an `encryption oracle` with the AES mode CRT, an stream cipher that encrypts a nonce and a counter and finally XOR it with the plaintext. 

![Untitled](Count%20The%20Counter%202aecb04a8690463b9fb2047b65db9859/Untitled.png)

It is trivial to decrypt a file if the same combination of `nonce|counter` are used to encrypt different files and we know the plaintext of one of the files. We can retrieve the `keystream` in order to decrypt the unknown file with  $ciphertext\ \oplus \ plaintext$.

```python
#!/bin/python3
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from secret import flag
import os

def Encrypt(key, message, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=long_to_bytes(nonce))
    return cipher.encrypt(message).hex()

def chal():
    key = os.urandom(16)
    print("Treat or Trick, count my thing. ")
    nonce_counter = 1
    print(Encrypt(key, flag, nonce_counter))
    
    while True:
        nonce_counter += 1
        to_enc = input("Give me something to encrypt: ")
        print(Encrypt(key, bytes.fromhex(to_enc), nonce_counter))

if __name__ == "__main__":
    chal()
```

The bug in the code is that a counter is used as nonce and the counter is used as the default counter of the class. The counter is concatenated to the nonce and a padding is added in front of it so that it occupies a complete block which makes the keystream with counter 1 equal to the keystream with counter 256.

![Untitled](Count%20The%20Counter%202aecb04a8690463b9fb2047b65db9859/Untitled%201.png)

### Solve Script

```python
from pwn import remote

def xor(a, b):
    return bytes([x^y for x, y in zip(a, b)])

ciphertexts=[]
server = remote('gold.b01le.rs', 5002)
server.recvuntil(b'thing. \n')
flag_enc = bytes.fromhex(server.recvline().strip().decode())
data = b'a'*256
for i in range(255):
    server.sendlineafter(b'Give me something to encrypt: ', data.hex())
    ciphertexts.append(bytes.fromhex(server.recvline().strip().decode()))

print(xor(flag_enc, xor(ciphertexts[-1],data)))
```