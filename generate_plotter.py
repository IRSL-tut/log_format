#/usr/bin/env python3

import sys

if __name__ == '__main__':
    fname = 'log.csv'
    if len(sys.argv) > 1:
        fname = sys.argv[1]

    print('parsing file: {}'.format(fname))

    fname_prefix = '.'.join( fname.split('.')[0:-1] )

    f = open(fname)
    header = f.readline()
    headerlst = header.split(',')
    prefix_set = set()

    for title in headerlst:
        t = title.split('_')
        if len(t) > 2:
            prefix = '_'.join(t[0:-1])
            if not prefix in  prefix_set:
                prefix_set.add(prefix)
        elif len(t) > 1:
            prefix = t[0]
            if not prefix in  prefix_set:
                prefix_set.add(prefix)

    prefix_file_index_map = {}
    for prefix in prefix_set:
        lst=[]
        for idx, h in enumerate(headerlst):
            if prefix in h:
                lst.append(idx)
        if len(lst) > 0:
            prefix_file_index_map[prefix] = (open('{}.{}'.format(fname_prefix, prefix), mode='w'), lst)

    ## write header
    # for prefix, (ff, index) in prefix_file_index_map.items():
    #     ff.write('## ')
    #     ff.write( index[0] )
    #     for ii in index[1:]:
    #         ff.write(', ')
    #         ff.write( headerlst[ii] )

    ## read data
    line = f.readline()
    while line:
        line = line.strip()
        ## data parse
        data = line.split(',')
        tm = data[0]
        # print(len(data))
        for prefix, (ff, index) in prefix_file_index_map.items():
            ff.write(tm)
            for i in index:
                ff.write(' ')
                d = data[i]
                if len(d) == 0:
                  ff.write('0')
                else:
                  ff.write(data[i])
            ff.write('\n')
        ## next data
        line = f.readline()

    ## closing
    f.close()
    for prefix, (ff, index) in prefix_file_index_map.items():
        ff.close()
