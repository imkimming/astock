# -*- coding: utf-8 -*-
import os
import datetime


TODAY = datetime.date.today()
today = TODAY.strftime('%Y%m%d')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, 'db')

STAT_DIR = os.path.join(BASE_DIR, 'stat')
DATE_STAT_DIR = os.path.join(STAT_DIR, 'date')
CODE_STAT_DIR = os.path.join(STAT_DIR, 'code')

GRAPH_DIR = os.path.join(BASE_DIR, 'graph')
MIN_GRAPH_DIR = os.path.join(GRAPH_DIR, 'min')
DAILY_GRAPH_DIR = os.path.join(GRAPH_DIR, 'daily')
WEEKLY_GRAPH_DIR = os.path.join(GRAPH_DIR, 'weekly')
MONTHLY_GRAPH_DIR = os.path.join(GRAPH_DIR, 'monthly')
GRAPH_DIRS = {
    'min': MIN_GRAPH_DIR,
    'daily': DAILY_GRAPH_DIR,
    'weekly': WEEKLY_GRAPH_DIR,
    'monthly': MONTHLY_GRAPH_DIR
}

BASE_TICK_URL = "http://hq.sinajs.cn/list="
IND_CODES = ['sh000001', 'sz399001']