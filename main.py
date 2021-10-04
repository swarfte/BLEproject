import projectTools.startUpOptions as PS
import projectTools.csvToExcel as PC



def start (option):
    #PS.hop_mode(option)
    PS.CG_mode(option) #轉換全部檔案
    #PS.test_mode(option)
    #PS.reformatG_mode(option)#自動化對齊


if __name__ == "__main__":
    file_path = PC.open_json("./config/option.json")
    start(file_path)
