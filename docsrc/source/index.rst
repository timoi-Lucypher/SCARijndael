.. SCARijndael documentation master file, created by
   sphinx-quickstart on Sat Jun 12 10:31:24 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to npCrypto's documentation!
=======================================

npCrypto is a project which goal is to provide Numpy friendly cryptographic primitives.

.. toctree::
   :maxdepth: 2
   :caption: Contents:



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Symmetric primitives
====================

AES helper functions
---------------------
This module implements several AES sub functions.

.. automodule:: npcrypto.aes_utils
   :members:
   :undoc-members: __init__
   :show-inheritance:

AES
----------
.. automodule:: npcrypto.aes
   :members:
   :undoc-members:
   :special-members:
   :show-inheritance:

Keccak
----------
The Keccak cryptographic permutation is used within several cryptosystems such as SHA3 or Elephant.

.. automodule:: npcrypto.keccak
   :members:
   :undoc-members:
   :show-inheritance:

Error correcting codes
=======================
Error correcting codes are heavily used when data can suffer transmition or storage errors.
Thus we developped several functions in order to perform error correction in a Numpy friendly way.

Polynomial operations under Galois field
----------------------------------------
This module aims at providing polynomial operations on multidimentionnal Numpy arrays. 

.. automodule:: npcrypto.codes.poly_gf2
   :members:
   :undoc-members:
   :show-inheritance:

Error correcting codes polynomial helpers
-----------------------------------------
Implementation (mostly in Sympy) of useful polynomal function upon cyclic codes.

.. automodule:: npcrypto.codes.polynomial_helpers
   :members:
   :undoc-members:
   :show-inheritance:

BCH (Bose–Chaudhuri–Hocquenghem) codes 
-----------------------------------------
.. automodule:: npcrypto.codes.bch
   :members:
   :undoc-members:
   :special-members: __init__
   :show-inheritance:

