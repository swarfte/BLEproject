import os
import json
import projectTools.csvToExcel as PC

json_path = PC.open_json("./config/option.json")


def create_excel_folder(name):
    folder = name.replace("csv", "excel")
    try:
        os.mkdir(folder)
    except:
        pass


def HOP_put_csv_and_get_excel(csv_file):
    global json_path
    with open(json_path["log_file"], "w", encoding="utf-8") as l:  # 清空log的資料準備下一次使用
        l.write("")

    filer = HopFileControl(csv_file)
    filer.setup_external_name()
    filer.setup_second_name()
    filer.setup_last_name()
    filer.creat_folder()
    excel_file = filer.get_excel_path()
    csv_file = filer.get_csv_path()
    return [csv_file, excel_file]


class HopFileControl(object):
    def __init__(self, path):
        super(HopFileControl, self).__init__()
        self.main_folder = os.listdir(path)  # 獲取有甚麼資料夾

        # *儲存不同檔案夾下的資料
        self.experiment = []
        self.experiment_name = []  # *最外層的名稱
        self.second = []
        self.second_name = []
        self.client_logs = []
        self.gateway_logs = []
        self.inner_file = []
        self.hop_file = []
        self.excel_file = []
        self.csv_file = []

    def setup_external_name(self):  # 獲取最外層的檔案名
        for x in self.main_folder:  # 獲取檔案夾中的檔案名
            inner_name = "./csv" + "/" + x
            self.experiment_name.append(inner_name)
            self.experiment.append(os.listdir(inner_name))

        return [self.experiment_name, self.experiment]

    def setup_second_name(self):  # *獲取client_logs和gateway_logs檔案夾中的檔案
        for x in range(len(self.experiment)):
            for y in range(len(self.experiment[x])):
                inner_name = self.experiment_name[x] + "/" + self.experiment[x][y]
                self.second_name.append(inner_name)
                self.second.append(os.listdir(inner_name))

        return [self.second_name, self.second]

    def setup_last_name(self):  # *獲取完整的路徑
        for x in range(len(self.second)):
            for y in range(len(self.second[x])):
                inner_name = self.second_name[x] + "/" + self.second[x][y]
                if "Client logs" in inner_name:
                    self.client_logs.append(inner_name)
                else:
                    self.gateway_logs.append(inner_name)

        self.inner_file.append(self.client_logs)
        self.inner_file.append(self.gateway_logs)
        return self.inner_file

    def creat_folder(self):  # *創建要用的檔案夾
        path = ""
        global json_path
        with open(json_path, "r", encoding="utf-8") as f:
            path = json.load(f)
        create_excel_folder(path["excel_file"])  # 創建excel根目錄
        for x in self.experiment_name:  # 創建不同的父目錄
            create_excel_folder(x)

        for x in self.second_name:
            create_excel_folder(x)  # *創建不同的子目錄
            for y in range(3):  # 創建3種類型的hop
                hop_path = x + "/" + str(y + 1) + "hop"
                create_excel_folder(hop_path)
                self.hop_file.append(hop_path)

    def get_excel_path(self):  # 生成excel存放的路徑
        for x in self.inner_file:  # *N個檔案
            for y in x:
                temp = y.replace(",", "")
                save = temp[:len(temp) - 7]
                check = temp[len(temp) - 7:]
                number = 0
                for z in check:
                    if z.isdigit():
                        number += 1
                sentence = temp[:len(temp) - (4 + number)] + str(number) + "hop" + "/" + temp[len(temp) - (4 + number):]
                use_sentence = sentence.replace("csv", "excel")
                final_sentence = use_sentence[:len(use_sentence) - 5] + "xlsx"
                self.excel_file.append(final_sentence)

        return self.excel_file

    def get_csv_path(self):  # 生成csv存放的路徑
        for x in range(len(self.second_name)):
            for y in self.second[x]:
                temp = self.second_name[x] + "/" + y
                self.csv_file.append(temp)
        return self.csv_file


def CG_put_csv_and_get_excel(csv_file):
    global json_path
    with open(json_path["log_file"], "w", encoding="utf-8") as l:  # 清空log的資料準備下一次使用
        l.write("")

    filer = CGFileControl(csv_file)
    filer.setup_external_name()
    filer.setup_second_name()
    filer.setup_last_name()
    filer.creat_folder()
    csv_file = filer.get_csv_path()
    excel_file = filer.get_excel_path()

    return [csv_file, excel_file]


class CGFileControl(HopFileControl):
    def __init__(self, path):
        super(CGFileControl, self).__init__(path)

    def creat_folder(self):  # *創建要用的檔案夾
        global json_path
        create_excel_folder(json_path["excel_file"])  # 創建excel根目錄
        for x in self.experiment_name:
            create_excel_folder(x)

    def get_excel_path(self):
        for logs in self.inner_file:
            for y in logs:
                temp = y.replace(",", "")
                save = temp[:len(temp) - 7]
                check = temp[len(temp) - 7:]
                number = 0
                for z in check:
                    if z.isdigit():
                        number += 1
                sentence = temp[:len(temp) - (4 + number)]
                file_name = temp[len(temp) - (4 + number):]
                if "Client logs" in sentence:
                    sentence = sentence[:len(sentence) - len("Client logs") - 1] + file_name
                    sentence = sentence[:len(sentence) - 4] + "c" + ".csv"
                elif "Gateway logs" in sentence:
                    sentence = sentence[:len(sentence) - len("Gateway logs") - 1] + file_name
                    sentence = sentence[:len(sentence) - 4] + "g" + ".csv"
                use_sentence = sentence.replace("csv", "excel")
                final_sentence = use_sentence[:len(use_sentence) - 5] + "xlsx"
                self.excel_file.append(final_sentence)

        return self.excel_file


def get_reformat_G_file(input_path):
    global json_path
    create_excel_folder(json_path["reformatG_file"])
    with open(json_path["reformatG_log"], "w", encoding="utf-8") as l:  # 清空log的資料準備下一次使用
        l.write("")

    filer = reformatFileControl(input_path)
    excel_name = filer.get_native_excel_file()

    return excel_name


class reformatFileControl(object):
    def __init__(self, input_path):
        super(reformatFileControl, self).__init__()
        self.input_path = input_path
        self.main_folder = [x for x in os.listdir(input_path) if ".txt" not in x]  # 獲取有甚麼資料夾,並過濾txt文檔
        self.second_file = [os.listdir(self.input_path + "/" + x) for x in self.main_folder]  # *獲取每個excel檔案夾中的資料

        self.use_file = []  # 真正要使用的檔案
        for x in range(len(self.second_file)):
            temp = []
            for y in range(len(self.second_file[x])):
                if "_res" not in self.second_file[x][y]:
                    use_name = self.input_path + "/" + self.main_folder[x] + "/" + self.second_file[x][y]
                    temp.append(use_name)
            self.use_file.append(temp)  # 最終使用的路徑名

        # self.finally_file[x][y][z] X為檔案夾 Y為res/g類型 Z為指定的檔案
        self.finally_file = []
        for x in range(len(self.use_file)):
            folder = []
            res = []
            g = []

            for y in range(len(self.use_file[x])):
                if "_req" in self.use_file[x][y]:
                    res.append(self.use_file[x][y])
                else:
                    g.append(self.use_file[x][y])

            folder.append(res)
            folder.append(g)
            self.finally_file.append(folder)

    def get_native_excel_file(self):
        global json_path
        for x in self.main_folder:  # 創建子檔案夾
            create_excel_folder(json_path["reformatG_file"] + "/" + x)

        return self.finally_file
