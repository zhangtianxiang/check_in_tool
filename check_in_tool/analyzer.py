# -*- coding: utf-8 -*-

from datetime import date
from .schedule import Schedule
from .date_data import DateData


class Analyzer:
    def __init__(self, schedule: Schedule, date_data: DateData, date: date):
        self.__schedule = schedule
        self.__date_data = date_data
        self.__date = date
        self.checked = []
        self.not_checked = []
        self.should_not_check = []
        self.unknown_checked = {}
        self.init()

    def init(self):
        # 今日未签到
        checked = []
        not_checked = []
        should_not_check = []
        unknown_checked = {}

        today = self.__date
        schedule = self.__schedule
        date_data = self.__date_data
        for name, segments in schedule.data.items():
            need_check = False
            for [st, ed] in segments:
                if st <= today <= ed:
                    need_check = True
                    break
            if not need_check:
                if name in date_data.data and 'time' in date_data.data[name]:
                    date_data.data[name]['state'] = 'should_not_check'
                continue
            if name in date_data.data:
                if 'time' in date_data.data[name]:
                    date_data.data[name]['state'] = 'checked'
                    checked.append(name)
                else:
                    date_data.data[name]['state'] = 'not_checked'
                    not_checked.append(name)
            else:
                not_checked.append(name)

        for name, v in date_data.data.items():
            if 'state' not in v:
                unknown_checked[name] = v

        self.checked = checked
        self.not_checked = not_checked
        self.should_not_check = should_not_check
        self.unknown_checked = unknown_checked

    def show(self):
        if self.not_checked:
            print('存在以下同学尚未签到')
            print(self.not_checked)
            print('')
        if self.unknown_checked:
            print('存在以下未知签到，需要修改签到名字')
            for name, v in self.unknown_checked.items():
                print(v)
                print(
                    f'签到名字[{name}] 微信昵称[{v.get("nickname","")}] 签到时间[{v.get("time","")}]')
            print('')
        if self.should_not_check:
            print('存在以下同学在时间表外的时间签到，需要更新时间表')
            print(self.should_not_check)
            print('')
