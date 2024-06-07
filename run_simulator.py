import multiprocessing
import subprocess
import time
import sys
import os


def run_process(args):
    FILE_PATH = args.pop(0)
    ACCESS_PSTTERN = args.pop(0)
    TT_LIST = args.pop(0)
    subprocess.run(["py", FILE_PATH, ACCESS_PSTTERN] + TT_LIST)
    print("-----------------",FILE_PATH, ACCESS_PSTTERN,  TT_LIST,"---------------")

def main(TTList):
    start = time.time()
    ACCESS_PATTERN = ["UNIFORM","EXPONENTIAL_DECAYING"]
    argsList = []

    # 実行する組合せの選択
    # argsList.append(["./EqualizingNodeBurden/main.py", ACCESS_PATTERN[0], TTList])
    argsList.append(["./EqualizingNodeBurden/main.py", ACCESS_PATTERN[1], TTList])
    # argsList.append(["./KademliaXOR/main.py", ACCESS_PATTERN[0], TTList])
    # argsList.append(["./KademliaXOR/main.py", ACCESS_PATTERN[1], TTList])
    # argsList.append(["./EqualizingNodeBurden_Hierachically/main.py", ACCESS_PATTERN[0], TTList])
    argsList.append(["./EqualizingNodeBurden_Hierachically/main.py", ACCESS_PATTERN[1], TTList])
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(run_process, argsList)
    # pool.map_async(run_process, argsList).get(1)



    print(time.time() - start)

if __name__ == "__main__":
    args = sys.argv
    args = sys.argv[1:]
    main(args)