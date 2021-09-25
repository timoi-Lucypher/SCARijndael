import numpy as np
from numpy.fft import fft, ifft
from sympy import Poly, GF
from sympy.abc import x
# https://github.com/popcornell/pyGF2


def strip_zeros(a):
    '''
    Strip un-necessary leading (rightmost) zeroes
    from a polynomial
    '''
    return np.trim_zeros(a, trim='b')


def deg(a: np.ndarray):
    '''
    Returns the degree of polynomials.

    :param a: (n,m) ndarray of n polynomials defined
        on m coefficients or 1 polynomial of m coefficients.
    :return deg: The degree of the provided polynomial,
        array like when mulptiple polynomials provided.

    .. warning::
        This function can be optimized by using numpy buildin functions.
    '''
    if len(a.shape) == 1:
        return np.array([np.max(np.where(a == 1)[0])])
    else:
        out = []
        for e in a:
            out.append(np.max(np.where(e == 1)[0]))
        return np.array(out)


def indep_roll(a: np.ndarray, shifts: np.array):
    '''
    Rolls rows of a matrix independently, inspired by:
    https://stackoverflow.com/questions/20360675/roll-rows-of-a-matrix-independently

    :param a: (n, m) numpy ndarray.
    :param shifts: n array of right shifts (negative values for left shift).

    - Example::

        >>> A = np.array([[1,2,3,4],
        ...               [1,2,3,4],
        ...               [1,2,3,4]])
        >>> r = np.array([1,-1,3])
        >>> indep_roll(A, r)
        np.array([[4, 1, 2, 3],
                  [2, 3, 4, 1],
                  [2, 3, 4, 1]])


    '''
    return np.real(
        ifft(fft(a, axis=1) *
             np.exp(-2 * 1j * np.pi / a.shape[1] * shifts[:, None] *
                    np.r_[0:a.shape[1]][None, :]),
             axis=1).round()).astype(a.dtype)


def a2p(a: np.ndarray):
    '''
    Converts nparray based polynomials to Sympy polynomials.

    :param a: (n,m) ndarray of n polynomials defined
        on m coefficients or 1 polynomial of m coefficients.
    :return p: A Sympy polynomial (or polynomial array).

    .. warning::
        This Function supposes that the rightmost
        bit is the highest coefficient.

    '''
    if len(a.shape) == 1:
        out = Poly(strip_zeros(a)[::-1], x).set_domain(GF(2))
    elif len(a.shape) == 2:
        out = []
        for e in a:
            out.append(Poly(strip_zeros(e)[::-1], x).set_domain(GF(2)))
    else:
        raise Exception("Invalid shape")
    return out


def p2a(p: Poly, size: int):
    '''
    Converts Sympy polynomial to numpy array.

    :param p: Sympy polynomial.
    :param size: Size of the resulting numpy array.
    :return a: The numpy array representing the polynomial.

    '''
    out = np.zeros(size, dtype=np.uint8)
    coeffs = p.all_coeffs()[::-1]
    if len(coeffs) > size:
        raise ValueError("Provided size too small")
    out[:len(coeffs)] = coeffs
    return out


def p_add(a: np.ndarray, b: np.ndarray):
    '''
    Add two polynomials in GF(2)[x].

    :param a: (n,m) ndarray of n polynomials defined
        on m coefficients or 1 polynomial of m coefficients.
    :param b: (n,m) ndarray of n polynomials defined
        on m coefficients.

    '''
    return a ^ b


def p_mul(a: np.ndarray, b: np.ndarray, use_fft=True):
    '''
    Multiply polynomials in GF(2)[x].

    :param a: (n,m) ndarray of n polynomials defined
        on m coefficients or 1 polynomial of m coefficients.
    :param b: (n,m) ndarray of n polynomials defined
        on m coefficients.
    :param fft: Uses fft by default because it speeds up
        computations for big arrays.
        If multiple calls of this function on 1D arrays are required,
        using a convolution (i.e., setting fft to False) can raise
        better performances.
        Convolution is available for 1D arrays only.

    .. warning::
        This Function supposes that the rightmost
        bit is the highest coefficient.

    '''
    if use_fft:
        fsize = a.shape[-1] + b.shape[-1] - 1
        fsize = 2**np.ceil(np.log2(fsize)).astype(int)
        fslice = slice(0, fsize)
        ta = fft(a, fsize)
        tb = fft(b, fsize)
        res = ifft(ta * tb)[..., fslice].copy()
        k = np.mod(np.rint(np.real(res)), 2).astype('uint8')
    else:
        if len(a.shape) > 1 or len(b.shape) > 1:
            raise ValueError("Convolution is only implemented for 1D arrays")
        k = np.mod(np.convolve(a, b), 2).astype("uint8")

    return k


def p_div(dividend: np.ndarray, divisor: np.ndarray):
    '''
    Divide dividend polynomial by divisor polynomial.

    :param dividend: (n,m) ndarray of n polynomials defined
        on m coefficients or 1 polynomial of m coefficients.
    :param divisor: (n,m) ndarray of n polynomials defined
        on m coefficients or 1 polynomial of m coefficients.
    :return (q, r): quotient and remainder polynomials

    '''
    if len(dividend.shape) > 2 or len(divisor.shape) > 2:
        raise Exception("Invalid shape")

    # By default, final shape is 2
    final_shape = 2

    # If dividend is 1d and divisor is 1d, make those two arrays 2D
    if len(dividend.shape) == 1 and len(divisor.shape) == 1:
        dividend = dividend[np.newaxis, :]
        divisor = divisor[np.newaxis, :]
        final_shape = 1

    # If dividend is 1d and divisor is 2d, extend dividend array
    if len(dividend.shape) == 1 and len(divisor.shape) == 2:
        dividend = np.repeat([dividend], repeats=divisor.shape[0], axis=0)

    # If dividend is 2d and divisor is 1d, extend divisor array
    if len(dividend.shape) == 2 and len(divisor.shape) == 1:
        divisor = np.repeat([divisor], repeats=dividend.shape[0], axis=0)

    u = dividend
    v = np.zeros(dividend.shape, dtype=divisor.dtype)
    v[..., :divisor.shape[-1]] = divisor
    # Get the degree of each polynomial
    m = deg(u)
    n = deg(v)

    if not divisor.any():
        raise ZeroDivisionError("polynomial division")

    # Keep track of valid divisions
    # (i.e, polynomials that can actually be divided)
    valid = n <= m
    # Compute shifting factors and roll polynomials
    sh = (m - n).astype(np.int64)
    v = indep_roll(v, sh)
    # Initialize result arrays
    shape = (u.shape[0], max(max(m) - min(n) + 1, 1))
    q = np.zeros(shape, u.dtype)
    r = u.astype(u.dtype)
    # Euclid's algorithm
    while not np.all(sh[valid] == 0):
        # Get the polynomials that can divide
        indexes = n + sh
        do_divide = np.full(indexes.shape[0], False, dtype=bool)
        # TODO: optimize this loop
        for i in range(indexes.shape[0]):
            do_divide[i] = (v[i, indexes[i]] & r[i, indexes[i]]
                            == 1) & valid[i]
        r[do_divide] ^= v[do_divide]
        q[do_divide, sh[do_divide]] = 1
        # Get the polynomials that can be rolled
        do_roll = np.where(sh > 0)[0]
        # Roll them
        v[do_roll] = np.roll(v[do_roll], -1, axis=-1)
        sh[do_roll] -= 1
    # Last iteration is done out of the loop
    indexes = n + sh
    do_divide = np.full(indexes.shape[0], False, dtype=bool)
    # TODO: optimize this loop
    for i in range(indexes.shape[0]):
        do_divide[i] = (v[i, indexes[i]] & r[i, indexes[i]] == 1) & valid[i]
    r[do_divide] ^= v[do_divide]
    q[do_divide, sh[do_divide]] = 1
    if final_shape == 1:
        q = q[0]
        r = r[0]
    return q, r
