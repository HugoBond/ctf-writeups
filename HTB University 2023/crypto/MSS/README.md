# MSS
The challenge implement a secret sharing scheme (SSS) through shares. The shares are the points in a polynomial. The polynomial was of degree 30 and you could recover a maximum of 19 points. In order to solve the polynomial, at least 29 points were needed. Therefore, analyzing the code we see that the value of **x** that is evaluated in the function **f(x)** cannot be greater than $2^{15}$. 

## Unintended Solution

The code only checks that the value $x > 2^{15}$ and we know that the key has 256 bits. So we only need to evaluate a $x > 2^{256}$ so that the independent value is not affected by the reduction of the polynomal to module **x**.  Because given a polynomial like this:
$f(x) = ax⁰ + bx¹ + cx² + dx³ + ex⁴$  , the first coefficient is the independent value because $x⁰ = 1$ so $f(x)\ mod\ x = a$ only if $x > a$. 
For this solution wwe only need **1 point**. 

## Intended Solution

The challenge allows us to evaluate 19 points of 15 bits over Real Numbers. So the idea is similar to the unintended solution but with smaller numbers. With the Chinese Remainder Theorem we  can evaluate the polynomial with 19 prime numbers that the sum of all of them is greater than the lenght of the key. Given $15*19 > 256$ we can recover the key and decrypt the flag.
