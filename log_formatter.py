import sys
import mc_log_ui
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


def main(): 
    args = sys.argv
    if len(args) > 1:
        print(args[1])

    log = mc_log_ui.read_log(args[1])
    xyz = ["x", "y", "z"]
    wrench = ["fx", "fy", "fz", "cx", "cy", "cz"]

    logged_list = []

    centroidal_param = [
        "CentroidalManager_IRSL_LOG_ControlRobot_position",
        "CentroidalManager_IRSL_LOG_ControlRobot_orientation",
        "CentroidalManager_IRSL_LOG_RealRobot_position",
        "CentroidalManager_IRSL_LOG_RealRobot_orientation",
        "CentroidalManager_CoM_planned",
        "CentroidalManager_CoM_controlRobot",
        "CentroidalManager_CoM_realRobot",
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
    
    # add "x", "y", "z" to the logged_list
    for log_name in centroidal_param:
        for axis in xyz:
            logged_list.append(log_name + "_" + axis)

    # add "fx", "fy", "fz", "cx", "cy", "cz" to the logged_list
    for log_name in foottask_param:
        for axis in wrench:
            logged_list.append(log_name + "_" + axis)

    #columns : logged_list
    #index : log["t"]
    df = pd.DataFrame(index=log["t"], columns=logged_list)

    #pandas.DataFrameにデータを格納
    for log_name in logged_list:
        df[log_name] = log[log_name]

    #データをcsvファイルに書き出し
    file_name = (args[1].split('/')[-1]).strip(".bin")
    df.to_csv(file_name + ".csv")

    pdf = PdfPages(file_name + ".pdf")

    for i in range(len(logged_list)):
        fig, ax = plt.subplots()
        ax.plot(df[logged_list[i]], "o-", markersize=0.1, color='Red')
        ax.set_title(logged_list[i])
        fig.tight_layout()
        pdf.savefig(fig)
        
    pdf.close()

if __name__ == "__main__":
    main()
