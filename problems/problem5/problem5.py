import gmpy2
from gmpy2 import mpz, powmod, invert, gcd
import argparse
import sys
from sys import stderr


# find the discrete log of exp based on the split of the result:
# x = 2 ** limit * x_0 + x_1
# then exp = g ** x implies
# exp / g ** x_0 = (g ** (2 ** limit)) ** x_1
#                = r ** x_1
def discrete_log(prime, generator, exp, limit):
    table = build_table(prime, generator, exp, limit)
    r = powmod(generator, 2 ** limit, prime)
    for x in range(0, 2 ** limit + 1):
        key = powmod(r, x, prime)
        if key in table:
            return (x * (2 ** limit) + table[key]) % prime
    return None

def build_table(prime, generator, exp, limit):
    return { (exp * powmod(generator, -x, prime)) % prime: x for x in range(0, 2 ** limit + 1) }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute the discrete log.')
    parser.add_argument('base', metavar='p', type=mpz, help='a prime')
    parser.add_argument('generator', metavar='g', type=mpz, help='a generator of Z_p')
    parser.add_argument('exp', metavar='x', type=mpz, help='the argument to the discrete log')

    args = parser.parse_args()

    if args.generator >= args.base or args.generator < 0:
        stderr.write('g must be an element of Z_p\n')
        sys.exit(1)

    if gcd(args.base, args.generator) != 1:
        stderr.write('g must be a generator of Z_p\n')
        sys.exit(1)

    if args.exp >= args.base or args.exp < 0:
        stderr.write('x must be an element of Z_p\n')
        sys.exit(1)

    stderr.write('Finding discrete log for parameters:\n')
    stderr.write('prime: ')
    stderr.write(str(args.base))
    stderr.write('\n')
    stderr.write('generator: ')
    stderr.write(str(args.generator))
    stderr.write('\n')
    stderr.write('argument: ')
    stderr.write(str(args.exp))
    stderr.write('\n')
    log = discrete_log(args.base, args.generator, args.exp, 20)
    if log is None:
        stderr.write('could not find discrete log, exponent too large\n')
        sys.exit(1)
    if powmod(args.generator, log, args.base) != args.exp:
        stderr.write('verification step failed\n')
        sys.exit(1)
    print log
