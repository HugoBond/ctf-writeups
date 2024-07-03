import re
from Crypto.Util.number import getPrime as get_prime

def main():
    p, q = [get_prime(1024) for _ in range(2)]

    with open('message.txt', 'rb') as f:
        message = f.read()
    
    m = int.from_bytes(message, 'big')


    # Encrypts the flag using the Rabin cryptosystem
    n = p * q
    c = pow(m, 2, n)

    # Sanity check: I should not...
    assert re.search(rb'CTF{.*}', message) # ...forget the flag :)
    assert m**2 >= n # ...make m so small that someone could retrieve m by computing sqrt(c).

    with open('param.py', 'w') as f:
        f.write(f'{n = }\n')
        f.write(f'{c = }\n')
    
if __name__ == '__main__':
    main()