#Blockchain
import block
import hashlib
from Kademlia_MLCU.Kademlia_node import Kademlia_node
from objectchain import objectchain


class blockchain:
    height = 0
    chain = []

    @classmethod
    def __init__ (cls):
        cls.height = 0
        cls.chain = []

    @classmethod
    def createBlock(cls, time, TxList):#新しいBlockを作成し、返す
        # 新しいブロックの生成
        prevHash = cls.hash(cls.getLatestBlock().header)
        cls.height += 1
        newBlock = block.block(prevHash, cls.height, time, TxList)
        cls.chain.append(newBlock)
        objectchain.addObject(newBlock)

        # 人気度の更新
        cls.updatePopLevel()

        return newBlock
    
    @classmethod
    def createGeneBlock(cls, time):#新しいBlockを作成し、返す
        # 新しいブロックの生成
        cls.height += 1
        newBlock = block.block(cls.hash(0), cls.height, time, [])
        objectchain.addObject(newBlock)
        cls.chain.append(newBlock)

        return newBlock

    @classmethod
    def getLatestBlock(cls):
        return cls.chain[cls.height - 1]
    
    @classmethod
    def getBlock(cls, idx):
        try:
            return cls.chain[idx]
        except Exception as e:
            return cls.getLatestBlock()
    @classmethod
    def updatePopLevel(cls):
        for i in range(cls.height - 1):
            cls.chain[i].popLevel *= 0.99

    def hash(obj):
        hash =  hashlib.sha1()
        hash.update(str(obj).encode())
        hash_value = hash.digest()
        hash_value = int.from_bytes(hash_value, "big") & ((1 << Kademlia_node.ID_space) - 1) #ID_Spaceになるよう調整
        return hash_value
        