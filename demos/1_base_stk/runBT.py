from wtpy import WtBtEngine,EngineType
from wtpy.apps import WtBtAnalyst

from wtpy.monitor import WtBtSnooper
from wtpy import WtDtServo
def testBtSnooper():    

    dtServo = WtDtServo()
    # 这里配置的是基础数据文件目录
    dtServo.setBasefiles(folder='../common/')

    # 这里配置的是datakit落地的数据目录
    dtServo.setStorage(path='../storage/')

    snooper = WtBtSnooper(dtServo)
    snooper.run_as_server(port=8081, host='localhost')

import sys
sys.path.append('../Strategies')
from DualThrust import StraDualThrust

name = "dt_cta"
codes = 'SSE.STK.688001'
period = "m5"

if __name__ == "__main__":
    #创建一个运行环境，并加入策略
    engine = WtBtEngine(EngineType.ET_CTA)
    engine.init(folder='../common/', cfgfile="configbt.yaml")
    #engine.configBacktest(201901010930,201912151500)
    #engine.configBTStorage(mode="csv", path="../storage/")
    engine.commitBTConfig()
    
    straInfo = StraDualThrust(name=name, code=codes, barCnt=50, period=period, days=5000, k1=0.1, k2=0.1)
    engine.set_cta_strategy(straInfo, slippage=0, isRatioSlp=False, incremental=False)
    engine.run_backtest(bAsync=False)

    #绩效分析
    analyst = WtBtAnalyst()
    analyst.add_strategy(name, folder="./outputs_bt/", init_capital=500000, rf=0.03, annual_trading_days=240)
    analyst.run_flat()

    # testBtSnooper()
    # 运行了服务以后，在浏览器打开以下网址即可使用
    # http://127.0.0.1:8081/backtest/backtest.html

    kw = input('press any key to exit\n')
    engine.release_backtest()