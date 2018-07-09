# -*- coding: utf-8 -*-
import os
import sys
import time
import datetime
import pandas as pd
from utils import headers


cur_dir = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today()
today = TODAY.strftime("%Y%m%d")

db_dir = os.path.join(cur_dir, 'db')
if not os.path.exists(db_dir):
    os.mkdir(db_dir)


def split_csv_files(date):
    csv_dir = os.path.join(cur_dir, date)
    if not os.path.exists(csv_dir):
        print("The directory {} does not exist".format(csv_dir))
        return False

    date_db_dir = os.path.join(db_dir, date)
    if not os.path.exists(date_db_dir):
        os.makedirs(date_db_dir)

    for csv_file in os.listdir(csv_dir):
        csv_path = os.path.join(csv_dir, csv_file)
        tick = pd.read_csv(csv_path, names=headers).drop_duplicates()
        codes = list(set(tick.code))
        for code in codes:
            t = tick[tick.code == code]
            t_path = os.path.join(date_db_dir, code + '.csv')
            t.to_csv(t_path, index=0)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        date = today
    else:
        date = sys.argv[1]
    start  = time.time()
    split_csv_files(date)
    print time.time() - start