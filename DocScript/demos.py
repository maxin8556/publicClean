import os
import re
import shutil

import docx


class Demo(object):
    # docx目录
    files_result = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\docxResult"
    files_resultFormat = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\docxResult\{}"
    nweFileNameFormat = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\docxResult\{}.docx"
    moveResultFormat = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\qqqqqqq\{}.docx"
    moveNoneFileFormat = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\NoneFile\{}.docx"

    def getText(self, file_path):
        '''
        :param file_path: 文件路径
        :return:获取文档中的所有内容
        '''
        doc = docx.Document(file_path)
        texts = []
        for paragraph in doc.paragraphs:
            texts.append(paragraph.text)
        return '\n'.join(texts)

    # 移动目录
    def moveFile(self, fileName):
        before_filePath = self.nweFileNameFormat.format(fileName)
        after_filePath = self.moveResultFormat.format(fileName)
        shutil.move(before_filePath, after_filePath)

    def getTitle(self):
        doc_files = os.listdir(self.files_result)
        print(len(doc_files))
        i = 0
        for doc_file in doc_files:
            print("原文件名称---->{}".format(doc_file))
            if doc_file:
                file_path = self.files_resultFormat.format(doc_file)
                content = self.getText(file_path)
                if "工作中发现" in content:
                    pass
                else:
                    title = ""
                    # 即时涉威舆情
                    # 网民反映威海职业学院疑似强制学生办信用卡
                    title_result = re.findall("即时涉威舆情\n(.*)\n", content)
                    if title_result:
                        i += 1
                        title = title_result[0] + "({})".format(i)
                        print("{}文件的标题为------>{}".format(doc_file, title))
                        oldFileName = file_path
                        newFileName = self.nweFileNameFormat.format(title)
                        os.rename(oldFileName,newFileName)
                        print("{}文件的文件名修改为------>{}".format(doc_file, title))
                        self.moveFile(title)

                    else:
                        title = "None"
                        print("{}文件的标题为------>{}".format(doc_file, title))
                        res = doc_file.replace('.docx','')
                        self.moveFile(res)



    def run(self):
        self.getTitle()


if __name__ == '__main__':
    tmp = Demo()
    tmp.run()
