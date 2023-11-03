#!/usr/bin/python3

from ecdsa.ecdsa import Private_key, Public_key, generator_521
from random import randrange
from hashlib import sha512
from Crypto.Util.number import bytes_to_long, long_to_bytes
from os import environ


flag = environ['FLAG'].encode()

g = generator_521
n = g.order()

secret = randrange(1, n)
secret2 = (randrange(1, 2048)  * secret) % n 

k = randrange(1, n)

public_key = Public_key(g, g * secret)
private_key = Private_key(public_key, secret)

public_key2 = Public_key(g, g * secret2)
private_key2 = Private_key(public_key2, secret2)



def signMsg(privkey, msg_bytes):
    hash = bytes_to_long(sha512(msg_bytes).digest())
    signature = privkey.sign(hash, k)
    return (signature.r, signature.s)



def xor(flag_bytes, key):
    key_bytes = long_to_bytes(key)
    flag_length = len(flag_bytes)
    generated_key = sha512(key_bytes).digest()[:flag_length]
    return bytes([a ^ b for a, b in zip(flag_bytes, generated_key)])


msg = "Can you get the flag?"
print("MSG: " + msg)

r, s = signMsg(private_key, msg.encode())
print("\nSignature 1\n---------------------")
print("r = " + str(r))
print("s = " + str(s))

r2, s2 = signMsg(private_key2, msg.encode())
print("\nSignature 2\n---------------------")
print("r2 = " + str(r2))
print("s2 = " + str(s2))

enc_flag = bytes_to_long(xor(flag, secret))
print("\nFlag: " + str(enc_flag))
