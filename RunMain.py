import logging
import time
from settings.setting import TIMESLEEP
from operation.DocxCleanMain import CleanData
from operation.ExtractData import ExtractData
import logging
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton

LoggerSingleton().init_dict_config(LOGGING_CONFIG)


class Main(object):
    def __init__(self):
        self.CleanData = CleanData()
        self.ExtractData = ExtractData()

    def run(self):
        # 先遍历文件并清洗文件
        self.CleanData.run()
        time.sleep(5)
        # 再把 清理之后的数据写入需要的格式中
        self.ExtractData.run()


if __name__ == '__main__':
    run = Main()
    while True:
        run.run()
        logging.info("休息中")
        time.sleep(TIMESLEEP)

