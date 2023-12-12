# Mayday

## Challenge Analysis

The challenge uses RSA-CRT variant to encrypt the flag and **e** is a 227 bit prime number. We have the RSA valus **N**, **e**,**ciphertext** and **dp** and **dq**. 
The attack implementation is based on this paper <https://eprint.iacr.org/2022/271.pdf>

## Attack Theory
