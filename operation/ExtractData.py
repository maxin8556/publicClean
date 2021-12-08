import sys
import time

sys.path.append("../")
import copy
import json
import os
import re
import shutil
from settings.setting import analysis_Items, warning_Items
from settings.setting import READJSONPATH, PATHFORMAT, AFTERPATHFORMAT, ANALYSIS_RESULT, WARNING_RESULT
import logging
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton

LoggerSingleton().init_dict_config(LOGGING_CONFIG)




# 提取数据入到完整的数据格式中
class ExtractData(object):
    def __init__(self):
        if os.name == "nt":
            # 需要提取的文件 的目录
            self.readPath = r"D:\MaXin-Study\2021-10-3\DataClean\Data\BeforeCleanJson"
            self.pathFormat = r"D:\MaXin-Study\2021-10-3\DataClean\Data\BeforeCleanJson\{}"
            self.afterPathFormat = r"D:\MaXin-Study\2021-10-3\DataClean\Data\AfterCleanJson\{}"
            # 最终数据的文件夹
            # 分析
            self.analysis_result = r"D:\MaXin-Study\2021-10-3\DataClean\ResultData\analysis_result_{}.json"
            # 预警
            self.warning_result = r"D:\MaXin-Study\2021-10-3\DataClean\ResultData\warning_result_{}.json"

        else:
            self.readPath = READJSONPATH
            self.pathFormat = PATHFORMAT
            self.afterPathFormat = AFTERPATHFORMAT
            # 最终数据的文件夹
            # 分析
            self.analysis_result = ANALYSIS_RESULT
            # 预警
            self.warning_result = WARNING_RESULT


    # 舆情详细数据
    def publicOpinionDetails(self, json_data):
        # 文件名称
        # fileName = json_data['fileName']
        fileName = "预警文件:《{}》".format(json_data['fileName'])
        # 平台
        infoSource = json_data['infoSource']

        address = json_data['address']
        # 标题
        title = json_data['title']
        # 标签
        label = json_data['label']
        # 时间
        time = json_data['time']
        # 网名
        nickname = json_data['nickname']
        # 内容
        content = json_data['content']
        # 链接
        link = json_data['link']
        url = json_data['url']
        r_content = json_data['fileContent']
        fileContent = r_content.replace('\n\n', '').replace('\n原文链接', '').replace(url, '') + fileName
        details = {
            "title": title,
            "address": address,
            "content": content,
            "time": time,
            "nickname": nickname,
            "label": label,
            "platform": infoSource,
            "link": link,
            "fileContent": fileContent
        }
        return details

    def writeFile(self, results, sign):
        # 预警文件
        # 时间戳
        t = time.time()
        TIME_STAMP = int(round(t * 1000))
        warningPath = self.warning_result.format(TIME_STAMP)
        if sign == "2":
            with open(warningPath, 'w', encoding='utf8')as fl:
                json.dump(results, fl, ensure_ascii=False, sort_keys=True, indent=4)
            logging.info("添加数据到warning_result完成")
        else:
            analysisPath = self.analysis_result.format(TIME_STAMP)
            with open(analysisPath, 'w', encoding='utf8')as fl:
                json.dump(results, fl, ensure_ascii=False, sort_keys=True, indent=4)
            logging.info("添加数据到analysis_result完成")

    # 需要把写入好的json文件给移除或者移动目录
    def moveFile(self, fileName):
        # 预警文件直接提取好，直接移动到所需目录下
        if "预警" in fileName:
            logging.info("开始移动预警{} 文件".format(fileName))
            # 目标目录
            before_filePath = self.pathFormat.format(fileName)
            after_filePath = self.afterPathFormat.format(fileName)
            shutil.move(before_filePath, after_filePath)
            logging.info("移动 预警 文件成功")
        else:
            logging.info("开始移动分析文件{}到BeforeJson文件".format(fileName))
            before_filePath = self.pathFormat.format(fileName)
            after_filePath = self.afterPathFormat.format(fileName)
            shutil.move(before_filePath, after_filePath)
            logging.info("移动到分析文件AfterJson文件下成功")

    # 如果需要增加数据,需要先把原本的数据提取出来,再把新的数据添加进去,最后就可以写入了
    def getJson(self, items):
        if os.path.exists(self.analysis_result):
            with open(self.analysis_result, 'r', encoding="UTF-8") as fl:
                json_data = json.load(fl)
                detailslist = json_data['platformDetails']
                detailslist.append(items)
                return detailslist
        else:
            return items

    # 提取文件信息 写入信息
    def getInfo(self):
        try:
            # 如果该目录下有文件,说明需要清洗,如果没有 就说明文件已经清洗完毕
            file_list = os.listdir(self.readPath)
            if file_list:
                # 如果有文件需要提取
                for _ in file_list:
                    if _.endswith('.json'):
                        # 预警信息直接是提取好的，直接移动文件
                        if "预警信息" in _:
                            path = self.pathFormat.format(_)
                            # 预警文件直接写好了，先复制一份备份，再移动到目标目录
                            with open(path, 'r', encoding='utf8')as fl:
                                json_data = json.load(fl)
                            warning_Items['warningList'] = json_data
                            self.writeFile(warning_Items, sign="2")
                            # 写好之后把之前解析好的的移动
                            self.moveFile(_)
                        else:
                            path = self.pathFormat.format(_)
                            with open(path, 'r', encoding='utf8')as fl:
                                json_data = json.load(fl)
                            #  获取相对应的需要的数据
                            # 遍历 舆情详细数据 ,转化成json文件
                            details = self.publicOpinionDetails(json_data)

                            # # 先读取json文件中内容并提取,然后把新获取的数据增加进去,然后写入文件
                            # detailslist = self.getJson(details)
                            # if os.path.exists(self.analysis_result):
                            #     analysis_Items['platformDetails'] = detailslist
                            # else:
                            #     analysis_Items['platformDetails'].append(detailslist)
                            analysis_Items['platformDetails'].append(details)

                            self.writeFile(analysis_Items, sign="1")
                            # 这里清空一下列表
                            analysis_Items['platformDetails'].clear()
                            # 移动存好的json文件到新的目录下
                            self.moveFile(_)
                    else:
                        logging.info("没有可清洗文件")
            else:
                logging.info("暂时没有文件可以提取")
        except Exception as msg:
            logging.exception(logging.exception("出现异常错误{}".format(msg)))

    def run(self):
        self.getInfo()


if __name__ == '__main__':
    tmp = ExtractData()
    while True:
        tmp.run()
        time.sleep(10)
