import numpy as np
from npcrypto.codes.bch import BCH
from npcrypto.codes.poly_gf2 import a2p, strip_zeros

def test_encode():
    #http://www.comlab.hut.fi/studies/3410/slides_08_6_4.pdf
    n = 7
    m = 3
    k = 3
    t = 2

    msg = np.array([1,0,1], dtype=np.uint8)
    expected = np.array([1, 1, 0, 0, 1, 0, 1], dtype=np.uint8)
    bch = BCH(n, m, k, t)
    gen = np.array([1, 0, 1, 1, 1], dtype=np.uint8)
    bch.set_generator(gen)  
    cdw = bch.encode(msg)
    assert np.all(strip_zeros(cdw) == expected)
    

