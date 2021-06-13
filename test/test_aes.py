import sys
import numpy as np

from Crypto.Cipher import AES as pyAES

sys.path.insert(1, '..')

from aes import AES

def test_encryption():
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
        ], dtype=np.uint8)


    plaintexts = np.random.randint(0, 256,
                                   size=(3, 4, 4),
                                   dtype=np.uint8)

    cipher = pyAES.new(key.T.tobytes(), pyAES.MODE_ECB)

    good_ciphers = []
    for i in range(plaintexts.shape[0]):
        ciphertext = cipher.encrypt(plaintexts[i].tobytes())
        good_ciphers.append(np.frombuffer(ciphertext,
                            dtype=np.uint8).reshape(4,4))

    good_ciphers = np.array(good_ciphers)

    mycipher = AES(key)
    computed_ciphers = mycipher.encrypt(plaintexts)

    for i in range(good_ciphers.shape[0]):
        print(good_ciphers[i])
        print('-----vs ----')
        print(computed_ciphers[i])
        print('\n\n')
    assert np.all(computed_ciphers == good_ciphers)
