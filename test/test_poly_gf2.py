import numpy as np
import pytest
from sympy import Poly, GF, div
from sympy.abc import x, alpha
from npcrypto.codes.poly_gf2 import strip_zeros, deg, a2p, p_mul, p_div, indep_roll
# Most of the test usecases are coming from "Error control coding fundamentals"

def test_deg():
    d1 = np.array([0, 0, 1, 0, 0], dtype=np.uint8)
    assert deg(d1) == 2
    d2 = np.array([[0, 0, 1, 0, 0], [1, 0, 1, 1, 0]], dtype=np.uint8)
    assert np.all(deg(d2) == np.array([2, 3]))

def test_indep_roll():
    A = np.array([[1,2,3,4],
              [1,2,3,4],
              [1,2,3,4]])
    r = np.array([1,-1,3])
    expected = np.array([[4, 1, 2, 3],
                        [2, 3, 4, 1],
                        [2, 3, 4, 1]])
    print(indep_roll(A, r))
    assert np.all(indep_roll(A, r) == expected)

def test_p_mul():
    n = 100
    m = 30
    # Numpy version
    a = np.random.randint(2, size=(n, m), dtype=np.uint8)
    b = np.random.randint(2, size=(n, m), dtype=np.uint8)
    # Sympy version 
    p_a = a2p(a)
    p_b = a2p(b)
    
    # 1d vs 1d
    c = p_mul(a[0], b[0])
    p_c = p_a[0] * p_b[0]
    assert np.all(p_c.all_coeffs()[::-1] == strip_zeros(c))
    
    # Test convolution
    assert np.all(strip_zeros(c) == strip_zeros(p_mul(a[0], b[0], use_fft=False)))

    # 2d vs 1d
    c = p_mul(a, b[0])
    print(c.shape)
    for i in range(a.shape[0]):
        p_c = p_a[i] * p_b[0]
        assert np.all(p_c.all_coeffs()[::-1] == strip_zeros(c[i]))
    
    # 1d vs 2d
    c = p_mul(a[0], b)
    print(c.shape)
    for i in range(a.shape[0]):
        p_c = p_a[0] * p_b[i]
        assert np.all(p_c.all_coeffs()[::-1] == strip_zeros(c[i]))
    
    # Test convolution
    with pytest.raises(ValueError):
        p_mul(a, b[0], use_fft=False)
    
    # 2d vs 2d
    c = p_mul(a, b)
    print(c.shape)
    for i in range(a.shape[0]):
        p_c = p_a[i] * p_b[i]
        assert np.all(p_c.all_coeffs()[::-1] == strip_zeros(c[i]))


def test_p_div():
    
    n = 20
    m = 1000
    # Numpy version
    a = np.random.randint(2, size=(n, m), dtype=np.uint8)
    b = np.random.randint(2, size=(n, m-7), dtype=np.uint8)
    # Sympy version 
    p_a = a2p(a)
    p_b = a2p(b)
    
    # 1d vs 1d
    print("a0",strip_zeros(a[0]))
    print("b0", strip_zeros(b[0]))
    q, r = p_div(a[0], b[0])
    p_q, p_r = div(p_a[0], p_b[0], domain=GF(2))
    print("numpy", list(strip_zeros(q)), list(strip_zeros(r)))
    print("poly", p_q.all_coeffs()[::-1], p_r.all_coeffs()[::-1])
    print("------------------")
    assert np.all(p_q.all_coeffs()[::-1] == strip_zeros(q))
    assert np.all(p_r.all_coeffs()[::-1] == strip_zeros(r))

    # 2d vs 1d
    print("\n\n2D vs 1D\n\n")
    q, r = p_div(a, b[0])
    for i in range(a.shape[0]):
        p_q, p_r = div(p_a[i], p_b[0])
        print("i = ",i) 
        print("poly",p_q.all_coeffs()[::-1], p_r.all_coeffs()[::-1])
        print("numpy", list(strip_zeros(q[i])), list(strip_zeros(r[i])))
        print("------------------")
        assert np.all(p_q.all_coeffs()[::-1] == strip_zeros(q[i]))
        assert np.all(p_r.all_coeffs()[::-1] == strip_zeros(r[i]))
    
    # 1d vs 2d
    q, r = p_div(a[0], b)
    for i in range(a.shape[0]):
        p_q, p_r = div(p_a[0], p_b[i])
        print(p_q.all_coeffs()[::-1], p_r.all_coeffs()[::-1])
        print(list(strip_zeros(q[i])), list(strip_zeros(r[i])))
        print("------------------")
        assert np.all(p_q.all_coeffs()[::-1] == strip_zeros(q[i]))
        assert np.all(p_r.all_coeffs()[::-1] == strip_zeros(r[i]))
    
    # 2d vs 2d
    q, r = p_div(a, b)
    for i in range(a.shape[0]):
        p_q, p_r = div(p_a[i], p_b[i])
        print(p_q.all_coeffs()[::-1], p_r.all_coeffs()[::-1])
        print(list(strip_zeros(q[i])), list(strip_zeros(r[i])))
        print("------------------")
        assert np.all(p_q.all_coeffs()[::-1] == strip_zeros(q[i]))
        assert np.all(p_r.all_coeffs()[::-1] == strip_zeros(r[i]))
    # 
