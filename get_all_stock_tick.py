# -*- coding: utf-8 -*-
import os
import sys
import time
import urllib2
import datetime
import tushare as ts
from multiprocessing import Pool, Process
from utils import get_all_stock_codes


base_url = "http://hq.sinajs.cn/list="
codes_per_process = 60
cur_dir = os.path.dirname(os.path.abspath(__file__))
TODAY = datetime.date.today()
today = TODAY.strftime('%Y%m%d')
csv_dir = os.path.join(cur_dir, today)


def get_tick_data(codes_str):
    url = base_url + codes_str
    try:
        request = urllib2.Request(url)
        reponse = urllib2.urlopen(request)
        data = reponse.read()
        data = data.replace('="', ',')
        data = data.replace('";', '')
        data = data.replace('var hq_str_', '')
        return data
    except Exception, e:
        print e
        return ''


def write_data(file_num, codes_str):
    prev_data = ''
    csv_file = 'tick_{}.csv'.format(file_num)
    with open(os.path.join(csv_dir, csv_file), 'w+') as f:
        while True:
            data = get_tick_data(codes_str)
            now = datetime.datetime.now()
            if int(now.strftime('%H%M')) >= 1503:
                break
            if prev_data == data:
                continue
            prev_data = data
            f.write(data.decode('gbk').encode('utf-8'))
            

def get_all_tick():
    now = datetime.datetime.now()
    if int(now.strftime('%H%M')) > 1503:
        print "The stock market has been closed"
        sys.exit()
    if not os.path.exists(csv_dir):
        os.mkdir(csv_dir)
    stock_codes = get_all_stock_codes()
    p_list = []
    for i in range((len(stock_codes) + codes_per_process - 1) / codes_per_process):
        codes = stock_codes[i * codes_per_process:(i + 1) *codes_per_process]
        codes_str = ','.join(codes)
        p = Process(target=write_data, args=(i, codes_str))
        p_list.append(p)
    for p in p_list:
        p.start()
    for p in p_list:
        p.join()

    return True


if __name__ == '__main__':
    get_all_tick()
