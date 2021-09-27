import projectTools.csvToExcel as PC
import projectTools.fileManagement as PF
import pandas as pd

def setup(csv_file, setting_file):
    #TODO
    all_file = PF.put_csv_and_get_excel(csv_file)
    for x in range(len(all_file[0])):
        try:
            run = PC.CTE(all_file[0][x],setting_file,all_file[1][x])
            run.transform()
        except pd.errors.EmptyDataError:
            with open ("log.txt","a",encoding="utf-8") as log:
                    sentence = "檔案:" + all_file[0][x] + "為空白,因此不能正確地轉為excel檔\n"
                    log.write(sentence)
        except:
            with open ("log.txt","a",encoding="utf-8") as log:
                    sentence = "檔案:" + all_file[0][x] + "出現了未知的錯誤\n"
                    log.write(sentence)

def start (csv_file, setting_file):
    setup(csv_file,setting_file)

if __name__ == "__main__":
    start("./csv","./projectTools/setting.json")

