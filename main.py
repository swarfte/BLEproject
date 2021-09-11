import projectTools.csvToExcel as PC
import projectTools.fileManagement as PF
import pandas as pd

def setup(csv_file, setting_file):
    filer = PF.FileControl(csv_file)
    csv_file_list = filer.get_css_path()
    for x in csv_file_list:
        for y in x :#css的檔案名
            try:
                build_path = filer.get_excel_file_path(y)
                #print(build_path)
                run = PC.CTE(y,setting_file,build_path)
                run.transform()
            except pd.errors.EmptyDataError:
                with open ("log.txt","a",encoding="utf-8") as log:
                    sentence = "檔案:" + y + "為空白,因此不能正確地轉為excel檔\n"
                    log.write(sentence)
            except:
                with open ("log.txt","a",encoding="utf-8") as log:
                    sentence = "檔案:" + y + "出現了未知的錯誤\n"
                    log.write(sentence)

def start (csv_file, setting_file):
    setup(csv_file,setting_file)

if __name__ == "__main__":
    start("./csv","./projectTools/setting.json")