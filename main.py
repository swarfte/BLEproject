import projectTools.startUpOptions as PS
import projectTools.csvToExcel as PC

def start (csv_file, setting_file,fix_file):
    #PS.hop_mode(csv_file, setting_file,fix_file)
    PS.CG_mode(csv_file, setting_file,fix_file)


if __name__ == "__main__":
    file_path = PC.open_json("./projectTools/option.json")
    start(file_path["csv_file"],file_path["old_setting_format"],file_path["new_setting_format"])
