class routing_table():
    def __init__(self, owner_node):
        self.node = owner_node #このテーブルの保持ノード
        self.table = []
        self.burden_table = dict()
        self.layer_table = dict()

    def add_to_table(self, contact_node, burden): #テーブルに追加する．その前に、チェックが必要
        if contact_node not in self.table:
            self.table.append(contact_node)
            self.burden_table.__setitem__(contact_node.node_ID, burden)
            self.layer_table.__setitem__(contact_node.node_ID, contact_node.layer)
         
    def get_node_list(self, ObjectiveID): #IDに近いノードを順にして返す.
        return sorted(self.table,  key = lambda a: (a.node_ID ^ ObjectiveID))
    
    def get_burden_of(self, node_ID):
         return self.burden_table.__getitem__(node_ID)
    

    def update_burden_table(self, node_ID, burden):
            self.burden_table.__setitem__(node_ID, burden)

    def get_layer_of(self, node_ID):
         return self.layer_table.__getitem__(node_ID)
    
    def __repr__(self):
        return f'------{self.node.node_ID}------\n{self.table}'
