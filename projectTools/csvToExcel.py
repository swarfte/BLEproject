import json
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

def open_json(path):
    with open(path, "r", encoding="utf-8") as f:
        setting = json.load(f)
    return setting

class CTE(object):
    def __init__(self, csvFile, json_path,excelFile):
        super(CTE, self).__init__()
        self.setting = open_json(json_path)
        self.csvFileName = csvFile
        self.excelFileName = excelFile
        self.csvDate = pd.read_csv(self.csvFileName,encoding="utf-8")
        #self.dataNumber = 1000  # *固定檢測數據
        self.dataNumber = self.csvDate.shape[0] + 1 # *動態檢測行數
        self.oldExcelDate = pd.DataFrame()
        self.temp_column = [x["column"] for x in self.setting]
        self.column = []
        if "Client logs" not in self.csvFileName:#*Gateway logs的情況
            self.column = self.temp_column
            self.newExcelData = pd.DataFrame({#新的格式
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
            self.newExcelData = pd.DataFrame({#新的格式
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
                    self.newExcelData.loc[x] = temp
                    check_index += 1
            except:
                pass
        self.newExcelData.to_excel(self.excelFileName, index=None)  # 寫入檔案


class FCTE(CTE):
    def __init__(self, csvFile, json_path,excelFile):
        super(FCTE, self).__init__(csvFile, json_path,excelFile)
        self.temp_column = [x["column"] for x in self.setting]
        self.column = self.temp_column
        self.newExcelData = pd.DataFrame({#新的格式,創建7個欄位
            self.column[0]:["" for x in range(self.dataNumber)],#0 type
            self.column[1]:[x+1 for x in range(self.dataNumber)],#1 sequence
            self.column[2]:["" for x in range(self.dataNumber)],#2 byte
            self.column[3]:["" for x in range(self.dataNumber)],#3 hop
            self.column[4]:["" for x in range(self.dataNumber)],#4 Signal strength
            "day":["" for x in range(self.dataNumber)],#5 day
            self.column[5]:["" for x in range(self.dataNumber)],#6 time
            self.column[6]:["" for x in range(self.dataNumber)]#7 gmtime
        })

    def transform(self):
        for x in range(len(self.column)):
            self.oldExcelDate[self.column[x]] = self.csvDate.iloc[0:len(self.csvDate), [x]]  # 獲取csv中每一欄的資料

        if "Client logs" in self.csvFileName:#*格式不齊的情況
            for x in range(self.dataNumber):
                try:
                    if "2021" in self.oldExcelDate[self.column[2]][x]:#*檢測是否錯行,是的話就移動資料

                        #移動兩欄時間
                        self.oldExcelDate[self.column[5]][x] = self.oldExcelDate[self.column[2]][x]
                        self.oldExcelDate[self.column[6]][x] = self.oldExcelDate[self.column[3]][x]

                        #刪除兩欄重覆的時間
                        self.oldExcelDate[self.column[2]][x] = ""
                        self.oldExcelDate[self.column[3]][x] = ""
                except:
                    pass

        time_column = []
        day_column = []
        gmtime_column = self.oldExcelDate[self.column[6]]

        for x in self.oldExcelDate[self.column[5]]:
            try:
                time_column.append(x[11:-1])  # 時間
                day_column.append(x[0:10])  # 日期
            except:
                time_column.append("")
                day_column.append("")

        #*直接刪除原本的欄
        self.oldExcelDate.drop(self.column[5], axis=1, inplace=True)
        self.oldExcelDate.drop(self.column[6], axis=1, inplace=True)

        self.oldExcelDate["day"] = day_column
        self.oldExcelDate["time"] = time_column
        self.oldExcelDate["gmtime"] = gmtime_column

        for x in range(self.dataNumber):
            try:
                self.newExcelData.loc[x] = self.oldExcelDate.loc[x]
            except:
                pass
        self.newExcelData.to_excel(self.excelFileName, index=None)  # 寫入檔案

class SQ_FCTE(FCTE):
    def __init__(self, csvFile, json_path,excelFile):
        super(SQ_FCTE, self).__init__(csvFile, json_path,excelFile)
        self.req_ExcelData = self.newExcelData
        self.res_ExcelData = self.newExcelData

    def transform(self):
        for x in range(len(self.column)):
            self.oldExcelDate[self.column[x]] = self.csvDate.iloc[0:len(self.csvDate), [x]]  # 獲取csv中每一欄的資料

        if "Client logs" in self.csvFileName:#*格式不齊的情況
            for x in range(self.dataNumber):
                try:
                    if "2021" in self.oldExcelDate[self.column[2]][x]:#*檢測是否錯行,是的話就移動資料

                        #移動兩欄時間
                        self.oldExcelDate[self.column[5]][x] = self.oldExcelDate[self.column[2]][x]
                        self.oldExcelDate[self.column[6]][x] = self.oldExcelDate[self.column[3]][x]

                        #刪除兩欄重覆的時間
                        self.oldExcelDate[self.column[2]][x] = ""
                        self.oldExcelDate[self.column[3]][x] = ""
                except:
                    pass

        time_column = []
        day_column = []
        gmtime_column = self.oldExcelDate[self.column[6]]

        for x in self.oldExcelDate[self.column[5]]:
            try:
                time_column.append(x[11:-1])  # 時間
                day_column.append(x[0:10])  # 日期
            except:
                time_column.append("")
                day_column.append("")

        #*直接刪除原本的欄
        self.oldExcelDate.drop(self.column[5], axis=1, inplace=True)
        self.oldExcelDate.drop(self.column[6], axis=1, inplace=True)

        #加入新的欄位
        self.oldExcelDate["day"] = day_column
        self.oldExcelDate["time"] = time_column
        self.oldExcelDate["gmtime"] = gmtime_column

        #TODO 控制res/req的輸出
        check = 0
        for x in range(self.dataNumber):
            try:
                if "Client logs" in self.csvFileName:#如果是Client的話則判斷res和req
                    if "req" in self.oldExcelDate[self.column[0]][x]:
                        self.req_ExcelData.loc[x-check] = self.oldExcelDate.loc[x]
                        check += 1
                    else:
                        self.res_ExcelData.loc[x] = self.oldExcelDate.loc[x]
                else:
                    self.newExcelData.loc[x] = self.oldExcelDate.loc[x]
            except:
                pass

        if "Client logs" in self.csvFileName:#按res/rsq檔名分類
            res_name = self.excelFileName[:len(self.excelFileName)-5] + "_res" + ".xlsx"
            req_name = self.excelFileName[:len(self.excelFileName)-5] + "_req" + ".xlsx"
            self.req_ExcelData.to_excel(req_name,index=None)
            self.res_ExcelData.to_excel(res_name, index=None)

        else:
            self.newExcelData.to_excel(self.excelFileName, index=None)  # 寫入檔案