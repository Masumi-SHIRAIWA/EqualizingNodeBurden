import random
import hashlib
from Kademlia_MLCU.Kademlia_node import Kademlia_node


class transaction:
    def __init__(self, height):
        self.type = "tx"
        self.height = height
        self.contents = random.random()

    
    def hash(self):
        hash =  hashlib.sha1()
        hash.update(str(self).encode())
        hash_value = hash.digest()
        hash_value = int.from_bytes(hash_value, "big") & ((1 << Kademlia_node.ID_space) - 1) #ID_Spaceになるよう調整
        return hash_value
    