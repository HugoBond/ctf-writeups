from ecdsa.ecdsa import Private_key, Public_key, generator_521
from random import randrange
from hashlib import sha512
from Crypto.Util.number import bytes_to_long, long_to_bytes,inverse,GCD
from os import environ

g = generator_521
n = g.order()

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

r2 = 6033413533409773983159129194608567700167808027544309312264475714231273314262399130086342771147013613464364002437741028946855960457520931841547828126905335212
s2 = 1770973723903855963203597249506316726320637385876961673266096708759728364719492366988955847251009621962063821995869023222661794647788842751345102818008767317

r = 6033413533409773983159129194608567700167808027544309312264475714231273314262399130086342771147013613464364002437741028946855960457520931841547828126905335212
s = 4634407588388368588856344443523588926071811834679379904365865988223504550650739815180425514252581927344145354749013213870566451576788230162598847294540925791
flag =7309572209470591388671665443312094597874019466185244572590887187072625238120792775655759202089432913645704781590755602

msg_hash = bytes_to_long(sha512(msg.encode()).digest())

#Solved equation for #s2 - s1 and s2 + s1
s2_s = s2 - s   
s2_mas_s = s2 + s 
for b in range(2,2048):
    b_inv = inverse(b, int(n))
    msg_hash_inv = inverse(msg_hash, int(n))
  
    krd = (inverse(b-1, n) * s2_s) % n
    k_inv = (inverse(2, n)*msg_hash_inv*(s2_mas_s - (b+1)*krd)) % n
    k = inverse(k_inv, n)
    if (k * g).x() == r:
        x = b
        break

secret = ((s*k - msg_hash)* inverse(r, n)) % n

flag_txt = (xor(long_to_bytes(flag), secret))
print("\nFlag: " + str(flag_txt.decode()))
