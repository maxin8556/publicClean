import os
import shutil

import docx
from win32com import client

"""
doc 转 docx
"""


class Infos(object):
    # doc目录下
    docFiles = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\docFile"
    files_format = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\docFile\{}"
    # 转换之后的docx目录
    files_result = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\docxResult\{}.docx"

    failDoc = r"D:\MaXin-Study\2021-10-3\DataClean\DocScript\failDoc\{}"

    # 失败的目录


    # 获取文件中的全部内容
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

    # 转换docx类型,把文件doc为后缀的传入
    def convertDocx(self, doc_file):
        """
        :param file: 需要转换的文件名称
        :return:
        """
        try:
            word = client.Dispatch('Word.Application')
            # 把文件名称路径传入方法中
            path = self.files_format.format(doc_file)
            # 目标路径下的文件
            doc = word.Documents.Open(path)
            # 转换后的文件地址  先把 .docFile 后缀名 删除
            modify_suffix = doc_file.replace('.doc', '')
            # 转化后路径下的文件
            new_fileName = self.files_result.format(modify_suffix)
            # 12 转换成docx模式
            doc.SaveAs(new_fileName, 12)
            doc.Close()
            word.Quit()
            return "SUCCESS"
        except:
            return "FAIL"

    # 移动目录
    def moveFile(self, fileName):
        before_filePath = self.files_format.format(fileName)
        after_filePath = self.failDoc.format(fileName)
        shutil.move(before_filePath, after_filePath)

    # 先转换docx文件,再删除转换后的 doc文件
    def removeDocx(self):
        # doc目录下的所有doc文件
        doc_files = os.listdir(self.docFiles)
        print(len(doc_files))
        for doc_file in doc_files:
            print(doc_file)
            if doc_file.endswith(".doc"):
                # 转换成docx
                conversionResults = self.convertDocx(doc_file)
                # 如果转换失败的，不操作
                if conversionResults == "FAIL":
                    print("{} ------> {}".format(doc_file, conversionResults))
                # 转换成功的移动原有文件
                else:
                    print("{} ------> {}".format(doc_file, conversionResults))
                    self.moveFile(doc_file)

    def run(self):
        self.removeDocx()


if __name__ == '__main__':
    tmp = Infos()
    tmp.run()

# 先转换docx文件读取内容，再重写写入为docx文件
