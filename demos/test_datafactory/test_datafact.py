from ctypes import POINTER
import datetime
import os
from wtpy.WtCoreDefs import WTSBarStruct
from wtpy.apps.datahelper import DHFactory as DHF
from wtpy.apps.datahelper.db import MysqlHelper

asset = ['SSE.600001']

# hlper = DHF.createHelper("baostock")
# hlper.auth()

# tushare
hlper = DHF.createHelper("tushare")
hlper.auth(**{"token":'20231208200557-eb280087-82b0-4ac9-8638-4f96f8f4d14c', "use_pro":True})

# rqdata
# hlper = DHF.createHelper("rqdata")
# hlper.auth(**{"username":"00000000", "password":"0000000"})

# 落地股票列表
hlper.dmpCodeListToFile("stocks.json")

# 下载K线数据
# hlper.dmpBarsToFile(folder='./', codes=asset, period='min1')
# hlper.dmpBarsToFile(folder='./', codes=asset, period='min5')
hlper.dmpBarsToFile(folder='./', codes=asset, period='day')

# 下载复权因子
hlper.dmpAdjFactorsToFile(codes=asset, filename="./adjfactors.json")

# 初始化数据库
dbHelper = MysqlHelper.MysqlHelper("localhost","root","bj721006","market", 3306)
dbHelper.initDB()

# 将数据下载到数据库
hlper.dmpBarsToDB(dbHelper, codes=asset, period="day")
hlper.dmpAdjFactorsToDB(dbHelper, codes=asset)

# 将数据直接落地成dsb
def on_bars_block(exchg:str, stdCode:str, firstBar:POINTER(WTSBarStruct), count:int, period:str):
    print(exchg, stdCode, firstBar, count, period)
    from wtpy.wrapper import WtDataHelper
    dtHelper = WtDataHelper()
    if stdCode[-4:] == '.HOT':
        stdCode = stdCode[:-4] + "_HOT"
    else:
        ay = stdCode.split(".")
        if exchg == 'CZCE':
            stdCode = ay[1] + ay[2][1:]
        else:
            stdCode = ay[1] + ay[2]

    filename = f"../storage/his/{period}/{exchg}/"
    if not os.path.exists(filename):
        os.makedirs(filename)
    filename += f"{stdCode}.dsb"
    if period == "day":
        period = "d"
    elif period == "min1":
        period = "m1"
    else:
        period = "m5"
    dtHelper.store_bars(filename, firstBar, count, period)
    pass

hlper.dmpBars(codes=asset, cb=on_bars_block, start_date=datetime.datetime(2000,12,1), end_date=datetime.datetime.now(), period="day")
