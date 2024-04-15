from Crypto.Util import number
from Crypto.Hash import SHA512
from pwn import remote
from sage.all import GF
import random

p = 32148430219533869432664086521225476372736462680273996089092113172047080583085077464347995262368698415917196323365668601969574610671154445337781821758494432339987784268234681352859122106315479086318464461728521502980081310387167105996276982251134873196176224643518299733023536120537865020373805440309261518826398579473063255138837294134742678213639940734783340740545998610498824621665838546928319540277854869576454258917970187451361767420622980743233300167354760281479159013996441502511973279207690493293107263225937311062981573275941520199567953333720369198426993035900390396753409748657644625989750046213894003084507
q = 25652174680121164880516494520695513229510497175386947962678706338003
g = 23174059265967833044489655691705592548904322689090091191484900111607834369643418104621577292565175857016629416139331387500766371957528415587157736504641585483964952733970570756848175405454138833698893579333073195074203033602295121523371560057410727051683793079669493389242489538716350397240122001054430034016363486006696176634233182788395435344904669454373990351188986655669637138139377076507935928088813456234379677586947957539514196648605649464537827962024445144040395834058714447916981049408310960931998389623396383151616168556706468115596486100257332107454218361019929061651117632864546163172189693989892264385257
A = 30210424620845820052071225945109142323820182565373787589801116895962027171575049058295156742156305996469210267854774935518505743920438652976152675486476209694284460060753584821225066880682226097812673951158980930881565165151455761750621260912545169247447437218263919470449873682069698887953001819921915874928002568841432197395663420509941263729040966054080025218829347912646803956034554112984570671065110024224236097116296364722731368986065647624353094691096824850694884198942548289196057081572758803944199342980170036665636638983619866569688965508039554384758104832379412233201655767221921359451427988699779296943487

server = remote("gold.b01le.rs", 5005)
h = SHA512.new(truncate="256")
h.update(number.long_to_bytes(g) + number.long_to_bytes(p) + number.long_to_bytes(A))
c = number.bytes_to_long(h.digest()) % p

c_2 = c //2
c_2_inv = pow(c_2,-1,p-1)
print((c_2_inv*c) % (p-1))
F = GF(p)
invA = pow(A,-1,p)
invc = c_2_inv#pow(c,-1,p-1)
z= random.randint(0, p-1)
gz = pow(g,z,p)

half_gz = F(gz).sqrt()
half_invA = F(invA).sqrt()


num=(half_gz * half_invA) % p
X=pow(num,invc,p)
print (f"z={z}, A={A}")
print (f"X={X}")

server.recvuntil(b"a + cx = ")
server.sendline(str(z).encode())
server.recvuntil(b"> X = ")
server.sendline(str(X).encode())
server.interactive()

'''
print("== Now checking ==")
check=(A*pow(X,c,p)) %p
gz=(pow(g,z,p)) %p
print (f"\nA.X^c={check}, g^z={gz}")
'''