#Blockchain
import hashlib
from Kademlia_MLCU.Kademlia_node import Kademlia_node


class objectchain:
    height = 0
    chain = []
    data_class = [[] for i in range(6)]

    # Header and Body

    @classmethod
    def __init__ (cls):
        cls.height = 0
        cls.chain = []
    
    @classmethod
    def addObject(cls, obj):
        cls.chain.append(obj)
        cls.add_data_class_list(obj, cls.height)
        cls.height += 1

    @classmethod
    def getLatestObject(cls):
        return cls.chain[cls.height - 1]
    
    @classmethod
    def getObject(cls, idx):
        try:
            return cls.chain[idx]
        except Exception as e:
            return cls.getLatestObject()
        
    @classmethod
    def add_data_class_list(cls, obj, idx):
        if obj.type == "block":
            cls.data_class[0].append(idx)
        else: # obj.type == "Transaction"
            cls.data_class[obj.data_class].append(idx)

    def hash(obj):
        hash =  hashlib.sha1()
        hash.update(str(obj).encode())
        hash_value = hash.digest()
        hash_value = int.from_bytes(hash_value, "big") & ((1 << Kademlia_node.ID_space) - 1) #ID_Spaceになるよう調整
        return hash_value
        