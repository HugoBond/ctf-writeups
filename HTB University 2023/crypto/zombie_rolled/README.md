# Zombie Rolled - Hard

## Code Analysis

The code has two classes ```PublicKey``` and ```PrivateKey```. At first sight we see that uses a similar scheme like RSA signatures. Lets check first the ```PublicKey``` class:

1. Using the public key values of ```pub``` and the function ```magic(a,b,c)``` generates a fraction $\frac{N}{D}$ , as $\frac{a}{b} + \frac{b}{c} + \frac{c}{a}$ . The Numerator $N$ plays as the RSA exponent and the denominator $D$ as the modulus.
 ```Python
   def magic(ar):
        a, b, c = ar
        return Fraction(a, b) + Fraction(b, c) + Fraction(c, a)
   ```

2. The encryption func just makes and RSA simple encryption $m^{N}\ mod\ D$ and the verify function ```verify(message,signature)``` given a message and the signature verifies if it was correctly signed.

Now the ```PrivateKey```:

1. Contains a static method that generates a tuple of three primes of **nbits** and calculates the public key with this values. We dont know the function that derives the pub key from the private key.
```Python
def generate(nbits):
        while True:
            try:
                priv = tuple([getPrime(nbits) for _ in range(3)])
                pub = derive_public_key(priv)
                return PrivateKey(priv, pub)
            except ValueError:
                pass
```
2. This class initialise the d value calulated as $N^{-1}\ mod\ phi(D)$ and asserts that ```magic(priv) == magic(pub)```.

3. The decrypt func just raise a values to the private value **d**. The sign function  ```sign(message)``` uses 3 values (a,b,c) to calculate the signature. The first value **a** is the message itself, the second value **b** is the sha256 hash of the message and the third value **c** is a random number of max 1024 bits. The signature return two values **s1** and **s2**, where  $s1 = r^d\ mod\ D$ and  **r** is $r = \frac{x}{y}\equiv x*y^{-1} mod\ D$ and  $s2 = c^d\ mod\ D$.
 ```Python
def sign(self, m):
        h = bytes_to_long(sha256(m.to_bytes(self.nb, "big")).digest())
        a, b = m, h
        c = randbelow(1 << self.nb)
        r = fraction_mod(self.magic((a, b, c)), self.f.denominator)
        s1 = self.decrypt(r)
        s2 = self.decrypt(c)
        return s1, s2
```

## Retrieve the Private Key

The strangest things in this code were the magic function and the public key. So playing a little with the public numbers i realized that if ```magic(priv) == magic(pub)``` we can derive the private key from the public key. 
Therefore if we write the equation: 

$$
\frac{a}{b} + \frac{b}{c} + \frac{c}{a} = \frac{a²c + b²a + c²b}{abc}
$$

we know that the priv numbers are primes and the denominator is the multiplication of the 3 and is equal to the lcm of the public keys, i made some guess and assume that the pub key was generated with some mix of the priv keys. Playing with the public numbers and the denominator $D$ we can calculate the priv numbers. I knew I had found the numbers because they all followed the structure of being prime and 1024 bits.
```Python
pub = [...,...,...]
x1 = gcd(D,pub[0])
x2 = gcd(D,pub[1])
x3 = gcd(D,pub[2])
priv =[gcd(x1,x2), gcd(x2,x3), gcd(x1,x3)]
assert priv[0] * priv[1] * priv[2] == D
```

## Reverse the MAGIC function

