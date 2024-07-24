from ctypes import POINTER
import datetime
import os
import numpy as np
import pandas as pd
from wtpy.wrapper import WtDataHelper
from wtpy.WtCoreDefs import WTSBarStruct
from wtpy.apps.datahelper import DHFactory as DHF
from wtpy.apps.datahelper.db import MysqlHelper

# asset = ['SSE.STK.688001',
#          'SSE.STK.688002',
#          'SSE.STK.688003']
period = 'min5'

# baostock
hlper = DHF.createHelper("baostock")
hlper.auth()

# tushare
# hlper = DHF.createHelper('tushare')
# hlper.auth(**{'token':'20231208200557-eb280087-82b0-4ac9-8638-4f96f8f4d14c', 'use_pro':True})

# rqdata
# hlper = DHF.createHelper("rqdata")
# hlper.auth(**{"username":"00000000", "password":"0000000"})

# 落地股票列表
hlper.dmpCodeListToFile('../common/stocks.json'); print("stock list acquired")

# 下载复权因子 (only stk)
hlper.dmpAdjFactorsToFile(codes='../common/stocks.json', filename='../common/adjfactors.json'); print("adj factor list acquired")


# 下载K线数据
hlper.dmpBarsToFile(folder='../storage/csv/', codes='../common/stocks.json', period=period); print(f'{period} dumped')
# hlper.dmpBarsToFile(folder='../storage/csv/', codes=asset, period='min5'); print('min5 dumped')
# hlper.dmpBarsToFile(folder='../storage/csv/', codes=asset, period='min1'); print('min1 dumped')

# 初始化数据库
# dbHelper = MysqlHelper.MysqlHelper("localhost","chuyin","bj721006","market", 3306)
# dbHelper.initDB()

# 将数据下载到数据库
# hlper.dmpBarsToDB(dbHelper, codes=asset, period=period); print('kline saved to MySql')
# hlper.dmpAdjFactorsToDB(dbHelper, codes=asset); print('adj_factor saved to MySql')

# dtHelper = WtDataHelper()
# dtHelper.trans_csv_bars(csvFolder='../storage/csv/', binFolder='../storage/bin/', period=period)

# 将数据直接落地成dsb
def on_bars_block(exchg:str, stdCode:str, firstBar:POINTER(WTSBarStruct), count:int, period:str):
    from wtpy.wrapper import WtDataHelper
    dtHelper = WtDataHelper()
    # print(exchg, stdCode, firstBar, count, period)
    #if stdCode[-4:] == '.HOT':
    #    stdCode = stdCode[:-4] + "_HOT"
    #else:
    #    ay = stdCode.split(".")
    #    if exchg == 'CZCE':
    #        stdCode = ay[1] + ay[2][1:]
    #    else:
    #        stdCode = ay[1] + ay[2]
    filename = f"../storage/his/{period}/{exchg}/"
    if not os.path.exists(filename):
        os.makedirs(filename)
    filename += f"{stdCode}.dsb"
    print(filename,count)
    if period == "day":
        period = "d"
    elif period == "min1":
        period = "m1"
    else:
        period = "m5"
    dtHelper.store_bars(filename, firstBar, count, period)
    pass
# not in tushare
hlper.dmpBars(codes='../common/stocks.json', cb=on_bars_block, 
              #start_date=datetime.datetime(2019,1,1), 
              #end_date=datetime.datetime(2024,1,1), 
              period=period)
print('done')
