# -*- coding: utf-8 -*-

from datetime import date

import check_in_tool

if __name__ == "__main__":
    time_str = input('输入日期，如"2020-01-13":')
    print(time_str)
    today = check_in_tool.Schedule.date_phaser(time_str)
    print('日期:', today)
    data_phaser = check_in_tool.DataPhaser('data.xls', today)
    data_phaser.save()
    schedule = check_in_tool.Schedule()
    date_data = check_in_tool.DateData(today)
    analyzer = check_in_tool.Analyzer(schedule, date_data, today)
    analyzer.show()