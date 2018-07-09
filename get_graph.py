# -*- coding: utf-8 -*-
import os
import time
import urllib2
import datetime
from multiprocessing import Process
from utils import get_all_stock_codes


cur_dir = os.path.dirname(os.path.abspath(__file__))
graph_dir = os.path.join(cur_dir, 'graph')
monthly_graph_dir = os.path.join(graph_dir, 'monthly')
weekly_graph_dir = os.path.join(graph_dir, 'weekly')
daily_graph_dir = os.path.join(graph_dir, 'daily')
min_graph_dir = os.path.join(graph_dir, 'min')

TODAY = datetime.date.today()
today_min_graph_dir = os.path.join(min_graph_dir, TODAY.strftime('%Y%m%d'))

graph_dirs = {
    'min': today_min_graph_dir,
    'daily': daily_graph_dir,
    'weekly': weekly_graph_dir,
    'monthly': monthly_graph_dir
}

for g_dir in graph_dirs.values():
    if not os.path.exists(g_dir):
        os.makedirs(g_dir)

base_graph_url = "http://image.sinajs.cn/newchart/{}/n/{}.gif"   # type: min|daily, code: sh600015


def get_graph_data(codes, graph_type='min'):
    for code in codes:
        url = base_graph_url.format(graph_type, code)
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            data= response.read()
            img_path = os.path.join(graph_dirs[graph_type], '{}.gif'.format(code))
            with open(img_path, 'wb+') as f:
                f.write(data)
        except Exception, e:
            print graph_type, code, e
            continue


def get_graph():
    codes = get_all_stock_codes()
    p = []
    for g_type in graph_dirs.keys():
        t = Process(target=get_graph_data, args=(codes, g_type))
        p.append(t)
    for t in p:
        t.start()
    for t in p:
        t.join()


if __name__ == '__main__':
    start = time.time()
    get_graph()
    print("Used time: {}s".format(time.time() - start))
        