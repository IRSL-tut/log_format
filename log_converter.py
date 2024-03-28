import sys
import os
import mc_log_ui
import argparse
import metayaml
import re
import numpy
import pandas as pd

def expand_str_to_list (input_str):
    parsed = re.match("([0-9]+)-([0-9]+)", input_str)
    if parsed:
        return range(int(parsed.group(1)),int(parsed.group(2))+1)
    else:
        return input_str

def main(): 
    # args
    parser = argparse.ArgumentParser(description='Convert data from mc_rtc log to hrpsys log')
    parser.add_argument('-f', type=str, help='input file', metavar='file', required=True)
    parser.add_argument('--plot', type=str, help='plot configure file', metavar='file')
    args = parser.parse_args()

    if args.plot is not None:
        plot_dict = metayaml.read(args.plot )

    #key : expand_str
    file_expand_name = plot_dict.keys()
    # print(file_expand_name)
        
    #import file name is log
    topic_list = {}
    for i in file_expand_name:
        topic_list[i] = (plot_dict[i]['data'][0]['log'])

    mc_rtc_log = mc_log_ui.read_log(args.f)
    for topic in topic_list.values():
        mc_rtc_keys = [key for key in mc_rtc_log.keys() if topic in key]
        if mc_rtc_keys:
            df = pd.DataFrame(index=mc_rtc_log["t"], columns=mc_rtc_keys)
            for key in mc_rtc_keys:
                df[key] = mc_rtc_log[key]
            df.to_csv(args.f.split('.')[0] + "." + topic , sep=' ', na_rep= 0)

if __name__ == "__main__":
    main()