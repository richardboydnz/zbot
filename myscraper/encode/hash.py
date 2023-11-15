from typing import Iterable, Iterator, NewType
from itertools import chain

import hashlib
import ctypes

# The flatten function takes an Iterable of Iterables and chains them into a single Iterator.
def flatten(iterable: Iterable[Iterable]) -> Iterator:
    return chain.from_iterable(iterable)

Hash64 = NewType('Hash64', int)

# The hash64 function takes a string and returns a 64-bit signed integer.
def hash64(s: str) -> int:
    # Create a SHA-256 hash object
    hash_object = hashlib.sha256(s.encode('utf-8'))
    
    # Convert the hex digest to a 64-bit integer using int and modulo to fit in 64 bits
    hash_int = int(hash_object.hexdigest(), 16) % 2**64
    
    # Convert the 64-bit unsigned integer to a signed integer
    hash_signed = ctypes.c_int64(hash_int).value
    
    return hash_signed
