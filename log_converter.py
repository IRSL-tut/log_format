import sys
import os
import mc_log_ui
import argparse
import metayaml
import re
import pandas as pd


def has_duplicates(l):
    return len(l) != len(set(l))

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
    parser.add_argument('-d', type=str, help='output dir', metavar='file')
    parser.add_argument('-p', type=str, help='prefix', metavar='file')
    parser.add_argument('--plot', type=str, help='plot configure file', metavar='file')
    args = parser.parse_args()

    # load log file
    mc_rtc_log = mc_log_ui.read_log(args.f)

    # mc_rtc logのtopic名を取得
    topic_list = {}
    # mc_rtc topic list
    if args.plot:
        plot_dict = metayaml.read(args.plot)
        file_expand_name = plot_dict.keys()
        for i in file_expand_name:
            topic_list[plot_dict[i]['data'][0]['log']] = [key for key in mc_rtc_log.keys() if plot_dict[i]['data'][0]['log'] in key]
    else:
        for keys in mc_rtc_log.keys():
            key = keys.rsplit('_',1)
            if key[0] == 't':
                continue
            else:
                if key[0] in topic_list.keys():
                    topic_list[key[0]].append(keys)
                else:
                    topic_list[key[0]] = [keys]

    if args.p is None:
        prefix=args.f.split('.')[0]
    else:
        prefix = args.p
    if args.d is not None:
        prefix = args.d + '/' + prefix.split('/')[-1]

    df_list = {}
    for topic in topic_list.keys():
        df = pd.DataFrame(index=mc_rtc_log["t"], columns=topic_list[topic])
        for key in topic_list[topic]:
            if key in mc_rtc_log.keys():
                df[key] = mc_rtc_log[key]

        if not df.empty:
            df.to_csv(prefix + '.' + topic , sep=' ', na_rep= 0, index=True, header=False)
            df_list[topic] = df

if __name__ == "__main__":
    main()
