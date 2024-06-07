import hashlib
import threading
import math
from . import index
from .  import routing_table
import time
import random


class Kademlia_node():
    ID_space = 50
    alpha = None
    beta = None

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.node_ID = Kademlia_node.hash(str(ip) + str(port))
        # self.node_ID = Kademlia_node.hash(random.random())
        self.table = routing_table.routing_table(self)

        self.LowFreqStorage = index.index() #LowFreqStorage
        self.ZeroFreqStorage = index.index() #ZeroFreqStorage
        
        # for Burden
        self.currentDataTraffic = 0
        self.DataTraffics = [] # the unit is MByte (Because in bitcoin blocksize is 1MB)

        self.burden = 0 #current node burden
        self.totalNodeBurden = 0
        self.avgNodeBurden = 0

        self.table.add_to_table(self, 0)

    @staticmethod
    def hash(obj):
        hash =  hashlib.sha1()
        hash.update(str(obj).encode())
        hash_value = hash.digest()
        hash_value = int.from_bytes(hash_value, "big") & ((1 << Kademlia_node.ID_space) - 1) #ID_Spaceになるよう調整
        return hash_value
    
    def xor(self, a, b):
        return a ^ b

    # def lookup(self, objective_ID):
    #     node_list = self.table.return_node_list(objective_ID)
    #     return node_list

    def join(self, other_node):
        self.table.add_to_table(other_node, other_node.burden)

    def find_node(self, objective_ID): #最も近いK個のノードListを自分のテーブルから返す
        node_list = self.table.get_node_list(objective_ID)
        return node_list

    def lookup_value(self, key):
        objective_ID = self.hash(key)
        node_list = self.find_node(objective_ID)[:self.beta]
        
        # node_list = [[n, n.burden] for n in node_list] # 常に最新の負担を知っている手法
        node_list = [[n, self.table.get_burden_of(n.node_ID)] for n in node_list] # 通信時にのみ負担を更新する手法
        
        node_list.sort(key=lambda a: a[1]) # Lookup時にも負担を考慮する手法

        resLayer = None        
        for n in node_list:
            value, new_burden = n[0].find_value(key, self, self.burden)
            if value != None: 
                resLayer = n[0].layer
                self.table.update_burden_table(n[0].node_ID, new_burden)
                break
        if value is None: print("データ", objective_ID, "は見つかりませんでした")
        return value, resLayer

    def find_value(self, key): #自分が持っていたらValueを返す，持っていなかったら目的データに近いNodeListを返す
        try:
            return self.LowFreqStorage.get_value(key)
        except KeyError:
            try:
                return self.ZeroFreqStorage.get_value(key)
            except KeyError:
                return None

    def publish_to_LowFreqStorage(self, key, value):
        stored_list = []
        not_stored_list = []

        objective_ID = self.hash(key)
        node_list = self.find_node(objective_ID)[:self.beta]

        # 最新のノード負担が小さいノードに保存を依頼する
        for n in node_list:
            isStored, current_burden = n.checkDataAndCurrentBurden(key)
            self.table.update_burden_table(n.node_ID, current_burden)
            if isStored:
                stored_list.append(n)
            else:
                not_stored_list.append([n,current_burden])
            if len(stored_list) >= self.alpha: break

        if len(stored_list) < self.alpha:
            not_stored_list.sort(key=lambda a: a[1]) # sorting by node burden. if omment out, same with just Kademlia
            for _ in not_stored_list:
                n = _[0]
                isStored, new_burden= n.store_to_LowFreqStorage(key, value, self, self.burden)
                if isStored:
                    stored_list.append(n)
                if len(stored_list) >= self.alpha: break




    def publish_to_ZeroFreqStorage(self, key, value):
        stored_list = []

        objective_ID = self.hash(key)
        node_list = self.find_node(objective_ID)

        i = 0
        while len(stored_list) < self.alpha and len(node_list) > 0:
            n = node_list.pop(0)
            isStored, new_burden = n.store_to_ZeroFreqStorage(key, value, self, self.burden)
            self.table.update_burden_table(n.node_ID, new_burden)
            if isStored:
                stored_list.append(n)
            

    def checkDataAndCurrentBurden(self, key):
        #　変更 nodeクラスでオーバーライド
        try:
            self.LowFreqStorage.get_value(key)
            return True
        except KeyError:
            try: 
                self.ZeroFreqStorage.get_value(key)
                return True
            except KeyError:
                return False


    def store_to_LowFreqStorage(self, key, value):
        try:
            self.LowFreqStorage.set_value(key, value)
            return True
        except:
            return False
        
    def store_to_ZeroFreqStorage(self, key, value):
        try:
            self.ZeroFreqStorage.set_value(key, value)
            return True
        except:
            return False
    
    