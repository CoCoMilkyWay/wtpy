from wtpy import WtBtEngine,EngineType
from wtpy.apps import WtBtAnalyst
from ConsoleIdxWriter import ConsoleIdxWriter

import sys
sys.path.append('../Strategies')
from StraCtaUnitTest import StraCtaUnitTest

# from Strategies.XIM import XIM

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
    engine.configBacktest(201909100930,201912011500)
    engine.configBTStorage(mode="csv", path="../storage/")
    engine.commitBTConfig()
    idxWriter = ConsoleIdxWriter()
    engine.set_writer(idxWriter)
    straInfo = StraCtaUnitTest(name='pydt_IF', code="CFFEX.IF.HOT", barCnt=50, period="m5", days=30, k1=0.1, k2=0.1, isForStk=False)
    engine.set_cta_strategy(straInfo)

    engine.run_backtest()

    analyst = WtBtAnalyst()
    analyst.add_strategy("pydt_IF", folder="./outputs_bt/", init_capital=500000, rf=0.02, annual_trading_days=240)
    analyst.run_flat()
    
    testBtSnooper()
    kw = input('press any key to exit\n')
    engine.release_backtest()
