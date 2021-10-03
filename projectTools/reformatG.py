import projectTools.csvToExcel as PC
import pandas as pd
import datetime as dt
import os
import re

class RG(object):
    def __init__(self,req_file,json_path,gateway_file):
        super(RG, self).__init__()
        self.setting = PC.open_json(json_path)
        self.temp_column = [x["column"] for x in self.setting]
        self.column = self.temp_column
        self.req = pd.read_excel(req_file)
        self.gateway_file_name = gateway_file
        self.gateway = pd.read_excel(gateway_file)
        self.dataNumber = self.req.shape[0] #req的行數比gateway多
        self.choice = re.compile(r"\d+g.xlsx")
        self.file_name = re.search(self.choice,self.gateway_file_name).group()#檔案名 r/q共通的
        self.new_gateway_folder = self.gateway_file_name.replace(self.file_name,"") + "reformatG/"#存放新的excel檔案夾
        self.new_gateway_excel_path = self.new_gateway_folder + "New" + self.file_name#新的excel存放路徑
        self.gateway_index = 0
        #self.new_excel_file = copy.deepcopy(self.gateway)
        self.new_excel_file = pd.DataFrame({  # 新的格式,創建7個欄位
            self.column[0]: ["" for x in range(self.dataNumber)],  # 0 type
            self.column[1]: [x + 1 for x in range(self.dataNumber)],  # 1 sequence
            self.column[2]: ["" for x in range(self.dataNumber)],  # 2 byte
            self.column[3]: ["" for x in range(self.dataNumber)],  # 3 hop
            self.column[4]: ["" for x in range(self.dataNumber)],  # 4 Signal strength
            "day": ["" for x in range(self.dataNumber)],  # 5 day
            self.column[5]: ["" for x in range(self.dataNumber)],  # 6 time
            self.column[6]: ["" for x in range(self.dataNumber)]  # 7 gmtime
        })

    def transform(self):
        #生成檔案夾
        try:
            os.mkdir(self.new_gateway_folder)
        except:
            pass

        for x in range(self.dataNumber):
            try:
                time_format = "%Y-%m-%d %H:%M:%S.%f"  # 設定時間格式

                #轉化req的時間
                req_time = self.req.loc[x][5] + " " + self.req.loc[x][6]#獲取每一行日期+時間
                req_timeArray = dt.datetime.strptime(req_time,time_format)
                req_timeStamp = dt.datetime.timestamp(req_timeArray)#轉為整數形式進行比較

                #轉化gateway的時間
                gateway_time = self.gateway.loc[self.gateway_index][5] + " " + self.gateway.loc[self.gateway_index][6]
                gateway_timeArray = dt.datetime.strptime(gateway_time,time_format)
                gateway_timeStamp = dt.datetime.timestamp(gateway_timeArray)#轉為整數形式進行比較

                check_time = gateway_timeStamp - req_timeStamp

                if self.req.loc[x][1] == self.gateway.loc[self.gateway_index][1]:#如果是一樣的sequence
                    if 0 < check_time < 1 :#*判斷req時間遲過recv時間
                        self.new_excel_file.loc[x] = self.gateway.loc[self.gateway_index]
                        self.gateway_index += 1
                    else:
                        self.new_excel_file.loc[x] = ""
                else:
                    self.new_excel_file.loc[x] = ""
            except Exception as ex:
                #print(str(ex))
                pass

        self.new_excel_file.to_excel(self.new_gateway_excel_path,index=None)

if __name__ == "__main__":
    q = "../excel/Experiment 2/25c_req.xlsx "
    j = "../config/F_excel_setting.json"
    g = "../excel/Experiment 2/25g.xlsx"

    A = RG(q,j,g)
    A.transform()


