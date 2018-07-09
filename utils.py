# -*- coding: utf-8 -*-
import os
import sys
import datetime
import pandas as pd
import tushare as ts


TODAY = datetime.date.today()
today = TODAY.strftime('%Y%m%d')
cur_dir = os.path.dirname(os.path.abspath(__file__))
db_dir = os.path.join(cur_dir, 'db')
stat_dir = os.path.join(cur_dir, 'stat')
date_stat_dir = os.path.join(stat_dir, 'date')
code_stat_dir = os.path.join(stat_dir, 'code')

headers = ['code', 'name', 'open', 'prev_close', 'price', 'high',
          'low', 'bid1', 'ask1', 'volumn', 'turnover', 'bid_vol_1',
          'bid_price_1', 'bid_vol_2', 'bid_price_2', 'bid_vol_3', 'bid_price_3', 'bid_vol_4', 'bid_price_4', 'bid_vol_5', 'bid_price_5',
          'ask_vol_1', 'ask_price_1', 'ask_vol_2', 'ask_price_2', 'ask_vol_3', 'ask_price_3', 'ask_vol_4', 'ask_price_4', 'ask_vol_5',
          'ask_price_5', 'date', 'time', 'sub_time']


def get_stock_df(code, date=None):
    if not date:
        date = TODAY.strftime('%Y%m%d')
    csv_dir = os.path.join(db_dir, date)
    csv_file = os.path.join(csv_dir, code + '.csv')
    if not os.path.exists(csv_file):
        print("The file {} does not exist".format(csv_file))
        sys.exit()
    return pd.read_csv(csv_file).sort_values(['volumn', 'time'])


def get_all_stock_codes():
    stock_info = ts.get_stock_basics()
    stock_code = stock_info.index.tolist()
    for i in range(len(stock_code)):
        if stock_code[i] == '000001' or stock_code[i].startswith('6'):
            stock_code[i] = 'sh' + stock_code[i]
        else:
            stock_code[i] = 'sz' + stock_code[i]
    return stock_code


def get_stat_by_date(date=today):
    file_path = os.path.join(date_stat_dir, '{}.csv'.format(date))
    if not os.path.exists(file_path):
        print("The file {} does not exist".format(file_path))
        sys.exit()
    return pd.read_csv(file_path)


def get_stat_by_code(code):
    file_path = os.path.join(code_stat_dir, '{}.csv'.format(code))
    if not os.path.exists(file_path):
        print("The file {} does not exist".format(file_path))
        sys.exit()
    return pd.read_csv(file_path)
    