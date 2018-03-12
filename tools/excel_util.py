# -*- coding:utf-8 -*-

"""
@author: wsy
@file: excel_util.py
@time: 2017/6/15 17:01
"""
import xlrd
import xlwt
import tornado.gen


class excel_util(object):

    # 表格默认第一行为标题，内容从第二行读起
    START_LINE = 1

    @staticmethod
    def exclude(list, filePath):
        """
        将链表数据导出到excel表格
        :param params: list按excel->sheet->raw层级传参，指明filepath文件路径
        :return:   
        """
        file = xlwt.Workbook()
        index = 0
        result = True
        try:
            for sheet in list:
                sht = file.add_sheet(u'sheet{}'.format(index), cell_overwrite_ok=True)
                index = index + 1
                for raw in sheet:
                    for r in range(0, len(raw)):
                        sht.write(0, r, raw[r], excel_util.set_style('Times New Roman', 220, True))
            file.save(filePath)
        except (Exception, IOError), e:
            result = False
            print e
        return result

    @staticmethod
    def include(filePath,startLine=1):
        """
        将excel表格数据读出到数据链表，默认从第二行读起
        :param self: 
        :return: list:按照excel->sheet->行 层级存储
        """
        sheets = []
        workbook = xlrd.open_workbook(filePath)
        sheetNames = workbook.sheet_names()
        try:
            for sheetName in sheetNames:
                sheet = workbook.sheet_by_name(sheetName)
                rawCount = sheet.nrows
                result = []
                for r in range(startLine, rawCount):
                    result.append(sheet.row_values(r))
                sheets.append(result)
                # print(result)
        except (Exception, IOError), e:
            print e
        return sheets

    @staticmethod
    def set_style(name, height, bold=False):
        '''
        设置导入数据样式
        :param name: 字体名称
        :param height: 字体大小
        :param bold: 字体加粗
        :return: 
        '''
        style = xlwt.XFStyle()  # 初始化样式
        font = xlwt.Font()  # 为样式创建字体
        font.name = name  # 'Times New Roman'
        font.bold = bold
        font.color_index = 4
        font.height = height
        style.font = font
        return style


if __name__ == '__main__':
    # filePath = 'C:\ExpressCode.xls'
    # excel_util.include(filePath)
    list = [[[u'AJ', u'\u5b89\u6377\u5feb\u9012', u'', u'']], [[u'AJ', u'\u5b89\u6377\u5feb\u9012', u'', u'']]]
    file = excel_util.exclude(list, 'D:/new_excel.xls')
