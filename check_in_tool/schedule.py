# -*- coding: utf-8 -*-

import os
import csv
import logging
from datetime import date

logger = logging.getLogger()


class Schedule:
    def __init__(self, sched_file='schedule.csv'):
        self.__sched_file = sched_file
        self.__rows = []
        self.__names = []
        self.data = {}  # {name:[(st1,ed1),(st2,ed2),...]}
        self.init()

    def init(self):
        with open(self.__sched_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                self.__rows.append(row)
                if not (len(row) & 1):
                    raise Exception(
                        f'schedule file count line should be odd at line[{len(self.__rows)}] [{row}]')
                if row[0] in self.__names:
                    raise Exception(
                        f'schedule file has duplicate names at line[{len(self.__rows)}] [{row}]')
                self.__names.append(row[0])
                segments = []
                length = len(row)
                if length == 1:
                    logging.warning(
                        f'schedule file line[{len(self.__rows())}] has no time segment')
                self.data[row[0]] = []
                now_seg = []
                ended = False
                for i, date_str in enumerate(row[1:]):
                    if ended:
                        if date_str:
                            raise Exception(
                                f'schedule file empty exists in middle at line[{len(self.__rows)}] [{row}]')
                    elif not date_str:
                        if i & 1:
                            raise Exception(
                                f'schedule file time begin and end not matched at line[{len(self.__rows)}] [{row}]')
                        ended = True
                    else:
                        if i & 1:
                            now_seg.append(Schedule.date_phaser(date_str))
                            self.data[row[0]].append(now_seg)
                            now_seg = []
                        else:
                            now_seg.append(Schedule.date_phaser(date_str))

    @staticmethod
    def date_phaser(date_str: str) -> date:
        delimiters = ['/', '-', '.']
        try:
            ret = None
            for delimiter in delimiters:
                if date_str.find(delimiter) != -1:
                    l = date_str.split(delimiter)
                    ret = date(year=int(l[0]), month=int(l[1]), day=int(l[2]))
                    break
            assert ret != None
            return ret
        except:
            raise Exception(f'phase date failed[{date_str}]')


if __name__ == "__main__":
    schedule = Schedule('../schedule.csv')
