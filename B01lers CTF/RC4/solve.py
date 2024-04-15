from pwn import remote
import re
server = remote("gold.b01le.rs", 5004)
server.recvuntil(b'padding(s).)\n')

pad = b'\x00'*100000
server.sendline(pad)
data = bytes.fromhex(server.recvline().strip().decode())
search = re.findall(b'bctf{.*}', data)
if search:
    print(search[0])
else:
    print("No flag found")