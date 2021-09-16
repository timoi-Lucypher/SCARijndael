import sys
import numpy as np
from Crypto.Cipher import AES as pyAES
from aes_reference import AES as refAES
from npcrypto.aes import AES


def test_encryption():
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
        ], dtype=np.uint8)

    ref_aes = refAES(int.from_bytes(key.tobytes(), 'big'))
    my_aes = AES(key)
    pts = np.random.randint(0, 256,
            size=(10, 4, 4), dtype=np.uint8)
    #pts = np.zeros((3, 4, 4), dtype=np.uint8)
    ciphertexts = my_aes.encrypt(pts)

    for i, pt in enumerate(pts):
        good_cipher = ref_aes.encrypt(int.from_bytes(pt.tobytes(), 'big'))
        assert int.from_bytes(ciphertexts[i].tobytes(), 'big') == good_cipher

def test_encryption2():
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
        ], dtype=np.uint8)

    ref_aes = pyAES.new(key.tobytes(),pyAES.MODE_ECB)
    my_aes = AES(key)
    pts = np.random.randint(0, 256,
            size=(100, 4, 4), dtype=np.uint8)
    ciphertexts = my_aes.encrypt(pts)

    for i, pt in enumerate(pts):
        good_cipher = ref_aes.encrypt(pt.tobytes())
        assert ciphertexts[i].tobytes() == good_cipher


def test_decryption():
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
    ], dtype=np.uint8)

    my_aes = AES(key)
    pts = np.random.randint(0, 256,
        size=(100, 4, 4), dtype=np.uint8)
    ciphertexts = my_aes.encrypt(pts)
    decrypted = my_aes.decrypt(ciphertexts)
    assert np.all(decrypted == pts)
