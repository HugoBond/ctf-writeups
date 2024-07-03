from pwn import remote
from tqdm import tqdm
from Crypto.Util.number import long_to_bytes, bytes_to_long, inverse, getPrime
from param import n,c

from sage.all import prod,is_square,sqrt, inverse_mod, randrange

import os
import json
import hashlib
import random
import subprocess

def solve_congruence(k: int, m: int, n=n):

    if not is_square(k):
        while True:
            u, v = randrange(n), randrange(n)
            m0 = m * (u**2 + k * v**2) % n
            if m0 % 4 != 3:
                continue
            x0 = pow(-k, (m0 + 1) // 4, m0)
            if pow(x0, 2, m0) == -k % m0:
                break
    else:
        j = int(sqrt(k))
        while True:
            u, v = randrange(n), randrange(n)
            m0 = m * (u**2 + k * v**2) % n
            if m0 % 8 != 5:
                continue
            x0 = j * pow(2, (m0 - 1) // 4, m0)
            if pow(x0, 2, m0) == -k % m0:
                break

    i = 0
    ms, xs = [m0], [x0]
    while True:
        # assert (xs[i]**2 + k) % ms[i] == 0
        mi = (xs[i]**2 + k) // ms[i]
        xi = min(xs[i] % mi, mi - (xs[i] % mi))
        ms.append(mi)
        xs.append(xi)
        if k > 0 and xs[i] <= ms[i + 1] <= ms[i] or k < 0 and mi**2 <= abs(k):
            break
        i += 1
    
    s, t = x0, 1
    for x_ in xs[1:-1]:
        s, t = (x_ * s + k * t) % n, (x_ * t - s) % n

    M = prod(ms[1:])
    U = s * inverse_mod(M, n) % n 
    V = t * inverse_mod(M, n) % n

    del ms, xs
    if is_square(mi):
        x, y = int(sqrt(mi)), 0
    elif mi == k:
        x, y = 0, 1
    else:
        x_, y_ = solve_congruence(-mi, -k, n)
        x, y = x_ * inverse_mod(y_, n) % n, inverse_mod(y_, n)
        # assert (x**2 + k * y**2) % n == mi % n

    X, Y = (U * x + k * V * y) % n, (U * y - V * x) % n

    x, y = (X * u + k * Y * v) % n, (X * v - Y * u) % n
    
    return int(x * m * inverse_mod(m0, n) % n), int(y * m * inverse_mod(m0, n) % n)


def test_solve_congruence():
    # z_0^2 * c - z_1^2 = (t_0 - t_1) * c (mod n)
    # z_0^2 - c^-1 * z_1^2 = t_0 - t_1 (mod n)
    p, q = getPrime(128), getPrime(128)
    n_ = p * q
    t0, t1 = random.getrandbits(128), random.getrandbits(128)
    shift = 2**64
    m = (t0 - t1) * shift % n_
    k = -inverse(c, n_)
    z0, z1 = solve_congruence(k, m, n_)
    assert (z0**2 + k * z1**2) % n_ == m % n_
    d = (z0**2 - t0 * shift) % n_
    d_ = (z1**2 * inverse(c, n_) - t1 * shift) % n_
    assert d == d_
    s0 = t0 * shift + d
    s1 = t1 * shift + d
    assert (z0**2 - s0) % n_ == 0
    assert (z1**2 - s1 * c) % n_ == 0

def encode(s):
    sib = int.to_bytes(s, (int(s).bit_length()+7)//8, 'big')
    sil = int.to_bytes(len(sib), 2, 'big')
    return sil + sib

def gen_proof():
    prefix_si = int.to_bytes(446, 2, 'big') + b'\xff'
    global_prefix = b''
    solved_congruences = {}
    ss,zs = [],[]
    for i in tqdm(range(128)):
        with open("prefix.bin", "wb") as f:
            f.write(global_prefix + prefix_si)

        #if not os.path.exists(f"out/coll{i}_1.bin") or not os.path.exists(f"out/coll{i}_2.bin"):
        subprocess.run(["/home/bond/tools/fastcoll/fastcoll", "-p", "prefix.bin", "-o", f"out/coll{i}_1.bin", f"out/coll{i}_2.bin"], stdout=subprocess.DEVNULL)


        # We read the colliding blocks
        t0 = bytes_to_long(open(f"out/coll{i}_1.bin", "rb").read()[-190:])
        t1 = bytes_to_long(open(f"out/coll{i}_2.bin", "rb").read()[-190:])

        k = -inverse(c, n)
        m = ((t0 - t1) * 2**2048) % n
        # z0^2 - c^-1 * z1^2 = t0 - t1 (mod n)
        if (k,m) in solved_congruences:
            z0, z1 = solved_congruences[k, m]
        else:
            z0, z1 = solve_congruence(k, m, n)
            assert (z0**2 + k * z1**2) % n == m % n
            solved_congruences[k, m] = z0, z1

        assert (z0**2 + k*z1**2) % n == m % n
        d0 = (z0**2 - t0 * 2**2048) % n
        d1 = (z1**2 * inverse(c, n) - t1 * 2**2048) % n
        assert d0 == d1

        s0 = int(t0 * 2**2048 + d0)
        s1 = int(t1 * 2**2048 + d1)
        assert (z0**2 - s0) % n == 0
        assert (z1**2 - s1 * c) % n == 0
        ss.append((s0,s1))
        zs.append((z0,z1))
        target0 = encode(s0)
        target1 = encode(s1)
        assert hashlib.md5(global_prefix + target0).digest() == hashlib.md5(global_prefix + target1).digest()
        global_prefix += target0

    return ss,zs
        

def challenge():
    ss,zs = gen_proof()
    s0 = [x[0] for x in ss]
    s1 = [x[1] for x in ss]
    z0 = [x[0] for x in zs]
    z1 = [x[1] for x in zs]
    h = int.from_bytes(hashlib.md5(b''.join(map(encode,s0))).digest(), 'big')
    b = [(h>>i)&1 for i in range(127, -1, -1)]
    s,z = [],[]
    for idx,bi in enumerate(b):
        if bi:
            s.append(s1[idx])
            z.append(z1[idx])
        else:
            s.append(s0[idx])
            z.append(z0[idx])

    io = remote("zkpok.2024.ctfcompetition.com", 1337)
    io.sendlineafter("> ",json.dumps({"s":s,"z":z}))
    io.interactive()

challenge()