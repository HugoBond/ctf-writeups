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