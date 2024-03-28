import sys
import os
import mc_log_ui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import img2pdf
from PIL import Image # img2pdfと一緒にインストールされたPillowを使います
import shutil

def main(): 
    args = sys.argv
    log_path = None
    config_path = None
    if len(args) == 2:
        log_path = args[1]
        print(args[1])
    elif len(args) == 3:
        config_path = args[1]
        log_path = args[2]
        print("log " + log_path) # log file
        print("config " + config_path) # config file

    log = mc_log_ui.read_log(log_path)
    xyz = ["x", "y", "z"]
    wrench = ["fx", "fy", "fz", "cx", "cy", "cz"]
    joint = ["0" , "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
    logged_list = []

    centroidal_param = [
        "CentroidalManager_IRSL_LOG_ControlRobot_position",
        "CentroidalManager_IRSL_LOG_ControlRobot_orientation",
        "CentroidalManager_IRSL_LOG_RealRobot_position",
        "CentroidalManager_IRSL_LOG_RealRobot_orientation",
        "CentroidalManager_IRSL_LOG_PlannedRobot_dcm",
        "CentroidalManager_IRSL_LOG_RealRobot_dcm",
        "CentroidalManager_CoM_planned",
        "CentroidalManager_CoM_controlRobot",
        "CentroidalManager_CoM_realRobot_com",
        "CentroidalManager_CoM_realRobot_comVelocity",
        "CentroidalManager_CoM_realRobot_comAcceleration",
        "CentroidalManager_CoM_planned",
        "CentroidalManager_ZMP_ref",
        "CentroidalManager_ZMP_control",
        "CentroidalManager_ZMP_planned",
        "CentroidalManager_ZMP_measured",
    ]
    
    
    foottask_param = [
        "FootTask_Left_filteredMeasuredWrench",
        "FootTask_Right_filteredMeasuredWrench",
        "FootTask_Left_targetWrench",
        "FootTask_Right_targetWrench",
    ]

    footmanger_param = [
        "FootManager_supportPhase",
    ]

    qout_param = [
        "CentroidalManager_IRSL_LOG_ControlRobot_q",
        "CentroidalManager_IRSL_LOG_RealRobot_q",
    ]
    
    # add "x", "y", "z" to the logged_list
    for log_name in centroidal_param:
        for axis in xyz:
            logged_list.append(log_name + "_" + axis)

    # add "fx", "fy", "fz", "cx", "cy", "cz" to the logged_list
    for log_name in foottask_param:
        for axis in wrench:
            logged_list.append(log_name + "_" + axis)

    # add "supportPhase" to the logged_list
    for log_name in footmanger_param:
        logged_list.append(log_name)
        
    # add "qout" to the logged_list
    for log_name in qout_param:
        for joint_name in joint:
            logged_list.append(log_name + "_" + joint_name)
            
    #columns : logged_list
    #index : log["t"]
    df = pd.DataFrame(index=log["t"], columns=logged_list)

    #pandas.DataFrameにデータを格納
    for log_name in logged_list:
        df[log_name] = log[log_name]

    #データの保存先 / ファイル名
    file_name = (log_path.split('/')[-1]).strip(".bin")
    
    #データ用フォルダの作成
    if not os.path.isdir(file_name):
        os.mkdir(file_name)

    #データをcsvファイルに書き出し
    df.to_csv(file_name + "/" + file_name + ".csv")

    # #image用フォルダの作成
    # if not os.path.isdir(file_name + "/image"):
    #     os.mkdir(file_name + "/image")
    
    # #データをimageに書き出し    
    # for i in range(len(logged_list)):
    #     fig, ax = plt.subplots()
    #     ax.plot(df[logged_list[i]], "o-", markersize=0.1, color='Red')
    #     ax.set_title(logged_list[i])
    #     fig.tight_layout()
    #     fig.savefig(file_name + "/image/" + logged_list[i] + ".png")

    # pdf_path = file_name + "/" + file_name + ".pdf"
    # image_path = file_name + "/image/"
    # extension = ".png"

    # with open(pdf_path,"wb") as f:
    #     # 画像フォルダの中にあるPNGファイルを取得し配列に追加、バイナリ形式でファイルに書き込む
    #     f.write(img2pdf.convert([Image.open(image_path+j).filename for j in os.listdir(image_path)if j.endswith(extension)]))
    
    # binファイルのコピー
    shutil.copyfile(log_path,file_name + "/" + log_path.split('/')[-1])

    # configファイルをtextファイルにコピー
    if(config_path != None):
        shutil.copyfile(config_path,file_name + "/" + file_name + ".txt")
        
if __name__ == "__main__":
    main()
