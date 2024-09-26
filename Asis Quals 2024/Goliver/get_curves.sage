proof.arithmetic(False)
p = 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
a = 0
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
F = GF(p)
P.<x> = PolynomialRing(F)
for _ in range(0,100):
    b = randint(-p,p) 
    if b in [-2,2]:
        continue
    
    f = x**3 + b - y**2
    roots = f.roots()
    for root in roots:
        _x = root[0]
        E = EllipticCurve(F, [a,b])
        G = E.gen(0)
        od = G.order()
        fac = od.factor()
        subgroups = [f^e for f,e in fac if gcd(f^e, prod) == 1 and f^e < 2**48]
        if subgroups:
            print([(b, (_x,y), od, subgroups)])
    

"""
for b in range(1, 15):
    if b in [-2, 2]:
        # singular
        continue
    E = EllipticCurve(F, [a, b])
    G = E.gen(0)
    od = G.order()
    fac = od.factor()
    subgroups = [
        f ^ e for f, e in fac if gcd(f ^ e, prod) == 1 and f ^ e < 2 ^ 32
    ]  # very small
    ar.append((b, G.xy(), od, subgroups))
    prod = lcm(prod, product(subgroups))
    print(prod)
    if prod > n:
        break


print(ar)
"""