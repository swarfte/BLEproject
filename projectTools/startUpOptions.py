import projectTools.csvToExcel as PC
import projectTools.fileManagement as PF
import pandas as pd

def hop_mode(csv_file, setting_file,fix_file):#*按檔案夾名生成對應的端口和hop檔案夾
    print("hop mode start!")
    all_file = PF.HOP_put_csv_and_get_excel(csv_file)
    for x in range(len(all_file[0])):
        try:
            run = PC.CTE(all_file[0][x],setting_file,all_file[1][x])
            run.transform()
        except:
            try:
                Frun = PC.FCTE(all_file[0][x],fix_file,all_file[1][x])
                Frun.transform()
            except pd.errors.EmptyDataError:
                with open ("log.txt","a",encoding="utf-8") as log:
                    sentence = "檔案:" + all_file[0][x] + "為空白,因此不能正確地轉為excel檔\n"
                    log.write(sentence)
            except:
                with open ("log.txt","a",encoding="utf-8") as log:
                    sentence = "檔案:" + all_file[0][x] + "出現了未知的錯誤\n"
                    log.write(sentence)


def CG_mode(csv_file, setting_file,fix_file):#*生成對應的檔案夾名,並在檔案名後加上c或g進行區分
    print("CG mode start")
    all_file = PF.CG_put_csv_and_get_excel(csv_file)
    print(all_file)