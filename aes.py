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
