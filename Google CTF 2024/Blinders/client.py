import ast
import socket
from Crypto.Random import random
import hashlib
from ecdsa.curves import NIST256p
from ecdsa.numbertheory import jacobi, square_root_mod_prime
from ecdsa.ellipticcurve import Point, INFINITY

curve = NIST256p.curve

def H(id):
    a, b, p = curve.a(), curve.b(), curve.p()

    hash = hashlib.sha256(f'id={id}'.encode()).digest()
    x = int.from_bytes(hash, 'big')

    while True:
        y2 = (x**3 + a*x + b) % p
        if jacobi(y2, p) == 1: break
        x += 1

    y = square_root_mod_prime(y2, p)
    return Point(curve, x, y)

class BlindersAPI:
    def __init__(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.settimeout(10)
        self.s = s
        self.recvline()

    def recvline(self):
        output = []
        while True:
            c = self.s.recv(1)
            if c == b'' or c == b'\n': break
            output.append(c)
        return b''.join(output)

    def handle(self, eid):
        self.s.send(f'handle {eid.x()} {eid.y()}\n'.encode())
        eids = ast.literal_eval(self.recvline().decode())
        deid = ast.literal_eval(self.recvline().decode())
        return [Point(curve, *eid) for eid in eids], Point(curve, *deid)

    def submit(self, S):
        hash = hashlib.sha256(','.join(map(str, S)).encode()).hexdigest()
        self.s.send(f'submit {hash}\n'.encode())
        return self.recvline().decode()
    
    def final(self):
        return self.recvline().decode()


# Implements the client side of Blinders
class BlindersClient:
    def __init__(self, api):
        self.api = api

    def query(self, eid):
        # 1.1. Generate a random key R
        r = random.randrange(0, int(NIST256p.order))
        r_inverse = int(pow(r, -1, NIST256p.order))
        # 1.2. Compute encrypted identified eid = H(id)^R
        eid = eid * r
        # 1.3. Send eid to P2
        server_eids, deid = self.api.handle(eid)
        # 3.1. Compute eid' = deid^(1/R)
        new_eid = deid * r_inverse
        return server_eids, new_eid
    
    def submit(self, S):
        return self.api.submit(S)

    def final(self):
        return self.api.final()

def find_missing(Eids1, OddDeid,Eids2, EvenDeid):
    for x in range(256):
        res = INFINITY
        if x % 2 == 0:
            for i in range(1,256,2):
                if i >= x:
                    res += Eids1[i-1]
                else:
                    res += Eids1[i]
            if res == OddDeid:
                return x
        else:
            for i in range(0,255,2):
                if i >= x:
                    res += Eids2[i-1]
                else:
                    res += Eids2[i]

            if res == EvenDeid:
                return x
    return None


def sumPoints(points):
    sumP = points[0]
    for p in points[1:]:
        sumP += p
    return sumP


def main():
    api = BlindersAPI('blinders.2024.ctfcompetition.com', 1337)
    client = BlindersClient(api)

    for _ in range(16):
        S = list(range(256))
        OddS = list(range(1, 256, 2))
        EvenS = list(range(0, 256, 2))
        OddIds = [H(id) for id in OddS]
        EvenIds = [H(id) for id in EvenS]
        Eids1, OddDeid = client.query(sumPoints(OddIds))
        Eids2, EvenDeid = client.query(sumPoints(EvenIds))
        secret = find_missing(Eids1, OddDeid, Eids2, EvenDeid)
        print("Secret: ", secret)
        S.remove(secret)
        res = client.submit(S)
        print(f'Response = {res}')
        if res == 'Nope.': return
    
    print(client.final()) # sweet flag <3


if __name__ == '__main__':
    main()