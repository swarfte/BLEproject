import json
import pandas as pd

def open_json(path):
    with open(path, "r", encoding="utf-8") as f:
        setting = json.load(f)
    return setting

class CTE(object):
    def __init__(self, csvFile, json_path,excelFile):
        super(CTE, self).__init__()
        self.dataNumber = 1000  # *檢測數字
        self.setting = open_json(json_path)
        self.csvFileName = csvFile
        self.excelFileName = excelFile
        self.csvDate = pd.read_csv(self.csvFileName,encoding="utf-8")
        self.oldExcelDate = pd.DataFrame()
        self.temp_column = [x["column"] for x in self.setting]
        self.column = []
        if "Client logs" not in self.csvFileName:#*Gateway logs的情況
            self.column = self.temp_column
            self.newExcelDate = pd.DataFrame({#新的格式
                self.column[0]:[x + 1 for x in range(self.dataNumber)],
                self.column[1]:["" for x in range(self.dataNumber)],
                self.column[2]:["" for x in range(self.dataNumber)],
                self.column[3]:["" for x in range(self.dataNumber)],
                "day":["" for x in range(self.dataNumber)],
                self.column[4]:["" for x in range(self.dataNumber)],
                self.column[5]:["" for x in range(self.dataNumber)]
            })
        else:#Client logs的情況
            self.column = [self.temp_column[0],self.temp_column[4],self.temp_column[5]]
            self.newExcelDate = pd.DataFrame({#新的格式
                self.column[0]:[x + 1 for x in range(self.dataNumber)],
                self.column[1]:["" for x in range(self.dataNumber)],
                "day":["" for x in range(self.dataNumber)],
                self.column[2]:["" for x in range(self.dataNumber)],
            })
    def native_transform(self):  # 不作任何修改的寫入
        for x in range(len(self.column)):
            self.oldExcelDate[self.column[x]] = self.csvDate.iloc[0:len(self.csvDate), [x]]  # 獲取csv中每一欄的資料

        self.oldExcelDate.to_excel(self.excelFileName, index=None)  # 寫入檔案

    def transform(self):  # *填空且分成時間和日期兩欄
        for x in range(len(self.column)):
            self.oldExcelDate[self.column[x]] = self.csvDate.iloc[0:len(self.csvDate), [x]]  # 獲取csv中每一欄的資料
        if "Client logs" not in self.csvFileName:
            time_and_day_column = self.oldExcelDate[self.column[4]]  # *獲取時間欄
            gmtime_column = self.oldExcelDate[self.column[5]]
        else:
            time_and_day_column = self.oldExcelDate[self.column[1]]  # *獲取時間欄
            gmtime_column = self.oldExcelDate[self.column[2]]

        time_column = []
        day_column = []

        for x in time_and_day_column:
            time_column.append(x[11:-1])  # 時間
            day_column.append(x[0:10])  # 日期

        # 刪除欄
        if "Client logs" not in self.csvFileName:
            self.oldExcelDate.drop(self.column[4], axis=1, inplace=True)
            self.oldExcelDate.drop(self.column[5], axis=1, inplace=True)
        else:
            self.oldExcelDate.drop(self.column[1], axis=1, inplace=True)
            self.oldExcelDate.drop(self.column[2], axis=1, inplace=True)

        # 增加欄
        self.oldExcelDate["day"] = day_column
        self.oldExcelDate["time"] = time_column
        self.oldExcelDate["gmtime"] = gmtime_column

        check_index = 0
        for x in range(self.dataNumber):
            try:
                #*對比新舊資料
                old_data_number = int(self.oldExcelDate.iloc[check_index].at[self.column[0]])
                if x+1 == old_data_number:#檢測到有資料匹配
                    temp = list(self.oldExcelDate.loc[check_index])
                    self.newExcelDate.loc[x] = temp
                    check_index += 1
            except:
                pass
        self.newExcelDate.to_excel(self.excelFileName, index=None)  # 寫入檔案