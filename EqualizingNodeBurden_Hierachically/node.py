# Node class
import block
import blockchain
from transaction import transaction
from transactionchain import transactionchain
from Kademlia_MLCU.index import index
from Kademlia_MLCU.Kademlia_node import Kademlia_node
import statistics
import random

class node (Kademlia_node):

    current_time = 0
    
    def __init__(self, ip, port, layer, resAbility, TimeThre1, TimeThre2, num_layer): #IP, Port, ストレージ容量（ブロック数）を指定
        super().__init__(ip, port, layer)
        # self.layer = layer

        self.HighFreqStorage = index() #HighFreqStorage
        self.ReponseAbility = resAbility

        self.HeaderStorage = index()
        self.TxhashStorage = index()

        self.TimeThre1 = TimeThre1
        self.TimeThre2 = TimeThre2

        self.AccessedBlocks = []
        self.AccessedTxs = []

        self.numOfResponsedFrom = [0 for _ in range(num_layer)]

        self.accessProbabilityList = [0.04 for _ in range(6)]
        self.accessProbabilityList[random.randint(1,5)] = 0.8
        self.accessProbabilityList = [element / sum(self.accessProbabilityList) for element in self.accessProbabilityList]

    def __repr__(self):
        return f'(L: {self.layer},ID: {self.node_ID})'
    
    def saveNewBlock(self, newBlock):
        #ヘッダに保存する
        key = self.hash(newBlock.header)

        self.HeaderStorage.set_value(key, {"header" : newBlock.header, "height" : newBlock.header["height"], "geneTime" : newBlock.header["TimeStamp"] , "LastUsedTime" : newBlock.header["TimeStamp"]})
        #HighFreqStorage領域に保存する
        self.store_to_HighFreqStorage(key, newBlock.body)

    def saveNewTx(self, newTx):
        #ヘッダに保存する
        key = newTx.hash()

        self.TxhashStorage.set_value(key, {"height" : newTx.height, "geneTime" : self.current_time , "LastUsedTime" : self.current_time})
        #HighFreqStorage領域に保存する
        self.store_to_HighFreqStorage(key, newTx)

        
    def accessToBlock(self, block):
        key = self.hash(block.header)
        block_height = self.HeaderStorage.get_value(key)["height"]
        if block_height not in self.AccessedBlocks:
            self.AccessedBlocks.append(block_height)
        
        isRemote, value = self.lookup_value(key)
        self.store_to_HighFreqStorage(key, value)
        return isRemote
        
    def accessToTx(self, Tx):
        key = Tx.hash()
        # Tx_height = self.TxhashStorage.get_value(key)["height"]
        # if Tx_height not in self.AccessedTxs:
        #     self.AccessedTxs.append(Tx_height)
        
        isRemote, _value = self.lookup_value(key)
        self.store_to_HighFreqStorage(key, _value)
        return isRemote

    def lookup_value(self, key):
        value, new_burden = self.find_value(key, self, self.burden)
        self.table.update_burden_table(self.node_ID, new_burden)
        if value != None: # 自分のStoargeにあった場合
            return 0,value
        else : # 自分のStorageにはなかった場合
            value, resLayer = super().lookup_value(key)
            self.numOfResponsedFrom[resLayer] += 1
            return 1,value

    def find_value(self, key, callerNode, new_burden): #value or Noneを返す
        value = None
        try:
            self.updateHeaderIndex(key)
        except KeyError as e:
            self.updateTxhashIndex(key)
        
        self.table.update_burden_table(callerNode.node_ID, new_burden)
        try:
            value =  self.HighFreqStorage.get_value(key)
        except KeyError as e:
            value = super().find_value(key)
        if callerNode != self:
            if value != None:
                self.currentDataTraffic += 1
                self.totalNodeBurden += 1
        
        return value, self.burden

    def store_to_HighFreqStorage(self, key, value): #上限はないとする
        if key in self.LowFreqStorage:
            return True
        if key in self.ZeroFreqStorage:
            return True
        try:
            self.HighFreqStorage.set_value(key, value)
            return True
        except:
            return False
    
    def store_to_LowFreqStorage(self, key, value, callerNode, new_burden):
        self.table.update_burden_table(callerNode.node_ID, new_burden)
        if key in self.HighFreqStorage:
            self.HighFreqStorage.delete_value(key)
        return super().store_to_LowFreqStorage(key, value), self.burden
    
    def store_to_ZeroFreqStorage(self, key, value, callerNode, new_burden):
        self.table.update_burden_table(callerNode.node_ID, new_burden)
        if key in self.HighFreqStorage:
            self.HighFreqStorage.delete_value(key)

        if key in self.LowFreqStorage:
            self.LowFreqStorage.delete_value(key)
        return super().store_to_ZeroFreqStorage(key, value), self.burden

    def checkDataAndCurrentBurden(self, key):
        return super().checkDataAndCurrentBurden(key), self.burden

    # Delete part
    def getInactiveDataKeyLists(self, current_time):
        LowActiveDataKeyList = []
        ZeroActiveDataKeyList = []

        for k in self.HighFreqStorage.keys():
            try:
                if current_time - self.HeaderStorage.get_value(k)["LastUsedTime"] >= self.TimeThre1:
                    LowActiveDataKeyList.append(k)
            except KeyError:
                if current_time - self.TxhashStorage.get_value(k)["LastUsedTime"] >= self.TimeThre1:
                    LowActiveDataKeyList.append(k)
            
        for k in self.LowFreqStorage.keys():
            try:
                if current_time - self.HeaderStorage.get_value(k)["LastUsedTime"] >= self.TimeThre2:
                    ZeroActiveDataKeyList.append(k)
            except KeyError:
                if current_time - self.TxhashStorage.get_value(k)["LastUsedTime"] >= self.TimeThre2:
                    ZeroActiveDataKeyList.append(k)

            
        return LowActiveDataKeyList, ZeroActiveDataKeyList
    
    def deleteAndPublishInactiveData(self):
        LowActiveDataKeyList, ZeroActiveDataKeyList = self.getInactiveDataKeyLists(self.current_time)

        for k in LowActiveDataKeyList:
            # print(self.node_ID, "のHighStorageでデータを削除します")
            value = self.HighFreqStorage.get_value(k)
            self.HighFreqStorage.delete_value(k)
            self.publish_to_LowFreqStorage(k, value)

        for k in ZeroActiveDataKeyList:
            # print(self.node_ID, "のLowStorageでデータを削除します")
            value = self.LowFreqStorage.get_value(k)
            self.LowFreqStorage.delete_value(k)
            self.publish_to_ZeroFreqStorage(k, value)

    def updateBurden(self):
        if len(self.DataTraffics) >= 100: self.DataTraffics.pop(0)
        self.DataTraffics.append(self.currentDataTraffic)
        # -------------合ってる？？？？？
        self.burden = (statistics.mean(self.DataTraffics))/self.ReponseAbility
        # -------------
        self.currentDataTraffic = 0

        

    def resetAccessedBlocks(self):
        self.AccessedBlocks = []

    def updateHeaderIndex(self, key):
        value = self.HeaderStorage.get_value(key)
                
        header = value["header"]
        geneTime = value["geneTime"]
        height = value["height"]
        
        self.HeaderStorage.set_value(key,{"header" : header, "height" : height, "geneTime" : geneTime, "LastUsedTime" : self.current_time})

    def updateTxhashIndex(self, key):
        value = self.TxhashStorage.get_value(key)
                
        geneTime = value["geneTime"]
        height = value["height"]

        self.TxhashStorage.set_value(key, {"height" : height, "geneTime" : geneTime, "LastUsedTime" : self.current_time})
