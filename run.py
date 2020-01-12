# -*- coding: utf-8 -*-

from datetime import date

import check_in_tool

if __name__ == "__main__":
    today = date(2020, 1, 12)
    data_phaser = check_in_tool.DataPhaser('data.xls', today)
    data_phaser.save()
    schedule = check_in_tool.Schedule()
    date_data = check_in_tool.DateData(today)
    analyzer = check_in_tool.Analyzer(schedule, date_data, today)
    analyzer.show()