import projectTools.startUpOptions as PS
import projectTools.csvToExcel as PC



def start (option):
    #PS.hop_mode(option)
    PS.CG_mode(option)
    #PS.test_mode(option)


if __name__ == "__main__":
    file_path = PC.open_json("./config/option.json")
    start(file_path)
