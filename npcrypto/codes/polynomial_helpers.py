from functools import reduce
import numpy as np
from sympy.abc import x, alpha
from sympy import GF, Poly, lcm, ZZ
from sympy.polys.galoistools import gf_irreducible, gf_irreducible_p
# http://www.comlab.hut.fi/studies/3410/slides_08_6_4.pdf
# https://github.com/jkrauze/bch/tree/master/bch
# https://github.com/popcornell/pyGF2


def power_dict(n: int, irr: Poly, p: int):
    '''
    Computes all the apha^i modulo an irreductible polynomial
    for i up to n+1 on a Galois field over p

    :param n: Maximum power to consider.
    :param irr: An irreductible polynomial.
    :param p: prime number on whih the Galois field is defined.

    :return powers: A dictionnary whose keys are the polynomials
        coefficients and values are the alpha power.
    '''
    powers = dict()
    for i in range(1, n + 1):
        test_poly = (Poly(alpha**i, alpha) % irr).set_domain(GF(p))
        powers[tuple(test_poly.all_coeffs())] = i
    return powers


def minimal_poly(i, n, q, irr_poly):
    '''
    Find the minimal polynomial defined by the cyclotomoc coset.
    :param i: The power of alpha.
    :param n: The size of the code.
    :param q: The base of the Gallois field.
    :param irr_poly: The irreductible polynomial.
    :return: The minimal polynomial if found, None otherwise.

    '''
    ti = int(i)
    checked = np.zeros(n, dtype=bool)
    checked[ti] = True
    poly = Poly(x - alpha**ti, x)
    for k in range(n):
        ti = (ti * q) % n
        if checked[ti]:
            polys = [(Poly(c, alpha) % irr_poly).trunc(q)
                     for c in poly.all_coeffs()]
            for p in polys:
                if p.degree() > 0:
                    raise Exception("Couldn't find minimal polynomial")
            coeffs = [p.nth(0) for p in polys]
            return Poly(coeffs, x)
        checked[ti] = True
        poly = poly * Poly(x - alpha**ti, x)
    return None


def all_minimal_poly(n: int, t: int, irr_poly: Poly, q=2):
    '''
    Computes all minimal polynomials from alpha to alpha^2t.

    :param n: Size of the code.
    :param t: Maximum number of errors.
    :param irr_poly: irreductible polynomial.
    :param q: base of the Gallois field.
    :return m_ps: a (k, v) dictionnary, the keys are
        the polynomials and values are the powers of alpha.

    '''
    m_ps = {}
    m_ps[minimal_poly(1, n, q, irr_poly)] = 1

    # Every even power of alpha in this sequence has the same
    # minimal polynomial as some preceding odd power of alpha.
    # (equation 6.3 of Error control Coding, fundamentals and applications).
    for i in range(3, 2 * t, 2):
        min_poly = minimal_poly(i, n, q, irr_poly)
        # Only keep one instance of the polynomial
        if min_poly not in m_ps.keys():
            m_ps[min_poly] = i
    return m_ps


def get_irr_poly(m: int, q=2):
    '''
    Get irreductible polynomial for the given parameters.
    An irreductible polynomial over GF(2) of degree m divides X^n + 1,
    with n = 2^m-1.

    :param m: polynomial's degree.
    :param q: base prime of the Galois field (default 2).
    :return: the irreductible polynomial.

    '''
    n = 2**m - 1
    irr_poly = Poly(alpha**m + alpha + 1, alpha).set_domain(GF(q))
    # If the polynomial is irreductible, update the quotient size
    if gf_irreducible_p([int(c) for c in irr_poly.all_coeffs()], q, ZZ):
        quotient_size = len(power_dict(n, irr_poly, q))
    else:
        quotient_size = 0
    while quotient_size < n:
        # TODO: Could cause infinite loops, correct this
        irr_poly = Poly([int(c.numerator) for c in gf_irreducible(m, q, ZZ)],
                        alpha)
        quotient_size = len(power_dict(n, irr_poly, q))
    return irr_poly


def get_gen_poly(m: int, t: int, q=2):
    '''
    Generate a generator polynomial G(X).
    Let alpha be a primitive element in GF(2^m).
    The generator polynomial of a t-error-correcting
    BCH code of length 2^m - 1 is the lowest-degree polynomial
    over GF(2) which have alpha, alpha^2 ... alpha^2t as its roots.
    Let Mi(X) be the minimal polynomial for alpha^i,
    the G(X) = LCM{M1(X),...,M2t(X)}.

    :param m: dimention of the Galois field q^m.
    :param t: the number of errors that can be corrected.
    :param q: base prime of the Galois field (default 2).
    :return: a tuple (irr_poly, g_poly) containing the irreductible
        polynomial and the generator polynomial.

    '''
    # TODO: Raise errors if theorems are not validated

    n = 2**m - 1
    irr_poly = get_irr_poly(m, q=q)
    m_ps = all_minimal_poly(n, t, irr_poly, q=q)
    print(m_ps)
    g_poly = reduce(lcm, m_ps.keys())
    g_poly = g_poly.trunc(q)
    return irr_poly, g_poly
