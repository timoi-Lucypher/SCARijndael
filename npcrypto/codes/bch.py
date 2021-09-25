from enum import Enum
import numpy as np
from sympy import Poly
from npcrypto.codes.polynomial_helpers import get_gen_poly
from npcrypto.codes.poly_gf2 import p_mul, p_add, p_div, p2a
# Most of the inspiration came from the following documents:
# http://www.comlab.hut.fi/studies/3410/slides_08_6_4.pdf
# https://github.com/jkrauze/bch/tree/master/bch


class Encoder(Enum):
    '''
    This class enumerates the different
    encoding paradigms: systematic and
    non systematic.

    '''
    systematic = 1
    non_systematic = 2


class BCH:
    '''
    This class represents a BCH code.

    '''
    def __init__(self, n: int, m: int, k: int, t: int, q=2):
        '''
        BCH codes are designed thanks to various parameters.
        
        :param n: length of the codeword.
        :param m: dimention of the Galois field (2^m).
        :param k: message bits.
        :param t: Correction capacity of the BCH code (in bits).

        '''
        # Checking some properties of the code
        if m < 3:
            raise ValueError("m must be superior to 3")
        if n != 2**m - 1:
            raise ValueError("n must be equal to 2**m-1")
        if n - k > m * t:
            raise ValueError("must assure n - k < m * t")
        if t >= n:
            raise ValueError("Must assure t < 2**m - 1")

        self.n = n
        self.m = m
        self.k = k
        self.t = t
        self.q = q

        irr, g = get_gen_poly(m, t)
        self.irr_poly = p2a(irr, n)
        self.g_poly = p2a(g, n)
        # Minimal distance of the code
        self.dmin = np.count_nonzero(self.g_poly)

        if self.dmin < 2 * t + 1:
            raise ValueError("Must assure that dmin > 2 * t + 1")

    def set_generator(self, p: np.array):
        '''
        Sets a generator polynomial.

        :param p: the generator polynomial.

        '''
        self.g_poly = p
        self.dmin = np.count_nonzero(self.g_poly)

    def _set_generator(self, p: Poly):
        self.g_poly = p2a(p, self.n)
        self.dmin = np.count_nonzero(self.g_poly)

    def encode(self, messages: np.ndarray, encoder=Encoder.systematic):
        '''
        Wrapper method for encoding, that can be
        wether systematic on non-systematic.

        :param messages: The messages to encode (as bit streams).
        :param encoder: The encoder to use, must be an instance
            of `Encoder` class
        :return: The codewords.

        '''
        if encoder == Encoder.systematic:
            return self._systematic_encode(messages)
        elif encoder == Encoder.non_systematic:
            return self._non_systematic_encode(messages)
        else:
            raise Exception("Unsupported encoder type")

    def _systematic_encode(self, messages: np.ndarray):
        '''
        Systematic encoding process.
        :param messages: the messages to encode
        :return: The codewords.

        '''
        if messages.shape[-1] != self.k:
            raise ValueError("Messages must be of length k bits")

        x_nk = np.zeros(self.n - self.k + 1, dtype=np.uint8)
        x_nk[-1] = 1
        print(x_nk)
        # Multiply the message polynomial by x^(n-k)
        shift_m_poly = p_mul(messages, x_nk)
        print("shifted", shift_m_poly)
        # Divide the result by the generator polynomial
        # and keep the reminder d(x)
        q, r_poly = p_div(shift_m_poly, self.g_poly)
        print("g_poly", self.g_poly)
        print("r_poly", r_poly)
        # the codeword is x^(n-k)m(x) - d(x)
        return p_add(shift_m_poly, r_poly)

    def _non_systematic_encode(self, messages):
        '''
        Systematic encoding process.
        :param messages: the messages to encode
        :return: The codewords.

        '''
        return p_mul(messages, self.g_poly)
