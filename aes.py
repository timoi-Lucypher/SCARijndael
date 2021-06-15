import numpy as np
from aes_utils import MixColumns, SubBytes, ShiftRows
from aes_utils import ExpandKeys, AddRoundKey


class AES:

    def __init__(self, key: np.ndarray):
        '''
        Setup aes key

        :param key: (4, 4) array key
        '''
        self.key = key
        self._round_keys = ExpandKeys(key)

    def encrypt(self, pts: np.ndarray):
        '''
        Encryption of multiple plaintexts

        :param pts: (N, 4, 4) plaintext array
        :return: (N, 4, 4) ciphertexts

        - Example::
            key = np.array([
                [0x2b, 0x7e, 0x15, 0x16],
                [0x28, 0xae, 0xd2, 0xa6],
                [0xab, 0xf7, 0x15, 0x88],
                [0x09, 0xcf, 0x4f, 0x3c]
                ], dtype=np.uint8)

            cipher = AES(key)
            pts = np.random.randint(0, 256,
                    size=(10, 4, 4), dtype=np.uint8)
            ciphertexts = cipher.encrypt(pts)

        '''
        states = AddRoundKey(pts, self._round_keys[0])
        for i in range(1, 10):
            states = SubBytes(states)
            states = ShiftRows(states)
            states = MixColumns(states)
            states = AddRoundKey(states, self._round_keys[i])

        states = SubBytes(states)
        states = ShiftRows(states)
        states = AddRoundKey(states, self._round_keys[10])
        return states
