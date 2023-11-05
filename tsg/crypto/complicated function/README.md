# Complicated Function

1. The solution that i used for this challenge was a binary search of **p**.

  $f(p) = \left\lfloor \sqrt{p^2 + (2^{512}-6)p + \left\lfloor \sqrt{p\sin p} \right\rfloor} \right\rfloor + 2^{1023}$  
  $N = pf(p) = pq$

2. The other solution proposed by the author was a convergence of **f(p) - p**. 
