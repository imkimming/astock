# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
from replay_tick import replay_tick, stat_headers

cur_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(cur_dir, 'db')
stat_dir = os.path.join(cur_dir, 'stat')
date_stat_dir = os.path.join(stat_dir, 'date')
code_stat_dir = os.path.join(stat_dir, 'code')
if not os.path.exists(date_stat_dir):
    os.makedirs(date_stat_dir)
if not os.path.exists(code_stat_dir):
    os.makedirs(code_stat_dir)


def gen_all_stat(date):
    date_dir = os.path.join(db_dir, date)
    if not os.path.exists(date_dir):
        print "The directory {} does not exist".format(date_dir)
        sys.exit()
    date_stat_path = os.path.join(date_stat_dir, '{}.csv'.format(date))
    with open(date_stat_path, 'w+') as f:
        f.write(','.join(stat_headers) + '\n')
        code_files = os.listdir(date_dir)
        for code_file in code_files:
            code = code_file.split('.')[0]
            res =replay_tick(code, date, is_output=False)
            res = [str(x) for x in res]
            f.write(','.join(res) + '\n')
            code_stat_path = os.path.join(code_stat_dir, '{}.csv'.format(code))
            if not os.path.exists(code_stat_path):
                with open(code_stat_path, 'w+') as f_code:
                    f_code.write(','.join(stat_headers) + '\n')
            with open(code_stat_path, 'a+') as f_code:
                f_code.write(','.join(res) + '\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        date = datetime.date.today().strftime('%Y%m%d')
    else:
        date = sys.argv[1]
    start = time.time()
    gen_all_stat(date)
    print("Used time: {}s".format(time.time() - start))