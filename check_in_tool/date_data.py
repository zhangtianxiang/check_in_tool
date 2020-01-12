# -*- coding: utf-8 -*-
'''
两个功能

1. phaser 将从小签到后台下载下来的xls文件转为csv文件，并存储为对应日期的文件
2. reader 将日期对应的csv文件读出。
'''

import os
import xlrd
import csv
import logging

from datetime import date

logger = logging.getLogger()


class DataPhaser:
    def __init__(self, data_file: str, date: date):
        self.__data_file = data_file
        self.__save_file = date.isoformat()+'.csv'
        self.__date = date
        self.__names = []
        self.__rows = []
        self.init()

    def init(self):
        work_book = xlrd.open_workbook(self.__data_file)
        work_sheet = work_book.sheet_by_name('checkin_data')
        for i, row in enumerate(work_sheet.get_rows()):
            if not i:
                continue
            nickname = row[0].value
            name = row[1].value
            time = row[5].value
            logger.info(f'nickname[{nickname}] name[{name}] time[{time}]')
            if name in self.__names:
                raise Exception(f'data file has duplicate names[{name}]')
            self.__names.append(name)
            self.__rows.append([name, time, nickname])

    def save(self, filename=None):
        if not filename:
            filename = os.path.join('data', self.__save_file)
        # 保存到data/date.csv
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerows(self.__rows)


class DateData:
    def __init__(self, date: date):
        self.__rows = []
        self.__names = []
        self.data = {}
        self.__date = date
        self.__data_file = date.isoformat()+'.csv'
        self.init()

    def init(self):
        with open(os.path.join('data', self.__data_file), 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self.__rows.append(row)
                name = row[0]
                time = row[1]
                nickname = row[2]
                if name in self.__names:
                    raise Exception(f'data file has duplicate names[{name}]')
                self.__names.append(name)
                self.data[name] = {}
                self.data[name]['nickname'] = nickname
                if time != 'X':
                    self.data[name]['time'] = time


if __name__ == "__main__":
    data_phaser = DataPhaser('./tmp/data2.xls', date(2020, 1, 12))
    dateData = DateData(date(2020, 1, 12))
