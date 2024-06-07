from transaction import transaction
from objectchain import objectchain

class transactionchain:
    height = 0
    chain = []

    @classmethod
    def __init__ (cls):
        cls.height = 0
        cls.chain = []

    @classmethod
    def createTransaction(cls):
        cls.height += 1
        new_t = transaction(cls.height)
        cls.chain.append(new_t.hash())
        objectchain.addObject(new_t)
        return new_t
    
    @classmethod
    def getLatestTransaction(cls):
        return cls.chain[cls.height - 1]
    
    @classmethod
    def getTransaction(cls, idx):
        try:
            return cls.chain[idx]
        except Exception as e:
            print(e)
            return cls.getLatestTransaction()