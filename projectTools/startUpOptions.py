import projectTools.csvToExcel as PC
import projectTools.fileManagement as PF
import projectTools.reformatG as PR
import pandas as pd


def hop_mode(options):  # *按檔案夾名生成對應的端口和hop檔案夾
    print("hop mode start!")
    all_file = PF.HOP_put_csv_and_get_excel(options["csv_file"])
    for x in range(len(all_file[0])):
        try:
            run = PC.CTE(all_file[0][x], options["old_setting_format"], all_file[1][x])
            run.transform()
        except:
            try:
                Frun = PC.FCTE(all_file[0][x], options["new_setting_format"], all_file[1][x])
                Frun.transform()
            except pd.errors.EmptyDataError:
                with open(options["log_file"], "a", encoding="utf-8") as log:
                    sentence = "檔案:" + all_file[0][x] + "為空白,因此不能正確地轉為excel檔\n"
                    log.write(sentence)
            except Exception as ex:
                with open(options["log_file"], "a", encoding="utf-8") as log:
                    sentence = "檔案:" + all_file[0][x] + "出現了未知的錯誤\n" + str(ex)
                    log.write(sentence)


def CG_mode(options):  # *生成對應的檔案夾名,並在檔案名後加上c或g進行區分
    print("CG mode start")
    all_file = PF.CG_put_csv_and_get_excel(options["csv_file"])
    for x in range(len(all_file[0])):
        try:
            print("transforming " + all_file[0][x])
            if "Experiment 1" in all_file[0][x]:  # 針對特例
                run = PC.CTE(all_file[0][x], options["old_setting_format"], all_file[1][x])
                run.transform()
            else:
                Frun = PC.SQ_FCTE(all_file[0][x], options["new_setting_format"], all_file[1][x])
                Frun.transform()
        except pd.errors.EmptyDataError:
            with open(options["log_file"], "a", encoding="utf-8") as log:
                sentence = "檔案:" + all_file[0][x] + "為空白,因此不能正確地轉為excel檔\n"
                log.write(sentence)
        except Exception as ex:
            with open(options["log_file"], "a", encoding="utf-8") as log:
                sentence = "檔案:" + all_file[0][x] + "出現了未知的錯誤: " + str(ex) + "\n"
                log.write(sentence)

        # 懶人測試法
        # try:
        #     run = PC.CTE(all_file[0][x],options["old_setting_format"],all_file[1][x])
        #     run.transform()
        # except :
        #     try:
        #         Frun = PC.SQ_FCTE(all_file[0][x],options["new_setting_format"],all_file[1][x])
        #         Frun.transform()
        #     except pd.errors.EmptyDataError:
        #         with open (options["log_file"],"a",encoding="utf-8") as log:
        #             sentence = "檔案:" + all_file[0][x] + "為空白,因此不能正確地轉為excel檔\n"
        #             log.write(sentence)
        #     except Exception as ex:
        #         with open (options["log_file"],"a",encoding="utf-8") as log:
        #             sentence = "檔案:" + all_file[0][x] + "出現了未知的錯誤: " + str(ex) + "\n"
        #             log.write(sentence)


def test_mode(options):
    print("Test mode start")

    def running():
        all_file = PF.CG_put_csv_and_get_excel(options["csv_file"])
        for x in range(len(all_file[0])):
            try:
                run = PC.CTE(all_file[0][x], options["old_setting_format"], all_file[1][x])
                run.test()
            except Exception as ex:
                print(str(ex))
    # running()


def reformatG_mode(options):
    print("reformat mode start")
    all_file = PF.get_reformat_G_file(options["excel_file"])
    for x in range(len(all_file)):
        # try:
        for z in range(len(all_file[x][1])):
            print(f"reformat: {all_file[x][1][z]}")
            run = PR.RG(all_file[x][0][z], options, all_file[x][1][z])
            run.transform()
        # except Exception as ex:
        #     print(str(ex))
    # 以main.py為起點
    # q = "./excel/Experiment 2/25c_req.xlsx "
    # j = "./config/F_excel_setting.json"
    # g = "./excel/Experiment 2/25g.xlsx"
    # A = PR.RG(q, j, g)
    # A.transform()
