class k_bucket(list): #contact node の入れ物
    def __init__(self, k):
        self.k = k #K-BucketのK    
    
    def append(self, n):
        if type(n) is None:
            print("Contact nodeクラスしか受け付けません")
            raise ValueError("Contact nodeクラスしか受け付けません")
        else: return super().append(n)
        # elif not self.is_full(): #Fullで無ければ、そのまま追加
        #     return super().append(n)
        # else: #Fullの場合、エラー
        #     # print("このK-Bucketにはもう入りません")
        #     return

    def is_full(self): #K-bucketがFullであればTrue
        return len(self) >= self.k
    
