# ECDSA - Nonce Reuse with Different Private Key

The idea to solve this ctf challenge was a system of equations that could retrieve the nonce value in order to calculate de first Private Key.
Some considerations:
1. Second Private Key is calculated from First one: $d_2 = a*d_1$
2. Nonce is the same for both signatures: $r_1 = r_2$
3. The value of **a** is very small.
4. We know $H(m)$, $s_1$, $s_2$, $r_1$, $r_2$

### The Proposed System of Equations:
```math
1.
  \begin{cases} 
    s_2 - s_1 = k^{-1}(H(m) + r*a*d) - k^{-1}(H(m) + r*d)   \\
    s_1 + s_2 = k^{-1}(H(m) + r*d) + k^{-1}(H(m) + r*a*d)
  \end{cases}
```
```math
2.
\begin{cases}
s_2 - s_1 = (a-1)k^{-1}rd  \\
s_1 + s_2 = 2k^{-1}H(m) + (a+1)k^{-1}rd
\end{cases}
```
Doing some substitution with $x = k^{-1}*r*d$ we can simplified the equation:
```math
3.
\begin{cases}
s_2 - s_1 = (a-1)*x  \\
s_1 + s_2 = 2k^{-1}H(m) + (a+1)*x
\end{cases}
```
Solving the first equation for $x$ and the second for $k^{-1}$.
```math
\begin{align*}
  
    x &= (s_2 - s_1)*(a-1)^{-1} \\
    &k^{-1} = 2^{-1}*H(m)^{-1}((s_1 + s_2) - (a+1)*x)

\end{align*}
````

Now we know all parameters except for **a** that can be bruteforce until we found a valid nonce. Once we recover the Private Key we can recover the flag doing a XOR of **flag** and **Private Key**.
