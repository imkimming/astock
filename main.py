# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import datetime
from get_all_stock_tick import get_all_tick
from split_csv_files import split_csv_files
from process_tick import gen_all_stat
from get_graph import get_graph


cur_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(cur_dir, 'logs')
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logger = logging.getLogger('Stock')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
file_handler = logging.FileHandler(os.path.join(log_dir, 'stock.log'))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)


if __name__ == '__main__':
    today = datetime.date.today().strftime('%Y%m%d')
    logger.info("Start get_all_tick")
    get_all_tick()
    logger.info("Finish get_all_tick")

    logger.info("Start split_csv_files")
    start = time.time()
    split_csv_files(today)
    used_time = time.time() - start
    logger.info("Finish split_csv_files, used time: {}s".format(used_time))

    today_csv_dir = os.path.join(cur_dir, today)
    os.system('rm -rf {}'.format(today_csv_dir))
    logger.info("Delete the directory {}".format(today_csv_dir))

    logger.info("Start get_graph")
    start = time.time()
    get_graph()
    used_time = time.time() - start
    logger.info("Finish get_graph, used time: {}s".format(used_time))

    logger.info("Start process_tick")
    start = time.time()
    gen_all_stat(today)
    used_time = time.time() - start
    logger.info("Finish gen_all_stat, used time: {}s".format(used_time))

    db_dir = os.path.join(cur_dir, 'db')
    today_db_dir = os.path.join(db_dir, today)
    if os.path.exists(today_db_dir):
        logger.info("Start to compress csv files")
        start = time.time()
        cmd = "cd {} && tar -jcf {}.tar.bz2 {}".format(db_dir, today, today)
        os.system(cmd)
        os.system("rm -rf {}".format(today_db_dir))
        used_time = time.time() - start
        logger.info("Finish compressing csv files, used time: {}s".format(used_time))
