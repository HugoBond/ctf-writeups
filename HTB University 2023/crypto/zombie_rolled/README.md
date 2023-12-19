# Zombie Rolled - Hard

## Code Analysis

The code has two classes ```PublicKey``` and ```PrivateKey```. At first sight we see that uses a similar scheme as RSA signatures. Lets check first the ```PublicKey``` class:

1. The public key values of ```pub``` and the function ```magic(a,b,c)``` generates a fraction $\frac{N}{D}$ , as $\frac{a}{b} + \frac{b}{c} + \frac{c}{a}$ . The Numerator $N$ acts as the RSA exponent and the denominator $D$ as the modulus.
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

### Get c and r from mixed signatures

With the private key know we can calculate $d$ ```d = pow(f.numerator,-1,prod(x-1 for x in priv))```. The mix signatures are both encrypted so we need to decrypt them $x ^{e^{d}}\ mod\ D \equiv x$. 
```Python
s1_plus_s2 = pow(mix[0],d,f.denominator)
s1_minus_s2 = pow(mix[1],d,f.denominator)
```
Now we have $s1+s2$ and $s1-s2$, doing some linear algebra we get:

$$\begin{align*}
2s1 \equiv s1 + s2 + s1 - s2\ mod\ D \iff s1 \equiv 2^{-1}(s1 + s2 + s1 - s2) \ mod\ D\\
2s2 \equiv (s1 + s2) - (s1 - s2)\ mod\ D \iff s2 \equiv 2^{-1}((s1 + s2) - (s1 - s2)) \ mod\ D
\end{align*}$$

The signatures are raise to the value d, so we have to rise them to the exponent $N$.
```Python
two_s1 = (s1_plus_s2 + s1_minus_s2) % f.denominator
two_s2 = (s1_plus_s2 - s1_minus_s2) % f.denominator
s1 = (inverse(2, f.denominator)*two_s1)%f.denominator
s2 = (inverse(2, f.denominator)*two_s2)%f.denominator
r = pow(s1,f.numerator,f.denominator)
c = pow(s2,f.numerator,f.denominator)
```

### Bivariate Coppersmith

In order to get the flag we have to get **a**, wich is the actual flag, and **b** which is the hash of the flag.

$$
r = \frac{a}{b} + \frac{b}{c} + \frac{c}{a} = \frac{a²c + b²a + c²b}{abc} = (a²c + b²a + c²b)(abc)^{-1}\ mod\ D 
$$

In order to remove inverse numbers we get this equation:

$$\begin{align*}
r(abc) = (a²c + b²a + c²b)\ mod\ D \\
P(a,b) = (a²c + b²a + c²b)(abc)^{-1} - r*(abc)\ mod\ D \\
P(a,b) = 0\ mod\ D
\end{align*}$$

We know the values of $r$,$c$,$D$ and we also know that b has a length of 256 bits and $a$ is less than 512 bits. Between both unknowns they add up to 768 bits, which is much smaller than the D module wich is 3072 bits. So we can try to recover them with bivariate coppersmith and the polynomial $P(a,b)$. I use an existing implementation of this attack []{https://github.com/ubuntor/coppersmith-algorithm}

