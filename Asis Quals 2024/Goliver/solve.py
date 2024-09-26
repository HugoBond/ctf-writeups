from sage.all import *
from pwn import remote, process
from Crypto.Util.number import *
from random import randint
from math import sqrt
import signal

def send_input(signum,frame):
    print("Sending input")
    io.sendline(b"p")

signal.signal(signal.SIGALRM, send_input)
signal.setitimer(signal.ITIMER_REAL, 50, 30)

p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

def dlog(G, nG, factors, order, MODS):
    dlogs = []
    mods = []
    print("Starting dlog...")
    for p in factors:
        if p in MODS:
            continue

        mods.append(p)
        t = order // mods[-1]
        dlogs.append(discrete_log(t * nG, t * G,ord=ZZ(mods[-1]), operation='+'))

    return dlogs, mods

def read_point():

    print(io.recvuntil(b"skey * H ="))
    resp = eval(io.recvline().strip().decode())
    return resp[0], resp[1]

def send_point(x,y):
    io.sendline(b"E")
    io.recvuntil(b"Secp256k1 curve:")
    print(f"Sending point {x},{y}")
    io.sendline(f"{x},{y}".encode())


def get_random_point(K,F,b):
    while True:
        try:
            x,y,_ = K.lift_x(F(randint(0, p-1)))
            if (x**3 + a * x + b - y**2) % p < 0x0f:
                return x,y
        except:
            continue

def get_key(params):
    global_dlogs , global_mods = [], []
    F = GF(p)
    for b, (x, y), od, subgroups in params:
        print(f"Trying curve {b}")
        K = EllipticCurve(GF(p), [a, b])
        #x,y = get_random_point(K,F,b)
        try:
            send_point(x, ceil(F(x**3+7-p).sqrt()))
        except:
            continue
        _x, _y = read_point()
        G = K(x, y)
        nG = K(_x, _y)
        _dlog, _mods = dlog(G, nG, subgroups, od, global_mods)
        global_dlogs += _dlog
        global_mods += _mods
    return crt(global_dlogs, global_mods)
        
def get_flag(key):
    #io.interactive()
    io.recvuntil(b'[Q]uit')
    io.sendline(b"g")
    io.sendlineafter(b"private key:",str(key).encode())
    print(io.recvline())

def get_pubkey():
    io.sendline(b"p")
    print(io.recvline())
    return io.recvline().strip().split(b"= ")[1]

G = EllipticCurve(GF(p), [a, 7])(x,y)
curve_parameters = [(105, (110834053634609602798951721692011457977766758728483459074616541482985821623454, 32670510020758816978083085130507043184471273380659243275938904335757337482424), 115792089237316195423570985008687907853031073199722524052490918277602762621571, [109903, 12977017, 383229727]),\
                    (107, (114019093326204313460470946256347872149422532841975370362780312422601275554501, 32670510020758816978083085130507043184471273380659243275938904335757337482424), 57896044618658097711785492504343953926299326406578432197819248705606044722122, [2, 3, 20412485227]),\
                            (189, (111774437130201132452936112676986108696691562597956893261844601685185028128210, 32670510020758816978083085130507043184471273380659243275938904335757337482424), 38597363079105398474523661669562635951234135017402074565436668291433169282997, [3, 169, 3319, 22639]),\
                                (26041017778364852772390897259712152653019331464252366056410452711258224774281, (27905622015652621924544316296830498939582142098804330421384373543155432666043, 32670510020758816978083085130507043184471273380659243275938904335757337482424), 115792089237316195423570985008687907853508896131558604026424249738214906721757, [3, 199, 18979]),\
                                    (989, (67490520979961012849978114987623022443052812750649962055158161631936267762493, 32670510020758816978083085130507043184471273380659243275938904335757337482424), 8270863516951156815969356072049136275281522608437447405948333614614684278506, [2, 7, 10903, 5290657, 10833080827,22921299619447])]      
io = remote('65.109.204.171', 17371)
io.recvuntil(b'[Q]uit')

pubkey = int(get_pubkey()[2:].decode(),16)

skey = get_key(curve_parameters)
assert (skey*G)[0] == pubkey
print(skey.bit_length(), skey)
get_flag(skey)
