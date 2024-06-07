#import
import node
import blockchain
from transactionchain import transactionchain
from transaction import transaction
from access_pattern import access_pattern
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from Kademlia_MLCU.Kademlia_node import Kademlia_node
import statistics
from analysis import create_graph, write_csv, create_table
import sys
import configparser

def print_nodes_burden():
    burden_list = []
    for i in range(num_layer):
        for n in nodes[i]:
            burden_list.append([n, round(n.burden, 10)])
    str_list = []
    i = 0
    str_temp = " "
    while len(burden_list) > 0:
        i += 1
        str_temp += str(burden_list.pop(0))
        if i % 3 == 0:
                str_list.append(str_temp)
                str_temp = " "
    
    str_temp = ""
    for _ in range(len(str_list[0])):
        str_temp += "-"
    str_list.insert(0,str_temp)
    str_list.append(str_temp)
    for s in str_list:
        print(s)

MethodName = "KademliaXOR"

args = sys.argv[:] # args[1~4] : Timethre1
print(args)
args.pop(0) # Delete Filename

# 設定値
ConfigFile = configparser.ConfigParser()
ConfigFile.read("C:/Users/masu3/RCL-Research2023/EqualizingNodeBurden/config.ini", encoding='utf-8')
run_time = int(ConfigFile['SIMULATOR']['RUN_TIME'])

if len(args) == 0:
    access_pattern.pattern = ConfigFile['SIMULATOR']['ACCESS_PATTERN']
else:
    ACCESS_PATTERN = args[0]
    if ACCESS_PATTERN == "UNIFORM" or ACCESS_PATTERN == "EXPONENTIAL_DECAYING":
        access_pattern.pattern = args.pop(0)
    else:
        print("指定したACCESS_PATTERNが間違っているか,閾値時間のみ指定してしまっています")
        access_pattern.pattern = ConfigFile['SIMULATOR']['ACCESS_PATTERN']

access_pattern.num = int(ConfigFile['SIMULATOR']['ACCESS_NUM'])




genInterval = int(ConfigFile['SIMULATOR']['GEN_INTERVAL']) #生成間隔(s)
accessInterval = int(ConfigFile['SIMULATOR']['ACC_INTERVAL']) # アクセス発生間隔
num_block = run_time / genInterval

num_layer = int(ConfigFile['SIMULATOR']['NUM_LAYER'])
num_node = eval(ConfigFile['SIMULATOR']['NUM_NODE'])
resAbility = eval(ConfigFile['SIMULATOR']['RES_ABILITY'])

Kademlia_node.alpha = int(ConfigFile['SIMULATOR']['ALPHA'])
Kademlia_node.beta = int(ConfigFile['SIMULATOR']['BETA'])


if len(args) == 0:
    TimeThre1 = eval(ConfigFile['SIMULATOR']['TIME_THRESHOLD_1'])
elif len(args) == num_layer:
    TimeThre1 = [int(args[0]),int(args[1]),int(args[2]),int(args[3])]
else:
    raise Exception("引数 TimeThreshold の数がConfigファイルの レイヤ数 と一致しません")

TimeThre2 = int(ConfigFile['SIMULATOR']['TIME_THRESHOLD_2'])

print("METHOD", MethodName)
print("ACCEAAPATERN", access_pattern.pattern)
print("TT1", TimeThre1)


# 評価グラフ用
remote_query_rate = [[0] for i in range(num_layer)]
remote_query_rate_temp = [[] for i in range(num_layer)]
avg_storage_cost = [[1] for i in range(num_layer)]
stdev_node_burden = [0]
query_from_to = [[0 for j in range(num_layer)] for i in range(num_layer)]
NodesStorageContentsInterval = 100

write_csv.delExcelFile(access_pattern.pattern, MethodName)


#ノードの初期化
nodes = [[] for l in range(num_layer)]
for i in range(num_layer):
    print("------------layer", i , "------------")
    for j in range(num_node[i]):
        nodes[i].append(node.node("122.2.206.139", str(i) + str(j), i, resAbility[i], TimeThre1[i], TimeThre2, num_layer))
        print(nodes[i][j].node_ID, ",")

# 経路表を確立 変更する.　全ノード情報を持つ。
for i in range(num_layer):
    for n1 in nodes[i]:
        for j in range(num_layer):
            for n2 in nodes[j]:
                n1.table.add_to_table(n2, 0)

#BlockChainの初期化
bc = blockchain.blockchain()
pendingTxs = []

t = 0
newBlock = bc.createGeneBlock(t)
print("Now is ", t, "s")
for j in range(num_layer):
    for n in nodes[j]:
        n.saveNewBlock(newBlock)


# Generate Roop
while t < run_time :
    t += 1
    node.node.current_time = t

    newTx = transactionchain.createTransaction()
    pendingTxs.append(newTx)
    for i in range(num_layer):
        for n in nodes[i]:
            n.saveNewTx(newTx)

    if t % genInterval == 0:
        newBlock = bc.createBlock(t, pendingTxs)
        pendingTxs = []
        print("Now is ", t, "s")
        for j in range(num_layer):
            for n in nodes[j]:
                n.saveNewBlock(newBlock)

        # ストレージの時間変化（avg_storage_cost）を更新
        write_csv.setStorageCost(num_layer, nodes, avg_storage_cost)
        write_csv.setStdevNodeBurden(num_layer, nodes, stdev_node_burden)

        # Output node burden
        # print_nodes_burden()

        

    # Access part
    for layer in range(num_layer):
        remote_query_rate_temp[layer].append(access_pattern().Access(nodes[layer])) # 時間毎のリモートクエリ発生率を返す

    if t % genInterval == 0:
        for layer in range(num_layer):
            remote_query_rate[layer].append(statistics.mean(remote_query_rate_temp[layer]))
        remote_query_rate_temp = [[] for _ in range(num_layer)]

    
        

    # delete part
    for layer in range(num_layer):
        for n in nodes[layer]:
            n.deleteAndPublishInactiveData()

    # create NodesStorageContents Excel sheet.
    if t % NodesStorageContentsInterval == 0:
        write_csv.NodesStorageContents(num_layer, num_node, nodes, t, access_pattern.pattern, MethodName)
        for i in range(num_layer):
            for n in nodes[i]:
                n.resetAccessedBlocks()

    # Update node burden part
    for i in range(num_layer):
        for n in nodes[i]:
            n.updateBurden()


# Generate Roop END


# -------------------------生成終了-------------------------

# calculate nodeBurden
for i in range(num_layer):
    for n in nodes[i]:
        n.totalNodeBurden /= resAbility[i]
        n.avgNodeBurden = n.totalNodeBurden / run_time
    
for i in range(num_layer):
    for n in nodes[i]:
        for j in range(num_layer):
            query_from_to[i][j] += n.numOfResponsedFrom[j] # the number of query which is rsponsed from j to i.




# 評価グラフ・表の作成

# # 各層での平均ストレージ容量の10秒ごとの時間変化
write_csv.TimeVariation_StorageCost(avg_storage_cost, access_pattern.pattern, MethodName)
create_graph.TimeVariation_StorageCost(num_layer, run_time, genInterval, access_pattern.pattern, MethodName)
write_csv.RetentionRate_StorageCost(avg_storage_cost, num_layer, access_pattern.pattern, MethodName)

# # リモートクエリ率の時間変化
write_csv.TimeVariation_RemoteQueryRate(remote_query_rate, access_pattern.pattern, MethodName)
create_graph.TimeVariation_RemoteQueryRate(num_layer, run_time, genInterval, access_pattern.pattern, MethodName)
write_csv.AVG_RemoteQueryRate(remote_query_rate, num_layer, access_pattern.pattern, MethodName)

# # 各ノードの負担
write_csv.TimeVariation_StdevNodeBurden(stdev_node_burden, access_pattern.pattern, MethodName)
create_graph.TimeVariation_StdevNodeBurden(run_time, genInterval, access_pattern.pattern, MethodName)
write_csv.TotalNodeBurden(num_layer, nodes, access_pattern.pattern, MethodName)
create_graph.TotalNodeBurden(num_layer, num_node, access_pattern.pattern, MethodName)
create_table.AnalysisNodeBurden(num_layer, num_node, access_pattern.pattern, MethodName)
write_csv.AVG_StdevNodeBurden(stdev_node_burden, num_layer, access_pattern.pattern, MethodName)


# # create QueryFromTo Table
# write_csv.QueryFromTo(num_layer, query_from_to, access_pattern.pattern, MethodName)
# create_table.QueryFromTo(access_pattern.pattern, MethodName)

# create_table.NodesStorageContents(access_pattern.pattern, MethodName)

# update StorageQueryBalance Excel file
# write_csv.StorageQueryBalance(TimeThre1, [avg_storage_cost[i][-1] for i in range(len(avg_storage_cost))], [statistics.mean(remote_query_rate[l]) for l in range(len(query_from_to))], access_pattern.pattern)
# create_table.StorageQueryBalance(access_pattern.pattern, MethodName)
