import pandas as pd
import openpyxl
import os
import numpy as np

path_root = "C:/Users/masu3/RCL-Research2023/"

def parse_excel(filename):
    wb = openpyxl.load_workbook(filename)
    sheets = {}
    for sheet in wb.worksheets:
        data = []
        for row in sheet.iter_rows():
            data.append([cell.value for cell in row])
        sheets[sheet.title] = data
    return sheets

def NodesStorageContents(access_pattern, MethodName):
    def sheets_to_html(sheets):
        html = ["<div>"]

        html.append(f'<h2>{MethodName} : {access_pattern}</h2>')

        # 矢印ボタンを追加
        html.append('<button onclick="switchSheet(-1)">&#8592; Previous</button>')
        html.append('<button onclick="switchSheet(1)">Next &#8594;</button>')

        for idx, (sheet_name, sheet_data) in enumerate(sheets.items()):
            display_style = "none" if idx > 0 else ""
            html.append(f'<h4 id="time_{idx}" style="display:{display_style};">{sheet_name}</h4>')
            html.append(f'<table id="sheet_{idx}" border="1" style="display:{display_style}; border-collapse: collapse" >')
            for row in sheet_data:
                html.append("<tr>")
                for cell in row:
                    html.append(f"<td>{cell}</td>")
                html.append("</tr>")
            html.append("</table>")

        html.append("""
        <script>
            let currentSheetIndex = 0;
            const sheetCount = %d;

            function switchSheet(delta) {
                document.getElementById("sheet_" + currentSheetIndex).style.display = 'none';
                document.getElementById("time_" + currentSheetIndex).style.display = 'none';
                currentSheetIndex += delta;

                if (currentSheetIndex == -1) currentSheetIndex = sheetCount - 1;
                if (currentSheetIndex >= sheetCount) currentSheetIndex = 0;

                document.getElementById("sheet_" + currentSheetIndex).style.display = '';
                document.getElementById("time_" + currentSheetIndex).style.display = '';
            }
        </script>
        """ % len(sheets))

        html.append("</div>")
        return '\n'.join(html)

    sheets = parse_excel(path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/NodesStorageContents.xlsx')
    html_content = sheets_to_html(sheets)
    with open(path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/NodesStorageContents.html', 'w') as file:
        file.write(html_content)

def QueryFromTo(access_pattern, MethodName):
    def sheets_to_html(sheets):
        html = ["<div>"]

        html.append(f'<h2>{MethodName} : {access_pattern}</h2>')
        
        html.append(f"<div style='display: flex; flex-wrap: wrap;'>")
        for idx, (sheet_name, sheet_data) in enumerate(sheets.items()):
            # シートコンテナのスタイルを設定
            html.append(f"<div style='width: 50%; box-sizing: border-box; padding: 10px;'>")
            html.append(f'<h4>{sheet_name}</h4>')
            html.append('<table border="1">')
            for row in sheet_data:
                html.append("<tr>")
                for cell in row:
                    html.append(f"<td>{cell}</td>")
                html.append("</tr>")
            html.append("</table>")
            html.append("</div>")

            # 2つのシートが表示されたら次の行に移動
            if idx == 1:
                html.append('<div style="clear: both;"></div>')

        html.append("</div>")
        html.append("</div>")
        return '\n'.join(html)

    sheets = parse_excel(path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/QueryFromTo.xlsx')
    html_content = sheets_to_html(sheets)
    with open(path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/QueryFromTo.html', 'w') as file:
        file.write(html_content)

def StorageQueryBalance(access_pattern, MethodName):
    def sheets_to_html(sheets):
        html = ["<div>"]

        html.append(f'<h2>{MethodName} : {access_pattern}</h2>')
        
        html.append(f"<div style='display: flex; flex-wrap: wrap;'>")
        for idx, (sheet_name, sheet_data) in enumerate(sheets.items()):
            # シートコンテナのスタイルを設定
            html.append(f"<div style=' box-sizing: border-box; padding: 10px;'>")
            html.append(f'<h4>{sheet_name}</h4>')
            html.append('<table border="1"  style="font-size: 10pt;">')
            html.append(f'<thead><tr><th>Threshold Time 1(s)</th><th>Storage Cost(#Tx + #Bbody)</th><th>Remote Query Rate(%)</th></tr></thead>')
            for row in sheet_data:
                html.append("<tr>")
                for cell in row:
                    html.append(f"<td>{cell}</td>")
                html.append("</tr>")
            html.append("</table>")
            html.append("</div>")

        html.append("</div>")
        return '\n'.join(html)

    sheets = parse_excel(path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/StorageQueryBalance.xlsx')
    html_content = sheets_to_html(sheets)
    with open(path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table/StorageQueryBalance.html', 'w') as file:
        file.write(html_content)



# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
# New Version
# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------

# 総ノード負担の平均と標準偏差
def AnalysisNodeBurden(num_layer, num_node, access_pattern, MethodName):


    TablePath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/table'
    ExcelPath = path_root + 'EqualizingNodeBurden/' + MethodName + '/analysis/' + access_pattern + '/csv/TotalNodeBurden.xlsx'

    if not os.path.exists(TablePath):
        os.makedirs(TablePath)
    
    TotalNodeBurden = pd.DataFrame()

    excel_file = pd.ExcelFile(ExcelPath)
    sheet_names = excel_file.sheet_names
    
    for sheet_name in sheet_names:
        df = excel_file.parse(sheet_name, header=None)
        TotalNodeBurden = TotalNodeBurden.add(df, fill_value=0)

    TotalNodeBurden = TotalNodeBurden.div(len(sheet_names))

    # Pandas.Seriesの形に直す
    import statistics
    Avg_TotalNodeBurden = TotalNodeBurden.mean()
    Avg_TotalNodeBurden.index = ["Average"]
    Stdev_TotalNodeBurden = TotalNodeBurden.std(ddof=0)
    Stdev_TotalNodeBurden.index= ["Stdev"]
    
    Avg_TotalNodeBurdenPerLayer = []

    total = 0
    for i in range(num_layer):
        Avg_TotalNodeBurdenPerLayer.append(float(TotalNodeBurden[total : total + num_node[i]].mean().values[0]))
        total += num_node[i]
    
    # Pandas.Seriesの形に直す
    Avg_TotalNodeBurdenPerLayer = pd.Series(Avg_TotalNodeBurdenPerLayer, index=["Average(Layer"+str(i)+")" for i in range(len(Avg_TotalNodeBurdenPerLayer))])
    
    # Seriesを連結し、HEML化
    Table = pd.concat([Avg_TotalNodeBurden, Stdev_TotalNodeBurden, Avg_TotalNodeBurdenPerLayer])
    html_content = Table.to_frame().T.to_html(index=False)
    with open(TablePath + '/AnalysisNodeBurden.html', 'w') as file:
        file.write(f'<h2>{MethodName} - {access_pattern}</h2\n>' + html_content)