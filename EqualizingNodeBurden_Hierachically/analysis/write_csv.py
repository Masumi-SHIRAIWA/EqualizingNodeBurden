import statistics
import csv
import os
import pandas as pd
import numpy as np
from openpyxl import load_workbook
# 実験ごとにシートを分ける
# 必要に応じて平均を取る

path_root = "C:/Users/masu3/RCL-Research2023/"

def open_or_create_CSV(filepath, mode):
    # ディレクトリのパスを取得
    directory = os.path.dirname(filepath)
    
    # ディレクトリが存在しない場合、ディレクトリを作成
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # ファイルを開く（存在しない場合は新しいファイルが作成される）
    return open(filepath, mode, newline='')

def open_or_create_Excel(filepath):
    # ディレクトリのパスを取得
    directory = os.path.dirname(filepath)

    try:
        return pd.ExcelWriter(filepath, engine='openpyxl', mode='a')
    except FileNotFoundError:
        try:
            os.makedirs(directory)
        except FileExistsError:
            pass
        return pd.ExcelWriter(filepath, engine='openpyxl')

def NodesStorageContents(num_layer, num_node, nodes, current_time, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/NodesStorageContents.xlsx'
    data_list = [[] for i in range(sum(num_node))]
    count_num_node = 0
    for layre in range(num_layer):
        for n in nodes[layre]:
            high_list = []
            for key in n.HighFreqStorage.keys():
                try:
                    h = n.HeaderStorage.get_value(key)["height"]
                    high_list.append("Block["+str(h)+"]")
                except KeyError:
                    h = n.TxhashStorage.get_value(key)["height"]
                    high_list.append("Tx["+str(h)+"]")

            low_list = []
            for key in n.LowFreqStorage.keys():
                try:
                    h = n.HeaderStorage.get_value(key)["height"]
                    low_list.append("Block["+str(h)+"]")
                except KeyError:
                    h = n.TxhashStorage.get_value(key)["height"]
                    low_list.append("Tx["+str(h)+"]")

            zero_list = []
            for key in n.ZeroFreqStorage.keys():
                try:
                    h = n.HeaderStorage.get_value(key)["height"]
                    zero_list.append("Block["+str(h)+"]")
                except KeyError:
                    h = n.TxhashStorage.get_value(key)["height"]
                    zero_list.append("Tx["+str(h)+"]")


            data_list[count_num_node].append([n.layer, n.node_ID])
            data_list[count_num_node].append(sorted(high_list))
            data_list[count_num_node].append(sorted(low_list))
            data_list[count_num_node].append(sorted(zero_list))
            data_list[count_num_node].append(sorted(n.AccessedBlocks))
            count_num_node += 1
            # data_list = [[layer-nodeID], [high], [low], [zero]]

    # DataFrameに変換
    df  = pd.DataFrame(data_list[:], columns=["layer - nodeID", "high", "low", "zero", "Blocks accessed for last 10s"])

    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        df.to_excel(writer, sheet_name="time" + str(current_time), index=False)

def delNodesStorageContents(access_pattern, MethodName):
    # delete NodesStorageContents file, before create new one.
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName +  '/analysis/' + access_pattern + '/table/NodesStorageContents.xlsx'
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

def QueryFromTo(num_layer, query_from_to, access_pattern, MethodName):
    temp_query_from_to = query_from_to[:]
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/QueryFromTo.xlsx'
    df = []
    index_name = []
    for i in range(num_layer):
        for j in range(num_layer):
            index_name.append(str(i) + "->" + str(j))
        temp_query_from_to[i] = np.array(temp_query_from_to[i])
        temp_query_from_to[i] = temp_query_from_to[i].reshape(len(temp_query_from_to[i]),1)
        df.append(pd.DataFrame(temp_query_from_to[i], index=index_name))
        index_name = []
    with open_or_create_Excel(filepath) as writer:
        for i in range(num_layer):
            df[i].to_excel(writer, sheet_name = "fromLayer_" + str(i))

def delQueryFromTo(access_pattern, MethodName):
    # delete QueryFromTo file, before create new one.
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/QueryFromTo.xlsx'
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

def StorageQueryBalance(Threshold, StorageCostList, QueryCostList, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/StorageQueryBalance.xlsx'
    existing_data = []
    for layer in range(len(Threshold)):
        sheet_name = "Layer" + str(layer)
        try:
            existing_data.append(pd.read_excel(filepath, sheet_name=sheet_name, engine='openpyxl', header=None))
        except Exception as e:
            print(e)
            existing_data.append(pd.DataFrame())
 
    delStorageQueryBalance(access_pattern)

    with open_or_create_Excel(filepath) as writer:
        for layer in range(len(Threshold)):
            sheet_name = "Layer" + str(layer)
            df = pd.DataFrame([[Threshold[layer], str(StorageCostList[layer]) + "(" + str(format(StorageCostList[layer]/StorageCostList[0]*100, '.2f')) + "%)", format(QueryCostList[layer], '.2f')]])
            df = pd.concat([existing_data[layer], df], ignore_index=True)
            df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)

def delStorageQueryBalance(access_pattern, MethodName): # => バッチファイルで実行
    # delete StorageQueryBalance file. usinf in bach file
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/StorageQueryBalance.xlsx'
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

def delExcelFile(access_pattern, MethodName):
    delNodesStorageContents(access_pattern, MethodName)
    delQueryFromTo(access_pattern, MethodName)

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# New Version
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

# 10s毎にストレージコストを追加する
def setStorageCost(num_layer, nodes, avg_storage_cost):
    for layer in range(num_layer):
        # 各レイヤのノードのストレージコストを保存するリスト
        HighSizeList_forLayer = []
        LowSizeList_forLayer = []
        ZeroSizeList_forLayer = []
        TotalSizeList_forLayer = []
        for n in nodes[layer]:

            HighSizeList_forLayer.append(len(n.HighFreqStorage))
            LowSizeList_forLayer.append(len(n.LowFreqStorage))
            ZeroSizeList_forLayer.append(len(n.ZeroFreqStorage))
            
            TotalSizeList_forLayer.append(len(n.HighFreqStorage) + len(n.LowFreqStorage) + len(n.ZeroFreqStorage))
            
            # 削除予定
            for data_key in n.HighFreqStorage.keys():
                if data_key in n.LowFreqStorage.keys() or data_key in n.ZeroFreqStorage.keys():
                    raise Exception

        avg_storage_cost[layer].append(statistics.mean(TotalSizeList_forLayer))
        print("Layer", layer, "Total : ", avg_storage_cost[layer][-1], " High : ", statistics.mean(HighSizeList_forLayer), ", Low : ", statistics.mean(LowSizeList_forLayer), ", Zero : ", statistics.mean(ZeroSizeList_forLayer))
        
    return

# ストレージコストの時間変化
def TimeVariation_StorageCost(avg_storage_cost, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TimeVariation_StorageCost.xlsx'
    df = pd.DataFrame(avg_storage_cost[:], columns=None)

    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)

# 最終的なストレージコスト（データ保有率%）
def RetentionRate_StorageCost(avg_storage_cost, num_layer, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/RetentionRate_StorageCost.xlsx'
    retentio_rate = [avg_storage_cost[i][-1] / avg_storage_cost[0][-1] * 100 for i in range(num_layer)]
    
    df = pd.DataFrame(retentio_rate[:], columns=None) # 縦に表示されればいい?

    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)

# リモートクエリ率の時間変化
def TimeVariation_RemoteQueryRate(remote_query_rate, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TimeVariation_RemoteQueryRate.xlsx'
    df = pd.DataFrame(remote_query_rate[:], columns=None, index=None)

    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)

# リモートクエリ率の平均
def AVG_RemoteQueryRate(remote_query_rate, num_layer, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/AVG_RemoteQueryRate.xlsx'
    avg_remote_query_rate = [[statistics.mean(remote_query_rate[i])] for i in range(num_layer)]

    
    df = pd.DataFrame(avg_remote_query_rate[:], columns=None, index=None)

    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)

# 10s毎にノード負担の(母集団)標準偏差を追加する
def setStdevNodeBurden(num_layer, nodes, stdev_node_burden):
    burdenList = []
    for layre in range(num_layer):
        for n in nodes[layre]:
            burdenList.append(n.burden)
    stdev_node_burden.append(statistics.pstdev(burdenList))

# ノード負担の標準偏差の時間変化
def TimeVariation_StdevNodeBurden(stdev_node_burden, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TimeVariation_StdevNodeBurden.xlsx'
    df = pd.DataFrame(stdev_node_burden[:], columns=None, index=None)
    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)

# ノード負担の標準偏差の平均
def AVG_StdevNodeBurden(stdev_node_burden, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/AVG_StdevNodeBurden.xlsx'
    
    avg_stdev_node_burden = np.sqrt(sum([s**2 for s in stdev_node_burden])/len(stdev_node_burden))
    
    df = pd.Series(avg_stdev_node_burden,index=None)
        
    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)

def TotalNodeBurden(num_layer, nodes, access_pattern, MethodName):
    filepath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TotalNodeBurden.xlsx'
    TotalNodeBurden = []
    for layer in range(num_layer):
        for n in nodes[layer]:
            TotalNodeBurden.append(n.totalNodeBurden)
        
    df = pd.DataFrame(TotalNodeBurden[:], columns=None)

    # ExcelWriterオブジェクトを作成
    with open_or_create_Excel(filepath) as writer:
        num = len(writer.sheets)
        df.to_excel(writer, sheet_name="Experiment" + str(num), index=False, header=False)
