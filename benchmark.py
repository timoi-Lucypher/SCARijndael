import time
import numpy as np
from Crypto.Cipher import AES as pyAES

from aes import AES

def benchmark_encryption(N):
    key = np.array([
        [0x2b, 0x7e, 0x15, 0x16],
        [0x28, 0xae, 0xd2, 0xa6],
        [0xab, 0xf7, 0x15, 0x88],
        [0x09, 0xcf, 0x4f, 0x3c]
    ], dtype=np.uint8)
    ref_aes = pyAES.new(key.tobytes(), pyAES.MODE_ECB)
    my_aes = AES(key)
    # Generate numpy plaintexts
    pts = np.random.randint(0, 256,
            size=(N, 4, 4), dtype=np.uint8)
    # Translate to bytes
    pts_bytes = []
    for pt in pts:
        pts_bytes.append(pt.tobytes())
    # Compare timings
    start = time.time()    
    for pt in pts_bytes:
        ref_aes.encrypt(pt)
    duration_ref = time.time() - start
    print(f"Reference time: {duration_ref}")
    start = time.time()
    my_aes.encrypt(pts)
    duration = time.time() - start
    print(f"Numpy aes time: {duration}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Numpy AES benchmark.')
    parser.add_argument('--N', dest='N',
                        default=1000,
                        type=int,
                        help='Number of random plaintexts  to encrypt')

    args = parser.parse_args()

    benchmark_encryption(args.N)
