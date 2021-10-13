import pandas as pd
import datetime as dt
import copy
import json

pd.options.mode.chained_assignment = None  # default='warn'


class Change_Time(object):
    def __init__(self, excel_file, config):
        self.setting = config
        super(Change_Time, self).__init__()
        self.old_excel_file = pd.read_excel(excel_file)
        self.new_excel_file = copy.deepcopy(self.old_excel_file)
        self.time_change = self.setting["hours"] * 3600 + self.setting["millisecond"] / 1000
        self.dataNumber = self.old_excel_file.shape[0]
        self.output_name = "New" + excel_file

    def transform(self):
        for x in range(self.dataNumber):
            # for x in range(10):
            time_format = "%Y-%m-%d %H:%M:%S.%f"
            fix_time_format = "%Y-%m-%d %H:%M:%S"
            old_excel_time = self.old_excel_file.loc[x][5] + " " + self.old_excel_file.loc[x][6]
            old_excel_timeArray = dt.datetime.strptime(old_excel_time, time_format)
            old_excel_timeStamp = dt.datetime.timestamp(old_excel_timeArray)  # 化為時間戳形式
            # print(old_excel_time)

            new_excel_timeStamp = old_excel_timeStamp + self.time_change
            try:
                new_excel_timeArrayy = dt.datetime.strptime(str(dt.datetime.fromtimestamp(new_excel_timeStamp)),
                                                            time_format)
            except ValueError:
                new_excel_timeArrayy = dt.datetime.strptime(str(dt.datetime.fromtimestamp(new_excel_timeStamp)),
                                                            fix_time_format)
            new_excel_time = str(new_excel_timeArrayy)[:len(str(new_excel_timeArrayy)) - 3]  # *實際要用的時間
            new_day = new_excel_time[:10]
            new_time = new_excel_time[11:]

            # self.new_excel_file.loc[x][5] = new_day
            # self.new_excel_file.loc[x][6] = new_time
            self.new_excel_file.loc[x, "day"] = new_day
            self.new_excel_file.loc[x, "time"] = new_time

        self.new_excel_file.to_excel(self.output_name, index=None)


if __name__ == "__main__":
    with open("config.json", "r", encoding="utf-8") as f:
        setting = json.load(f)
        run = Change_Time(setting["excel_file"], setting)
        run.transform()
