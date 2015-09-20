import gmpy2

from gmpy2 import mpz, isqrt, isqrt_rem, powmod, is_even

N1 = mpz('17976931348623159077293051907890247336179769789423065727343008115 \
        77326758055056206869853794492129829595855013875371640157101398586 \
        47833778606925583497541085196591615128057575940752635007475935288 \
        71082364994994077189561705436114947486504671101510156394068052754 \
        0071584560878577663743040086340742855278549092581')

N2 = mpz('6484558428080716696628242653467722787263437207069762630604390703787 \
        9730861808111646271401527606141756919558732184025452065542490671989 \
        2428844841839353281972988531310511738648965962582821502504990264452 \
        1008852816733037111422964210278402893076574586452336833570778346897 \
        15838646088239640236866252211790085787877')

N3 = mpz('72006226374735042527956443552558373833808445147399984182665305798191 \
        63556901883377904234086641876639384851752649940178970835240791356868 \
        77441155132015188279331812309091996246361896836573643119174094961348 \
        52463970788523879939683923036467667022162701835329944324119217381272 \
        9276147530748597302192751375739387929')

def scan(n, x, y):
    parity = 0 if is_even(x + y) else 1
    a, r = isqrt_rem(x * y * n)
    i = a
    while True:
        if (4 * i ** 2 - 4 * parity * i - 4 * x * y * n + parity) < 0:
            i = i + 1
            continue
        z, rem = isqrt_rem(4 * i ** 2 - 4 * parity * i - 4 * x * y * n + parity)
        if rem == 0:
            p = i + (z - parity) / 2
            q = i - (z + parity) / 2
            p = reduce(p, x, y)
            q = reduce(q, x, y)
            assert p * q == n
            return q, p
        i = i + 1

def reduce(n, *primes):
    x = n
    for p in primes:
        if x % p == 0:
            x = x / p
    return x

def factor(n, x, y):
    print 'Factoring'
    print n
    p, q = scan(n, x, y)
    print 'Smaller factor'
    print p
    print 'Bigger factor'
    print q

factor(N1, 1, 1)
factor(N2, 1, 1)
factor(N3, 3, 2)

CHALLENGE = mpz('22096451867410381776306561134883418017410069787892831071731839143676135600120538004282329650473509424343946219751512256465839967942889460764542040581564748988013734864120452325229320176487916666402997509188729971690526083222067771600019329260870009579993724077458967773697817571267229951148662959627934791540')

def decrypt(challenge, e, n, x, y):
    p, q = scan(n, x, y)
    phi = n - p - q + 1
    d = powmod(e, -1, phi)
    m = powmod(challenge , d, n)
    assert powmod(m, e, n) == challenge
    mhex = "%x" % m
    return mhex[mhex.find("00") + 2:].decode("hex")

print decrypt(CHALLENGE, 65537, N1, 1, 1)
