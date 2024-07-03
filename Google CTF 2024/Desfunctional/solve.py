from pwn import remote,xor

io = remote("desfunctional.2024.ctfcompetition.com", 1337)

def decrypt_query(message):
    io.sendline("2")
    io.sendlineafter("(hex) ct: ",message.hex())
    decrypted = bytes.fromhex(io.recvline().decode().strip())
    return decrypted


def get_challenge():
    io.sendlineafter(b"flag\n",b"1")
    challenge = io.recvline().decode().strip()
    return challenge


def get_flag(challenge):
    io.sendline("3")
    io.sendlineafter("(hex) pt: ",challenge.hex())
    flag = io.recvline().decode().strip()
    return flag


def find_collision():
    s = set()
    cha = get_challenge()
    print("Challenge: ", cha)
    # Flip all bits of the challenge, to find a key that flip all the key bits and decrypts the challenge
    flip_cha = xor(bytes.fromhex(cha),b"\xff"*64) 
    for i in range(128):
        dec = decrypt_query(flip_cha)
        if dec not in s:
            s.add(dec)
        else:
            print("Collision found")
            return dec
    return None



decrypted_chall = find_collision()
# We only need to flip the first 8 bytes of the challenge because the subsequent blocks are already xored by CBC mode
flag = get_flag(xor(decrypted_chall,b'\xff'*8 + b'\x00'*56))
print(flag)



