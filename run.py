# -*- coding: utf-8 -*-

import sys

from datetime import date

import check_in_tool

if __name__ == "__main__":
    time_str = input(f'输入日期，默认"{date.today()}":')
    if not time_str:
        print(f'得到空串，将使用"{date.today()}"')
        today = date.today()
    else:
        today = check_in_tool.Schedule.date_phaser(time_str)
    print('\n将要处理日期:', today)
    opt = ['Y', 'y', 'Yes', 'yes', '1']
    ok = input(f'是否确认？{opt}\n')
    if ok not in opt:
        sys.exit()
    else:
        print('')
    data_phaser = check_in_tool.DataPhaser('data.xls', today)
    data_phaser.save()
    schedule = check_in_tool.Schedule()
    date_data = check_in_tool.DateData(today)
    analyzer = check_in_tool.Analyzer(schedule, date_data, today)
    analyzer.show()
