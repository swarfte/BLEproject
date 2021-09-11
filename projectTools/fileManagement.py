import os

def create_excel_log(name):
    local = os.getcwd()
    logs = local + "/excel" + "/" + name
    try:
        os.mkdir(logs)
    except:
        pass

class FileControl (object):
    def __init__(self,path):
        super(FileControl, self).__init__()
        self.main_folder = os.listdir(path)#獲取有甚麼資料夾
        self.client_logs = []
        self.gateway_logs = []
        self.inner_file = []

    def get_css_path(self):
        temp_file = []
        for x in self.main_folder:#獲取檔案夾中的檔案名
            inner_name = "./csv" + "/" + x
            temp_file.append(os.listdir(inner_name))

        # for folder in temp_file:
        #     for file in folder:
        #         num_count = 0
        #         temp_file_path = ""
        #
        #         if folder == temp_file[0] :
        #             temp_file_path = "./csv" + "/" + "Client logs" + "/"
        #         else:
        #             temp_file_path = "./csv" + "/" + "Gateway logs" + "/"
        #
        #         for x in file:#查找有多少個數字
        #             if x.isdigit():#
        #                 num_count += 1
        #
        #         hop_file_path = temp_file_path + str(num_count) + "hop" + "/"
        #         use_inner_file = hop_file_path + file#加入詳細的相對路徑
        #
        #         if folder == temp_file[0]:#Client logs的情況
        #             self.client_logs.append(use_inner_file)
        #         else:
        #             self.gateway_logs.append(use_inner_file)

        for folder in temp_file:
            for file in folder:
                if folder == temp_file[0]:
                    use_inner_file = "./csv" + "/" + "Client logs" + "/" + file#加入詳細的相對路徑
                    self.client_logs.append(use_inner_file)
                else:
                    use_inner_file = "./csv" + "/" + "Gateway logs" + "/" + file
                    self.gateway_logs.append(use_inner_file)

        self.inner_file.append(self.client_logs)
        self.inner_file.append(self.gateway_logs)

#===========================================================
        #按分類成生資料夾
        save_path = ["Client logs","Gateway logs"]
        for x in save_path :
            create_excel_log(x)
            for y in range(3):
                temp = x + "/" + str(y+1) + "hop"
                create_excel_log(temp)

        return self.inner_file #第一個數組是click的 第2個

    def get_excel_file_path(self,css_file):
        num_count = 0
        temp_file_path = ""
        temp_file_file = ""
        path = css_file.replace("csv","excel")
        for x in path:
            if x.isdigit():#*判斷為多少hop
                num_count += 1
        if "Client logs" in path :
            path = path.replace(",","")
            temp_file_path = path[:20]
            temp_file_file = path[20:]
        else:
            temp_file_path = path[:21]
            temp_file_file = path[21:]
        path = temp_file_path + str(num_count) + "hop" + "/" + temp_file_file #*中間插入hop的位置
        use_path = path[:len(path) - 5] + "xlsx"#*剛去由csv換成的excel

        return use_path


