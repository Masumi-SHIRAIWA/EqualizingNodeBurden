#Access patern class
import time
import sympy as sym
import numpy as np
from matplotlib import pyplot as plt
import block
import blockchain
from transactionchain import transactionchain
from objectchain import objectchain
import node
import random

class access_pattern:
    pattern = ""
    num = 0 # 1回のアクセス処理でアクセスが発生するTx数
    # 3 transactions are generated per one second in bitcoin. assuming that one transaction is relevant to 2 transactions.

    def Access(cls, nodes):
        if cls.pattern == "UNIFORM":
            return cls.UniformAccessPattern(nodes)
        elif cls.pattern == "EXPONENTIAL_DECAYING":
            return cls.ExponentialDecayingAccessPattern(nodes)
        else:
            raise NameError("アクセスパターンの名称が違います．Configファイルを変更してください．UNIFORM or EXPONENTIAL_DECAYINGです．")

    def UniformAccessPattern(cls, nodes):
        total_access = 0
        remote_access = 0
        for n in nodes:
            for i in range(cls.num):
                total_access += 1
                idx = int(random.uniform(0,objectchain.height))
                obj = objectchain.getObject(idx)
                if obj.type == "block":
                    remote_access += n.accessToBlock(obj)
                else:
                    remote_access += n.accessToTx(obj)
                        
        if total_access == 0 : return 0
        else: return (remote_access / total_access) * 100
            
    def ExponentialDecayingAccessPattern(cls, nodes):
        total_access = 0
        remote_access = 0
        for n in nodes:
            for i in range(cls.num):
                total_access += 1
                idx = int(1.1 * random.expovariate(0.1) * 100) 
                obj = objectchain.getObject(-idx-1)
                if obj.type == "block":
                    remote_access += n.accessToBlock(obj)
                else:
                    remote_access += n.accessToTx(obj)
        
        if total_access == 0 : return 0
        else: return (remote_access / total_access) * 100
