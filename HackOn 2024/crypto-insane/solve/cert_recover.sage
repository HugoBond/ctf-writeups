
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse

def reverse_cos(cos):
    bits = 4096
    arccosQ = arccos(cos)
    pie = pi.n(bits)
    L = matrix(QQ, [[1, 0, 0], [arccosQ, 1, 0], [pie, 0, 1]])
    L[:, 0] *= 2**bits
    L = L.LLL()
    k = int(L[0][-1])
    return abs(int(k*pie + arccosQ))

def rsa_high_bits_known(n, upper):
    x = PolynomialRing(Zmod(n),'x', implementation='NTL').gen(); 
    pol = upper + x
    beta = 0.43
    XX = 2**450
    epsilon = beta / 7
    rt = pol.small_roots(XX,beta, epsilon)
    return upper + rt[0]
    
    

def read_pubKey(filename):
    with open(filename, 'rb') as f:
        pub = RSA.importKey(f.read())
    return pub.n,pub.e

def main():
    N,e = read_pubKey("server-cert.pem")
    print(f"N = {N}")
    msb_q = reverse_cos(RealNumber(-0.83677025469083783941541701752761854754793836436580928644247008941810266469532458996045447348443859400152817824525738732652478723578550322419681449352934903962868272432839950443728133311767399079690030001079242722034971856216464693298008475334803612328029119715730610948114017183466860376219520135065944451843458471230390067711216822465611823803314088335568327990572989813880317949003496128817743756941657517592732976171161188449564836856703887590653409218974871687234942350215936871374265782174012360582549759635891009261305443677350659234691411334888094583016691447506478413851786692210332884103069291530840376504431016357464401672842279159473862600445695092589720790836314505433051945268839223026728538635526261735680020640125514694922387865117641745486767737807560114356069413145843513030254057578430063498955558945235100024577603060294061771113596755818633721728098654211982059793050427304804021628754473574523763161349682175284850419236582818156064980865716476145483816198034274679778084438576624517718459301374217997767985615596748052223448537502912453071556058736828589970943263917953424626006378389407199956646994682638376389500968564930356704561568053846692273026900362154710217069324829901876963571359354949212621973636284))
    print(f"msb_q = {msb_q}")
    q = int(rsa_high_bits_known(N, (msb_q << 450)))
    p = N // q
    print(f"p = {p}\nq = {q}")
    assert p*q == N

    print("N factorization completed")
    d = inverse(e,(p - 1) * (q - 1))
    priv = RSA.construct((int(N), int(e), int(d)))
    with open('priv2.pem','wb') as file:
        file.write(priv.exportKey('PEM'))

if __name__ == '__main__':
    main()