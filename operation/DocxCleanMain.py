import sys

sys.path.append("../")

from settings.setting import TARGET_FOLDERS, FILES_FORMAT, FILES_RESULT, JSON_PATH, AFTER_DOCX, ERROR_PATH, \
    ERROR_PATH_FORMAT, ADDRESS
import datetime
import json
import os
import shutil
import time
# from win32com import client
import docx
import re
import logging
from Utils.logcfg import LOGGING_CONFIG
from Utils.Logger import LoggerSingleton
from settings.CleanRules import *

LoggerSingleton().init_dict_config(LOGGING_CONFIG)

t = time.time()
TIME_STAMP = int(round(t * 1000))

# 清洗数据写入json文件中
class CleanData(object):

    def __init__(self):
        # 目标文件夹
        if os.name == "nt":
            self.target_folders = r"D:\MaXin-Study\2021-10-3\DataClean\Data\BeforeCleanDocx"
            # 方便读取存入的变量
            self.files_format = r"D:\MaXin-Study\2021-10-3\DataClean\Data\BeforeCleanDocx\{}"
            # 转换之后的目标文件
            self.files_result = r"D:\MaXin-Study\2021-10-3\DataClean\Data\BeforeCleanDocx\{}.docx"
            # 查看目标问价夹下有哪些文件
            # self.file_list = os.listdir(self.target_folders)
            #  清洗之后并转换成json的目标文件
            self.json_path = r'D:\MaXin-Study\2021-10-3\DataClean\Data\BeforeCleanJson\{}.json'

            # 转换成json之后的docx文件需要移动到AfterCleanDocx,防止运行时不停的读写
            self.after_docx = r"D:\MaXin-Study\2021-10-3\DataClean\Data\AfterCleanDocx\{}"

            # 无法解析的文件
            self.error_filePath = r"D:\MaXin-Study\2021-10-3\DataClean\Data\ErrorCleanDocx"
            # 无法解析的文件的变量
            self.error_format = r"D:\MaXin-Study\2021-10-3\DataClean\Data\ErrorCleanDocx\{}"

        else:
            self.target_folders = TARGET_FOLDERS
            # 方便读取存入的变量
            self.files_format = FILES_FORMAT
            # 转换之后的目标文件
            self.files_result = FILES_RESULT
            # 查看目标问价夹下有哪些文件
            # self.file_list = os.listdir(self.target_folders)
            #  清洗之后并转换成json的目标文件
            self.json_path = JSON_PATH
            # 转换成json之后的docx文件需要移动到AfterCleanDocx,防止运行时不停的读写
            self.after_docx = AFTER_DOCX
            # 无法解析的文件
            self.error_filePath = ERROR_PATH
            # 无法解析的文件的变量
            self.error_format = ERROR_PATH_FORMAT
        # 暂时以字典的方式存储
        # 舆情分析
        self.AnalysisItems = {
            # 文件名称
            "fileName": "",
            # 地址
            "address": "",
            # 标签
            "label": "",
            # 类型
            "fileType": "",
            # 内容标题
            "title": "",
            # 时间
            "time": "",
            # 网名
            "nickname": "",
            # 信息来源
            "infoSource": "",
            # 发布内容
            "content": "",
            # 原文链接
            "link": "",

            "url": "",
            # 原文内容(文件原本内容)
            "fileContent": "",
        }

        # 舆情预警
        self.YqEarlyWarningItems = {
            # 标记   隐患1 和 专项2
            "sign": "",
            # 地区
            "region": "",
            # 内容标题
            "title": "",
            # # 提取具体内容
            # "content": "",
            # # 提取 姓名
            # "name": "",
            # # 手机号码
            # "phoneNumber": "",
            # # 身份证号码
            # "IdCard": "",
            # # 地址
            # "address": "",
            # 标签
            "label": "",
            # 时间
            "time": "",
            # 文件名称
            "fileName": "",
            # 原文名称   预警文件:《.........》
            "link": "",
            # 原文内容(文件原本内容)
            "fileContent": "",
        }

    def get_text(self, file_path):
        '''
        :param file_path: 文件路径
        :return:获取文档中的所有内容
        '''
        doc = docx.Document(file_path)
        texts = []
        for paragraph in doc.paragraphs:
            texts.append(paragraph.text)
        return '\n'.join(texts)

    def getAddress(self, content):
        retAdd = ""
        for key, value in ADDRESS.items():
            if value in content:
                retAdd = key
                break
            else:
                retAdd = ""
        return retAdd

    # 舆情分析规则
    def YqAnalysis(self, file):
        items = self.AnalysisItems.copy()
        # 文件全部内容
        content = self.get_text(self.files_format.format(file))
        # 文件名称
        fileName = file.replace(".docx", "")
        logging.info("开始清洗")
        # 文件名称
        fileName_result = fileName
        items['fileName'] = fileName_result

        # 地区
        address_result = re.findall('[)）][(（](.*)[）)]', fileName_result)
        if address_result:
            items['address'] = address_result[0]
        else:
            items['address'] = ''

        # 标签
        # fileLabel_result = re.findall('[(（](涉.*)[)）][(（]', fileName_result)
        fileLabel_result = re.findall('[(（](涉.*?)[)）]', fileName_result)
        if fileLabel_result:
            items['label'] = fileLabel_result[0]
        else:
            items['label'] = ""

        # 舆情类型
        fileType_result = re.findall("(即时.*)", content)
        if fileType_result:
            items['fileType'] = fileType_result[0]
        else:
            items['fileType'] = ""

        # 标题
        title_result = re.findall("(网民.*)", content)
        if title_result:
            items['title'] = title_result[0]
        else:
            items['title'] = ""

        # 时间
        time_result = re.findall("(.*月.*日)[，,]", content)
        if time_result:
            # 时间需要转化 由10月30日 转化成时间 2021-10-30 00:00:00
            time_item = self.conversionTime(time_result[0])
            items['time'] = str(time_item)
        else:
            items['time'] = ""

        # 网名
        nickname_result = re.findall('网民“(.*?)”在', content)
        if nickname_result:
            items['nickname'] = nickname_result[0]
        else:
            items['nickname'] = ""

        # 信息来源
        infoSource_result = re.findall('在“(.*?)”[发贴称发贴称]', content)
        if infoSource_result:
            items['infoSource'] = infoSource_result[0]
        else:
            items['infoSource'] = ""

        # 发布内容
        content_result = re.findall('[发贴称发贴称][，,:：](.*?)[\s]原文链接', content)
        if content_result:
            items['content'] = content_result[0]
        else:
            items['content'] = ""

        # # 原文链接
        link_result = re.findall('(http[s]://.*)', content)
        if link_result:
            items['url'] = link_result[0]
        else:
            items['url'] = ""

        items['link'] = "预警文件:《{}》".format(fileName)

        # 原文内容
        fileContent_result = content
        items['fileContent'] = fileContent_result
        return items, fileName

    # # 舆情预警规则
    # def YqEarlyWarning(self, file):
    #     # 文件名称  file
    #     fileName = file.replace('.docx', '')
    #     # 时间 根据 给的 文件名称中提取
    #     fileTimes = re.findall('(.*月.*日)预警信息', fileName)
    #     resTime = ""
    #     if fileTimes:
    #         resTime = self.conversionTime(fileTimes[0])
    #     else:
    #         resTime = ""
    #
    #     # 文件全部内容
    #     content = self.get_text(self.files_format.format(file))
    #     # 开始切割成 隐患类1 和 专项类2
    #     result = []
    #     if "专项监测任务:" in content:
    #         result = content.split('专项监测任务:')
    #     elif "专项监测任务：" in content:
    #         result = content.split('专项监测任务：')
    #
    #     # 《《《《《《《《《《《《《《《《《隐患类》》》》》》》》》》》》》》》》》》》
    #     hidden_danger = result[0]
    #     hidden_danger_result = []
    #     # 再把 隐患类 切割 保留主要信息
    #     if "矛盾风险隐患类:" in hidden_danger:
    #         hidden_danger_result = hidden_danger.split('矛盾风险隐患类:')
    #         # print(result)
    #     elif "矛盾风险隐患类：" in hidden_danger:
    #         hidden_danger_result = hidden_danger.split('矛盾风险隐患类：')
    #
    #     hidden_list = []
    #
    #     if hidden_danger_result:
    #         hidden = hidden_danger_result[1]
    #         hiddenInfos = re.split('\n\d[、]', hidden)
    #         print(hiddenInfos)
    #         for hiddenInfo in hiddenInfos:
    #             YJitems = self.YqEarlyWarningItems.copy()
    #             if hiddenInfo is ' ':
    #                 pass
    #             else:
    #                 sign = "1"
    #                 YJitems['sign'] = sign
    #
    #                 # 地区  就是哪个地区发生的事情
    #                 regions = self.getAddress(hiddenInfo)
    #                 if regions:
    #                     YJitems['region'] = regions
    #                 else:
    #                     YJitems['region'] = ""
    #
    #                 # 提取标题
    #                 titles = re.findall('([【\[涉].*)\n', hiddenInfo)
    #                 if titles:
    #                     YJitems['title'] = titles[0]
    #                 else:
    #                     YJitems['title'] = ""
    #
    #                 print(YJitems['title'])
    #
    #                 # # # 提取具体内容
    #                 # contents = re.findall('\n(.*)\n姓名', hiddenInfo)
    #                 # if contents:
    #                 #     YJitems['content'] = contents[0]
    #                 # else:
    #                 #     YJitems['content'] = ""
    #                 # # # 提取 姓名
    #                 # names = re.findall('姓名[:：](.*?)[,，]', hiddenInfo)
    #                 # if names:
    #                 #     YJitems['name'] = names[0]
    #                 # else:
    #                 #     YJitems['name'] = ""
    #                 #
    #                 # phoneNumbers = re.findall('手机号[码：: ](.*)[,，]身份', hiddenInfo)
    #                 # if phoneNumbers:
    #                 #     YJitems['phoneNumber'] = phoneNumbers[0].replace(':','').replace(' ','')
    #                 # else:
    #                 #     YJitems['phoneNumber'] = ""
    #                 # # # ID card
    #                 # IdCards = re.findall('\d{18}', hiddenInfo)
    #                 # if IdCards:
    #                 #     YJitems['IdCard'] = IdCards[0]
    #                 # else:
    #                 #     YJitems['IdCard'] = ""
    #                 # # # 地址
    #                 # addresss = re.findall('地址[：:](.*)[。]', hiddenInfo)
    #                 # if addresss:
    #                 #     YJitems['address'] = addresss[0]
    #                 # else:
    #                 #     YJitems['address'] = ""
    #
    #                 # 标签
    #                 label = ""
    #                 if "[" in YJitems['title'] or "【" in YJitems['title']:
    #                     # labels = re.findall('【\[(.*?)\]', YJitems['title'])
    #                     labels = re.findall('[\[【](.*?)[\]】]', YJitems['title'])
    #                     if labels:
    #                         label = labels[0]
    #                 else:
    #                     label = YJitems['title']
    #                 YJitems['label'] = label
    #                 # 时间
    #                 times = resTime
    #                 YJitems['time'] = str(times)
    #
    #                 # 文件名称
    #                 filenames = fileName
    #                 YJitems['fileName'] = filenames
    #
    #                 # 原文名称   预警文件:《.........》
    #                 links = "预警文件：《{}》".format(YJitems['title'])
    #                 YJitems['link'] = links
    #                 # 原文内容(文件原本内容)
    #                 YJitems['fileContent'] = hiddenInfo
    #
    #                 hidden_list.append(YJitems)
    #
    #     # 《《《《《《《《《《《《《《《《《《《《专项类》》》》》》》》》》》》》》》》》》
    #     special = result[1]
    #     specialInfos = re.split('\n\d[、]', special)
    #     # print(specialInfos)
    #     for specialInfo in specialInfos:
    #         print(specialInfo)
    #         # if specialInfo is '':
    #         if specialInfo:
    #             pass
    #         else:
    #             YJitems = self.YqEarlyWarningItems.copy()
    #             # # 标题
    #             specialTitle = re.findall('([涉].*?)\n', specialInfo)
    #             if specialTitle:
    #                 YJitems['title'] = specialTitle[0]
    #             else:
    #                 YJitems['title'] = ""
    #             specialContent = re.findall('\n(.*[。])', specialInfo)
    #             if specialContent:
    #                 if len(specialContent) >= 2:
    #                     YJitems['fileContent'] = specialContent[0] + specialContent[1]
    #                 else:
    #                     YJitems['fileContent'] = specialContent[0]
    #             else:
    #                 YJitems['fileContent'] = ""
    #
    #             sign = "2"
    #             YJitems['sign'] = sign
    #
    #             YJitems['region'] = ""
    #
    #             YJitems['label'] = YJitems['title']
    #
    #             YJitems['time'] = str(resTime)
    #
    #             YJitems['fileName'] = fileName
    #
    #             links = "预警文件：《{}》".format(YJitems['title'])
    #             YJitems['link'] = links
    #             hidden_list.append(YJitems)
    #
    #     return hidden_list, fileName

    # 清洗舆情分析数据,存储数据

    # 舆情预警规则
    def YqEarlyWarning(self, file):
        # 文件名称  file
        fileName = file.replace('.docx', '')
        # 时间 根据 给的 文件名称中提取
        fileTimes = re.findall('(.*月.*日)预警信息', fileName)
        resTime = ""
        if fileTimes:
            resTime = self.conversionTime(fileTimes[0])
        else:
            resTime = ""

        # 文件全部内容
        content = self.get_text(self.files_format.format(file))
        # resultContent = content.replace('\n', '')
        resultContent = content
        # print(resultContent)

        # 开始切割成 隐患类1 和 专项类2
        result = []
        if "专项监测任务:" in resultContent:
            result = resultContent.split('专项监测任务:')
        elif "专项监测任务：" in resultContent:
            result = resultContent.split('专项监测任务：')

        # print(result)
        # 再把隐患类切割 保留主要信息
        hidden_danger = result[0]
        hidden_danger_result = []
        # 再把 隐患类 切割 分成了 XX预警信息和主要信息，保留主要信息
        if "矛盾风险隐患类:" in hidden_danger:
            hidden_danger_result = hidden_danger.split('矛盾风险隐患类:')
            # print(result)
        elif "矛盾风险隐患类：" in hidden_danger:
            hidden_danger_result = hidden_danger.split('矛盾风险隐患类：')

        hidden_list = []
        if hidden_danger_result:
            hidden = hidden_danger_result[1]
            hiddenInfos = re.split('\d[、]', hidden)
            for hiddenInfo in hiddenInfos:
                YJitems = self.YqEarlyWarningItems.copy()
                if hiddenInfo == " \n":
                    pass
                elif hiddenInfo == '\n':
                    pass
                elif hiddenInfo == " ":
                    pass
                else:
                    sign = "1"
                    YJitems['sign'] = sign

                    # 地区  就是哪个地区发生的事情
                    regions = self.getAddress(hiddenInfo)
                    if regions:
                        YJitems['region'] = regions
                    else:
                        YJitems['region'] = ""

                    # 提取标题
                    for titleRule in titleRules:
                        titles = re.findall(titleRule, hiddenInfo)
                        if titles:
                            title = titles[0]
                            YJitems['title'] = title
                            break
                        else:
                            YJitems['title'] = ""

                    # 标签
                    label = ""
                    if "[" in YJitems['title'] or "【" in YJitems['title']:
                        for labelRule in labelRules:
                            labels = re.findall(labelRule, YJitems['title'])
                            if labels:
                                label = labels[0]
                            else:
                                label = YJitems['title']
                    else:
                        label = YJitems['title']
                    YJitems['label'] = label
                    # 时间
                    times = resTime
                    YJitems['time'] = str(times)

                    # 文件名称
                    filenames = fileName
                    YJitems['fileName'] = filenames

                    # 原文名称   预警文件:《.........》
                    links = "预警文件：《{}》".format(YJitems['title'])
                    YJitems['link'] = links
                    # 原文内容(文件原本内容)
                    YJitems['fileContent'] = hiddenInfo

                    hidden_list.append(YJitems)

    # 《《《《《《《《《《《《《《《《《《《《专项类》》》》》》》》》》》》》》》》》》
        special = result[1]
        specialInfos = re.split('\d[、]', special)
        for specialInfo in specialInfos:
            print(specialInfo)
            if specialInfo == '\n':
                pass
            else:
                if "今日无新增" in specialInfo:
                    pass
                else:
                    YJitems = self.YqEarlyWarningItems.copy()
                    if "恒大" in specialInfo:
                        YJitems['title'] = "涉恒大今日情况"
                        YJitems['label'] = "涉恒大"

                    elif "银信" in specialInfo:
                        YJitems['title'] = "银信、诺金、汇利群体动态"
                        YJitems['label'] = "涉银信/诺金/汇利"

                    elif "捷越" in specialInfo:
                        YJitems['title'] = "涉捷越今日情况"
                        YJitems['label'] = "涉捷越"

                    else:
                        specialTitle = re.findall('([涉].*?)\n', specialInfo)
                        if specialTitle:
                            YJitems['title'] = specialTitle[0]
                            YJitems['label'] = YJitems['title']
                        else:
                            YJitems['title'] = ""
                            YJitems['label'] = YJitems['title']
                    print(YJitems['title'])
                    specialContent = specialInfo.replace('涉恒大今日情况','').replace('银信、诺金、汇利群体动态','').replace('涉捷越今日情况','')
                    YJitems['fileContent'] = specialContent.replace('\n','')
                    sign = "2"
                    YJitems['sign'] = sign

                    YJitems['region'] = ""

                    YJitems['time'] = str(resTime)

                    YJitems['fileName'] = fileName

                    links = "预警文件：《{}》".format(YJitems['title'])
                    YJitems['link'] = links
                    hidden_list.append(YJitems)

        return hidden_list, fileName


    def clean(self):
        files_list = os.listdir(self.target_folders)
        # 开始对目标文件夹下的docx文件进行清洗
        if os.listdir(self.target_folders):
            logging.info("检测到文件夹下有文件存在---------->{}".format(str(files_list)))
            for file in files_list:
                if file.endswith('.docx'):
                    try:
                        if "预警信息" in file:
                            logging.info("开始清洗 {}文件".format(file))
                            YJitems, fileName = self.YqEarlyWarning(file)
                            self.getFile(items=YJitems, fileName=fileName)
                            # 写入一个文件 就把原docx文件给一到另一个文件夹下
                            logging.info("开始移动文件 {} ...".format(file))
                            self.moveFile(file)
                            logging.info("清洗文件 {} 结束...".format(file))

                        # 舆情分析信息
                        else:
                            FXitems, fileName = self.YqAnalysis(file)
                            # 把清洗好的数据 写入文件中
                            logging.info("开始清洗 {} ...".format(file))
                            self.getFile(items=FXitems, fileName=fileName)
                            logging.info("清洗文件 {} 结束...".format(file))

                            # 写入一个文件 就把原docx文件给一到另一个文件夹下
                            logging.info("开始移动文件 {} ...".format(file))
                            self.moveFile(file)
                            logging.info("清洗文件 {} 结束...".format(file))

                    except Exception as msg:
                        # 如果错误文件目录下存在此文件,先删除
                        if file in os.listdir(self.error_filePath):
                            print(os.listdir(self.error_filePath))
                            os.remove(self.error_format.format(file))
                        logging.exception(logging.exception("出现异常错误{}".format(msg)))
                        filePath = self.files_format.format(file)
                        error_filePath = self.error_filePath
                        shutil.move(filePath, error_filePath)
                        logging.error("没有找到该文件或无法解析")

                else:
                    logging.info("无docx文件")
        else:
            logging.info("无文件可以清洗")

    # 需要把写入好的docx文件给移除或者移动目录
    def moveFile(self, fileName):
        before_filePath = self.files_format.format(fileName)
        after_filePath = self.after_docx.format(fileName)
        shutil.move(before_filePath, after_filePath)

    # 把清洗之后的数据存入新的文件(或者其他方式-----待定)
    def getFile(self, items, fileName):
        try:
            resultPath = self.json_path.format(fileName + str(TIME_STAMP))
            with open(resultPath, "w", encoding="utf-8") as f_json:
                json.dump(items, f_json, ensure_ascii=False, sort_keys=True, indent=4)
                logging.info("清洗文件 {} 并且写入完成...".format(fileName))
        except:
            resultPath = self.json_path.format(fileName + str(TIME_STAMP))
            with open(resultPath, "w", encoding="utf-8") as f_json:
                json.dump(items, f_json, ensure_ascii=False, sort_keys=True, indent=4)
                logging.info("清洗文件 {} 并且写入完成...".format(fileName))

    # 转换时间
    def conversionTime(self, a_time):
        year = datetime.datetime.now().strftime('%Y')
        time_time = a_time.replace('月', '-').replace('日', '')

        time_str = year + "-" + time_time + " 00:00:00"

        dateTime_d = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
        return dateTime_d

    def run(self):
        logging.info("开始")
        self.clean()


if __name__ == '__main__':
    tmp = CleanData()
    while True:
        tmp.run()
        time.sleep(30)
