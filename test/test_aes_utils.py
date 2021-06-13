import sys
import numpy as np

sys.path.insert(1, '..')

from aes_utils import SBOX
from aes_utils import SubBytes
from aes_utils import ShiftRows
from aes_utils import MixColumns
from aes_utils import AddRoundKey
from aes_utils import ExpandKeys
from aes_reference import AES as refAES
from aes_reference import text2matrix


def test_SubBytes():
    pts = np.random.randint(0, 256,
                           size=(200,4,4), dtype=np.uint8)
    goods = []
    for pt in pts:
        int_pt = int.from_bytes(pt.tobytes(), 'big')
        goods.append(refAES.sub_bytes(text2matrix(int_pt)))
    goods = np.array(goods)
    updated = SubBytes(pts)

    assert np.all(goods == updated)


def test_ShiftRows():
    pts = np.random.randint(0, 256,
                           size=(200,4,4), dtype=np.uint8)
    goods = []
    for pt in pts:
        int_pt = int.from_bytes(pt.tobytes(), 'big')
        goods.append(refAES.shift_rows(text2matrix(int_pt)))
    goods = np.array(goods)
    updated = ShiftRows(pts)

    assert np.all(goods == updated)


def test_MixColumns():
    pts = np.random.randint(0, 256,
                           size=(200,4,4), dtype=np.uint8)

    goods = []

    for pt in pts:
        int_pt = int.from_bytes(pt.tobytes(), 'big')
        goods.append(refAES.mix_columns(text2matrix(int_pt)))

    goods = np.array(goods)
    updated = MixColumns(pts)

    assert np.all(goods == updated)


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
    
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
        ], dtype=np.uint8)

    ref_aes = refAES(int.from_bytes(key.tobytes(), 'big'))

    good_rks = np.array(ref_aes.round_keys, 
                       dtype=np.uint8).reshape(11, 4, 4)

    rks = ExpandKeys(key)

    assert np.all(good_rks == rks)