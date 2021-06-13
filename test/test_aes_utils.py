import sys
import numpy as np

sys.path.insert(1, '..')

from aes_utils import SBOX
from aes_utils import SubBytes
from aes_utils import ShiftRows
from aes_utils import MixColumns
from aes_utils import AddRoundKey
from aes_utils import ExpandKeys

def test_SubBytes():

    states = np.random.randint(0, 256, 
                               size=(10, 4, 4),
                               dtype=np.uint8)
    updated = SubBytes(states)

    assert updated.shape == (10, 4, 4)
    for n, state in enumerate(states):
        for i in range(4):
            for j in range(4):
                assert SBOX[state[i, j]] == updated[n, i, j]

def test_ShiftRows():
    s0 = np.arange(0, 16, dtype=np.uint8).reshape(4,4)
    s1 = np.arange(16, 32, dtype=np.uint8).reshape(4,4)
    s2 = np.arange(32, 48, dtype=np.uint8).reshape(4,4)

    states = np.array([s0, s1, s2])

    updated = ShiftRows(states)

    good = np.array([
                      [[0, 1, 2, 3],
                       [5, 6, 7, 4],
                       [10, 11, 8, 9],
                       [15, 12, 13, 14]],

                      [[16, 17, 18, 19],
                       [21, 22, 23, 20],
                       [26, 27, 24, 25],
                       [31, 28, 29, 30]],

                       [[32 ,33 ,34 ,35],
                        [37 ,38 ,39 ,36],
                        [42 ,43 ,40 ,41],
                        [47 ,44 ,45 ,46]]], dtype=np.uint8)
    assert np.all(updated == good)


def test_MixColumns():
    s0 = np.arange(0, 16, dtype=np.uint8).reshape(4,4)
    s1 = np.arange(16, 32, dtype=np.uint8).reshape(4,4)
    s2 = np.arange(32, 48, dtype=np.uint8).reshape(4,4)

    states = np.array([s0, s1, s2])
    updated = MixColumns(states)

    good = np.array(
        [
        [[ 8, 9, 10, 11],
         [28, 29, 30, 31],
         [ 0, 1, 2, 3],
         [20, 21, 22, 23]],

        [[24, 25, 26, 27],
         [12, 13, 14, 15],
         [16, 17, 18, 19],
         [4, 5, 6, 7]],

        [[40, 41, 42, 43],
         [60, 61, 62, 63],
         [32, 33, 34, 35],
         [52, 53, 54, 55]]], dtype=np.uint8)

    assert np.all(updated == good)


def test_AddRoundKey():
    s0 = np.tile(np.uint8(3), (4,4))
    s1 = np.tile(np.uint8(4), (4,4))
    s2 = np.tile(np.uint8(5), (4,4))

    states = np.array([s0, s1, s2])

    rk = np.tile(np.uint8(12), (4, 4))

    updated = AddRoundKey(states, rk)

    assert np.all(updated[0] == 15)
    assert np.all(updated[1] == 8)
    assert np.all(updated[2] == 9)

def test_ExpandKeys():
    # TODO: TEST the entire key expansion
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
        ], dtype=np.uint8)

    rk1 = np.array([
        [0xa0, 0xfa, 0xfe, 0x17],
        [0x88, 0x54, 0x2c, 0xb1],
        [0x23, 0xa3, 0x39, 0x39],
        [0x2a, 0x6c, 0x76, 0x05]
        ], dtype=np.uint8)
    keys = ExpandKeys(key)

    assert np.all(keys[0] == key)
    print(rk1)
    print()
    print(keys[1])
    assert np.all(keys[1] == rk1)
