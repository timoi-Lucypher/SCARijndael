import numpy as np
from sympy import Poly, GF
from sympy.abc import x, alpha
from npcrypto.codes.polynomial_helpers import power_dict, minimal_poly, all_minimal_poly, \
    get_irr_poly, get_gen_poly
# Most of the test usecases are coming from "Error control coding fundamentals"

def test_get_irr_poly():
    
    m = 3
    q = 2
    irr_poly = get_irr_poly(m,q=q)
    print(irr_poly)
    assert irr_poly.all_coeffs() == [1, 0, 1, 1]

def test_all_minimal_poly():
    n = 15
    q = 2
    t = 3
    irr_poly = Poly(1 + alpha + alpha**4, alpha)
    m_ps = all_minimal_poly(n, t, irr_poly, q=q)
    for poly, power in m_ps.items():
        if power == 1:
            assert poly.all_coeffs() == [1, 0, 0, 1, 1] 
        elif power == 3:
            assert poly.all_coeffs() == [1, 1, 1, 1, 1]
        elif power == 5:
            assert poly.all_coeffs() == [1 ,1 ,1]

def test_get_gen_poly():
    m = 4 
    irr, g = get_gen_poly(m, 2)
    # x**8 + x**7 + x**6 + x**4 + 1
    assert g.all_coeffs() == [1, 1, 1, 0, 1, 0, 0, 0, 1]
    irr, g = get_gen_poly(m, 3)
    # x**10 + x**8 + x**5 + x**4 + x**2 + x + 1
    assert g.all_coeffs() == [1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1]
