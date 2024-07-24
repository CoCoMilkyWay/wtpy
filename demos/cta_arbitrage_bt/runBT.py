from wtpy import WtBtEngine,EngineType
from wtpy.apps import WtBtAnalyst

import sys
sys.path.append('../Strategies')
from T1 import StraT1

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
    
if __name__ == "__main__":
    #创建一个运行环境，并加入策略
    engine = WtBtEngine(EngineType.ET_CTA)
    engine.init('../common/', "configbt.yaml")
    engine.commitBTConfig()

    straInfo = StraT1(name='t1_rb_i', code1="SHFE.rb.HOT", code2="DCE.i.HOT", bar_cnt=400, period="m5", N=360, threshold=0.9)
    engine.set_cta_strategy(straInfo)

    engine.run_backtest()

    analyst = WtBtAnalyst()
    analyst.add_strategy("t1_rb_i", folder="./outputs_bt/", init_capital=350000, rf=0.02, annual_trading_days=240)
    analyst.run_new()

    # kw = input('press any key to exit\n')
    engine.release_backtest()
    
    testBtSnooper()
    # 运行了服务以后，在浏览器打开以下网址即可使用
    # http://127.0.0.1:8081/backtest/backtest.html