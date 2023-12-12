from pwn import *
import os, random, json
from hashlib import sha256
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from sympy.ntheory.modular import crt

server = remote("94.237.51.118",42151)

def decrypt_flag(iv, flag,key):
    key = sha256(str(key).encode()).digest()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    fg = cipher.decrypt(flag)
    return fg


def get_points():
    points = []
    modulus = [getPrime(15) for _ in range(19)]
    for i in range(19):
        
        query = '{"command":"get_share","x":'+str(modulus[i])+'}'
        server.recvuntil("query = ")
        server.sendline(query)
        point = json.loads(server.recvuntil('\n'))
        points.append((point['x'],point['y']))
    return points

points = get_points()
server.recvuntil("query = ")
server.sendline('{"command":"encrypt_flag"}')
server.recvuntil('Here is your encrypted flag : ')
x = server.recvuntil('\n').replace(b".", b"").replace(b"\n", b"")
flag_obj = json.loads(x)
xs =[x[0] for x in points]
ys = [x[1] for x in points]

key = crt(xs, ys)[0]
print(key)
iv = bytes.fromhex(flag_obj['iv'])
enc_flag = bytes.fromhex(flag_obj['enc_flag'])

flag = decrypt_flag( iv, enc_flag, key)
print(flag)
