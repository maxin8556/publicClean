# 数据汇总
import time

TIMESLEEP = 30

# 需要循环提取的目标文件
TARGET_FOLDERS = "/home/analysis/upload/"
# 方便读取存入的变量
FILES_FORMAT = "/home/analysis/upload/{}"
# 转换之后的目标文件  现在不用
FILES_RESULT = "/home/analysis/upload/{}.docx"
# 清洗之后并转换成json的目标文件
JSON_PATH = "/root/mx/PublicOpinionCleaning/Data/BeforeCleanJson/{}.json"
# 转换成json之后的docx文件需要移动到AfterCleanDocx,防止运行时不停的读写
AFTER_DOCX = "/root/mx/PublicOpinionCleaning/Data/AfterCleanDocx/{}"

# 读取解析之后的json文件路径
READJSONPATH = "/root/mx/PublicOpinionCleaning/Data/BeforeCleanJson"
# format变量
PATHFORMAT = "/root/mx/PublicOpinionCleaning/Data/BeforeCleanJson/{}"
# format变量
AFTERPATHFORMAT = "/root/mx/PublicOpinionCleaning/Data/AfterCleanJson/{}"
#  分析数据最终数据的文件夹
ANALYSIS_RESULT = "/home/analysis/data/analysis_result_{}.json"
# 预警数据文件夹
WARNING_RESULT = "/home/analysis/data/warning_result_{}.json"

# 无法解析的文件目录
ERROR_PATH = "/root/mx/PublicOpinionCleaning/Data/ErrorCleanDocx"
ERROR_PATH_FORMAT = "/root/mx/PublicOpinionCleaning/Data/ErrorCleanDocx/{}"

# 舆情预警地址配置
ADDRESS = {
    "乳山市": "乳山",
    "文登区": "文登",
    "临港": "临港",
    "荣成市": "荣成",
    "高区": "高区",
    "经区": "经区",
    "环翠区": "环翠",
}

# 专项舆情预警配置


analysis_Items = {
    # 平台详情
    "platformDetails": [

    ]
}

warning_Items = {
    "warningList": [

    ]
}

# 时间戳
t = time.time()
TIME_STAMP = int(round(t * 1000))


# 专项舆情
special = [

]
