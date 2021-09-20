import numpy as np

MAX_ROUNDS = 18

RC = np.array([
    0x01, 0x82, 0x8a, 0x00, 0x8b, 0x01, 0x81, 0x09, 0x8a, 0x88, 0x09, 0x0a,
    0x8b, 0x8b, 0x89, 0x03, 0x02, 0x80
],
              dtype=np.uint8)

RHO_OFFSETS = np.array([[0, 1, 6, 4, 3], [4, 4, 6, 7, 4], [3, 2, 3, 1, 7],
                        [1, 5, 7, 5, 0], [2, 2, 5, 0, 6]],
                       dtype=np.uint8)


def ROL8(states, offset):
    '''
    Elementwise 8 bit roll of given offset.

    :param states: (N, 5, 5) Keccak states.
    :param offset: left rolling offset.

    :return: The updated states

    '''
    return (states << offset) ^ (states >> 8 - offset)


def theta(states: np.ndarray):
    '''
    Numpy implementation of keccak Theta fuction.

    :param states: (N, 25) Keccak state.
    :return: The updated states.

    '''
    states = states.reshape(states.shape[0], 5, 5)
    C = np.bitwise_xor.reduce(states, axis=-2)
    C1 = np.roll(C, shift=-1, axis=-1)
    C4 = np.roll(C, shift=-4, axis=-1)
    D = ROL8(C1, 1) ^ C4
    D = np.repeat(D, 5, axis=-2).reshape(states.shape[0], 5, 5)
    states = states ^ D
    return states.reshape(states.shape[0], 25)


def rho(states: np.ndarray):
    '''
    Numpy implementation of keccak Rho fuction.

    :param states: (N, 25) Keccak state.
    :return: The updated states.

    '''
    states = states.reshape(states.shape[0], 5, 5)
    states = ROL8(states, RHO_OFFSETS)
    return states.reshape(states.shape[0], 25)


def pi(states: np.ndarray):
    '''
    Numpy implementation of keccak Pi fuction.
    Uses a precomputed permutation matrix.

    :param states: (N, 25) Keccak state.
    :return: The updated states.

    '''
    p_mat = np.array([
        0, 6, 12, 18, 24, 3, 9, 10, 16, 22, 1, 7, 13, 19, 20, 4, 5, 11, 17, 23,
        2, 8, 14, 15, 21
    ],
                     dtype=np.uint8)
    return states[:, p_mat]


def chi(states: np.ndarray):
    '''
    Numpy implementation of keccak Chi fuction.

    :param states: (N, 25) Keccak state.
    :return: The updated states.

    '''
    states = states.reshape(states.shape[0], 5, 5)
    A1 = np.roll(states, -1, axis=-1)
    A2 = np.roll(states, -2, axis=-1)
    states = states ^ (np.invert(A1) & A2)
    return states.reshape(states.shape[0], 25)


def iota(states: np.ndarray, round_index: int):
    '''
    Numpy implementation of keccak Iota fuction.

    :param states: (N, 25) Keccak state.
    :param round_index: the round index.
    :return: The updated states.

    '''
    states[:, 0] ^= RC[round_index]
    return states


def keccak_round(states: np.ndarray, round_index: int):
    '''
    Numpy implementation of one keccak round.

    :param states: (N, 25) Keccak state.
    :param round_index: the round index.
    :return: The updated states.

    '''
    states = theta(states)
    states = rho(states)
    states = pi(states)
    states = chi(states)
    states = iota(states, round_index)
    return states


def permutation(states: np.ndarray):
    '''
    Perform Keccak cryptographic permutation over
    an numpy array.

    :param states: (N, 25) Keccak state.
    :return: The updated states.

    '''
    for i in range(MAX_ROUNDS):
        states = keccak_round(states, i)
    return states
