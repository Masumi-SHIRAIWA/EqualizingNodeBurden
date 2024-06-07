# テキストファイルまたは、CSSファイルに出力した結果を読み込み平均や標準偏差を計算したグラフを作成するファイル

import matplotlib.pyplot as plt
import statistics
# from node import node
import csv
import os
import pandas as pd

path_root = "C:/Users/masu3/RCL-Research2023/"

fig_color = ["lightcoral", "dodgerblue", "limegreen", "orange", "violet"]
line_style = ["-", "--", "-.", ":"]

# CSVファイルの読み込みを行う
def open_file(filepath):
    # ディレクトリのパスを取得
    directory = os.path.dirname(filepath)
    
    # ディレクトリが存在しない場合、ディレクトリを作成
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    # ファイルを開く（存在しない場合は新しいファイルが作成される）
    return open(filepath)

#グラフスタイルの変更
def change_graph_style():
    plt.rcParams['font.family'] = 'Times New Roman' # font familyの設定
    plt.rcParams["font.size"] = 15 # 全体のフォントサイズの変更。
    plt.rcParams['xtick.direction'] = 'in' #x軸の目盛りの向き
    plt.rcParams['ytick.direction'] = 'in' #y軸の目盛りの向き
    plt.rcParams["xtick.minor.visible"] = True  #x軸補助目盛りの追加
    plt.rcParams["ytick.minor.visible"] = True  #y軸補助目盛りの追加
    plt.rcParams['xtick.top'] = True  #x軸の上部目盛り
    plt.rcParams['ytick.right'] = True  #y軸の右部目盛り

    #凡例設定
    plt.rcParams["legend.fancybox"] = False  # 丸角OFF
    plt.rcParams["legend.framealpha"] = 1  # 透明度の指定、0で塗りつぶしなし
    plt.rcParams["legend.edgecolor"] = 'black'  # edgeの色を変更
    plt.rcParams["legend.markerscale"] = 5 #markerサイズの倍率

# ストレージの時間変化
def TimeVariation_StorageCost(num_layer, run_time, genInterval, access_pattern, MethodName):
    GraphPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/graph/TimeVariation_StorageCost'
    ExcelPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TimeVariation_StorageCost.xlsx'
    
    if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

    StorageCost = pd.DataFrame()

    excel_file = pd.ExcelFile(ExcelPath)
    sheet_names = excel_file.sheet_names
    
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name, header=None, index_col=None)
        StorageCost = StorageCost.add(df, fill_value=0)

    StorageCost = StorageCost.div(len(sheet_names))

    change_graph_style()

    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    for i in range(num_layer):
        ax.plot(StorageCost.iloc[i], color = fig_color[i], ls = line_style[i], label = "layer" + str(i))
        
    # ax.set_title("Average Storage Cost in each layer over time")
    ax.set_xlabel("Time $\it{t}$ [s]")
    ax.set_ylabel("Storage cost")
    ax.legend()

    ax.set_xticks([ i for i in range(int(run_time / genInterval)) if i % 100 == 0])
    ax.set_xticklabels([i * 10 for i in range(int(run_time / genInterval)) if i % 100 == 0])

    fig.savefig(GraphPath + "/StorageTimeVariation_StorageCost.jpg")
    
    plt.close(fig)

# リモートクエリ率の時間変化
def TimeVariation_RemoteQueryRate(num_layer, run_time, genInterval, access_pattern, MethodName):
    GraphPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/graph/TimeVariation_RemoteQueryRate'
    ExcelPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TimeVariation_RemoteQueryRate.xlsx'

    
    if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

    RemoteQueryRate = pd.DataFrame()

    excel_file = pd.ExcelFile(ExcelPath)
    sheet_names = excel_file.sheet_names
    
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name, header=None,index_col=None) # hedaer=None, Index_col=None とすることで,header&indexが0からの連番が自動で選ばれる
        RemoteQueryRate = RemoteQueryRate.add(df, fill_value=0)
    RemoteQueryRate = RemoteQueryRate.div(len(sheet_names))

    change_graph_style()

    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)

    for i in range(num_layer):
        ax.plot(RemoteQueryRate.iloc[i], color = fig_color[i], ls = line_style[i], label = "layer" + str(i))

    # ax.set_title("Remote Query Rate over time")
    ax.set_xlabel("Time $\it{t}$ [s]")
    ax.set_ylabel("Remote query rate [%]")
    ax.legend()

    ax.set_xticks([ i for i in range(int(run_time / genInterval)) if i % 100 == 0])
    ax.set_xticklabels([i * 10 for i in range(int(run_time / genInterval)) if i % 100 == 0])

    ax.set_ylim(0,100)

    fig.savefig(GraphPath + "/TimeVariation_RemoteQueryRate.jpg")
    plt.close(fig)

# ノード負担の標準偏差の時間変化
def TimeVariation_StdevNodeBurden(run_time, genInterval, access_pattern, MethodName):
    GraphPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/graph/TimeVariation_StdevNodeBurden'
    ExcelPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TimeVariation_StdevNodeBurden.xlsx'

    if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

    StdevNodeBurden = pd.DataFrame()

    excel_file = pd.ExcelFile(ExcelPath)
    sheet_names = excel_file.sheet_names
    
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name, header=None, index_col=None)
        StdevNodeBurden = StdevNodeBurden.add(df, fill_value=0) # n 列 × 1 行 で出力される

    StdevNodeBurden = StdevNodeBurden.div(len(sheet_names))

    change_graph_style()

    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(StdevNodeBurden, color = fig_color[0])

    # ax.set_title("Stdev of Node Load over time")
    ax.set_xlabel("Time $\it{t}$ [s]")
    ax.set_ylabel("Standard deviation of node load")

    ax.set_xticks([ i for i in range(int(run_time / genInterval)) if i % 100 == 0])
    ax.set_xticklabels([i * 10 for i in range(int(run_time / genInterval)) if i % 100 == 0])

    ax.set_ylim(0,0.3)


    fig.savefig(GraphPath + "/TimeVariation_StdevNodeBurden.jpg")
    plt.close(fig)

# 総ノード負担のノード間の比較
def TotalNodeBurden(num_layer, num_node, access_pattern, MethodName):
    GraphPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/graph/TotalNodeBurden'
    ExcelPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TotalNodeBurden.xlsx'

    if not os.path.exists(GraphPath):
        os.makedirs(GraphPath)

    TotalNodeBurden = pd.DataFrame()

    excel_file = pd.ExcelFile(ExcelPath)
    sheet_names = excel_file.sheet_names
    
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name, header=None)
        TotalNodeBurden = TotalNodeBurden.add(df, fill_value=0)

    TotalNodeBurden = TotalNodeBurden.div(len(sheet_names))

    Avg_TotalNodeBurdenPerLayer = []
    total = 0
    for i in range(num_layer):
        Avg_TotalNodeBurdenPerLayer.append(TotalNodeBurden[total : total + num_node[i]].mean())
        total += num_node[i]


    change_graph_style()

    fig = plt.figure(dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    total = 0

    for i in range(num_layer):
        for j in range(num_node[i]): ax.plot(j + total, TotalNodeBurden[j + total:j + total + 1], '.', color = fig_color[i])
        ax.hlines(Avg_TotalNodeBurdenPerLayer[i], total - 0.25 , total + num_node[i] - 0.75 , colors=fig_color[i], linewidth = 3, label = "avg of layer" + str(i))
        total += num_node[i]

    # ax.set_title("Total Node Burden of Each Nodes and Avg of Total Node Burden in Each Layer")
    ax.set_xlabel("layer - node")
    ax.set_ylabel("Total Node Burden")
    ax.legend(bbox_to_anchor=(1, 1), loc='upper right', borderaxespad=0.5, fontsize=10).get_frame().set_alpha(0.6)
    fig.savefig(GraphPath + "/TotalNodeBurden.jpg")
    plt.close(fig)