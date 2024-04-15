from pwn import remote
from Crypto.Util.number import getPrime,long_to_bytes
server = remote("gold.b01le.rs", 5006)
server.recvuntil("Let's use \n\n")
n = int(server.recvline(b'n =').strip().split(b"=")[1])
k = int(server.recvline(b'k =').strip().split(b"=")[1])
p = int(server.recvline(b'p =').strip().split(b"=")[1])
print(f"n = {n}, k = {k}, p = {p}")
count = 0
#prime = getPrime(490)

while count < n:
    if count == 0:
        server.sendlineafter(b'> ',str(p-(p-54)).encode())
    elif count == 1:
        server.sendlineafter(b'> ',str(p-54).encode())
    else:
        server.sendlineafter(b'> ',str(count).encode())
    count += 1

server.recvuntil(b'> ')
server.sendline(str(pow(n,-1,p)).encode())
server.interactive()
