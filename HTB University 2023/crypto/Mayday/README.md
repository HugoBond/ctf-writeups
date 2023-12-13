# Mayday - Medium

## Challenge Analysis

The challenge uses RSA-CRT variant to encrypt the flag and **e** is a 227 bit prime number. We have the RSA values **N**, **e**,**ciphertext** and the 512 Most Significant Bits of **dp** and **dq**. 
The attack implementation is based on this paper <https://eprint.iacr.org/2022/271.pdf>

## Attack Theory

The RSA-CRT calculates the values **dp** and **dq** with this equations ($d_p^{(M)}$ = Most Significant bits and $d_p^{(L)}$ = Less Significant Bits):

$$\begin{align*}
d_p = e^{-1}\ mod\ (p-1)  & \iff d_p = d_p^{(M)} * 2^{512} + d_p^{(L)}\\
d_q = e^{-1}\ mod\ (q-1)  & \iff d_q = d_q^{(M)} * 2^{512} + d_q^{(L)}
\end{align*}$$

### First Step: Recover $k_p$ and $k_q$
$$\begin{align*}ed_p = k_p(p-1) + 1 \\
ed_q = k_q(p-1) + 1\end{align*}$$

If we rewrite the equations: 

$$\begin{aligned}k_pp = k_p - 1 + ed_p \\
k_qq = k_q - 1 + ed_q\end{aligned}$$

Now if we multiply $k_pp$ with $k_qq$:

$$k_pk_qN = (k_p - 1)(k_q - 1) + ed_p(k_q - 1) + ed_q(k_p - 1) + e^2d_pd_q$$

Let A be:

$$A = {2^{2*512}e^2d_pd_q \over N}$$

We only have the MSB of $d_p$ and $d_q$ so we can calculate the approximation of **A**. The paper states that for sufficiently large N (which
already holds for standard RSA moduli) we have $\lceil A \rceil = k_pk_q$. Therefore we have $k_pk_q$ and with this value we can calculate $k_p + k_q$ solving $k_pk_qN - AN$:

$$k_p + k_q = 1 - kl(N - 1) \mod\ e $$

Now $k_p$ and $k_q$ are the two solutions of the quadratic polynomial:

$$0 = (x-k_p)(x-k_q) = x² - k_qx - k_px +k_pk_q = x² + (1 - k_pk_q(N -1))x + k_pk_q $$

$$x² + (1 - A(N -1))x + A = 0$$

We know just have to get the roots of the quadratic equation over **e** and check whether the product of the solutions equals $k_pk_q$. If we cant recover them we need to find the roots over e in the next polynomial:

$$ x² +(1 - A(N-1) + e)x + A = 0$$

### Second Step: Factor N with $k_p$ and $k_q$

Using the calculated $k_p$ and $d_p^{(M)}$ with $ed_p = k_p(p-1) + 1$ and $d_p = d_p^{(M)} * 2^{512} + d_p^{(L)}$

Rewrite to:

$$ed_p^{(L)} + ed_p^{(M)}*2^i + k - 1 = kp$$

With this equation we can get the polynomial $f(x) = x + a\ mod\ k_pp$ where the coefficient **a** is $$a = (ed_p^{(M)}2^{512} + k_p -1)(e^{-1}\ mod\ k_pN)$$ 

and the root is:

$$x_0 = d_p^{(L)}$$  
