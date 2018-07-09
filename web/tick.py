# -*- coding: utf-8 -*-
import os
import sys
import chardet
import urllib2
import datetime
import functools
import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
reload(sys)
sys.setdefaultencoding('utf-8')

bp = Blueprint('tick', __name__, url_prefix='/tick')


def get_tick_data(code_str):
    base_url = current_app.config['BASE_TICK_URL']
    ind_codes = current_app.config['IND_CODES']
    url = base_url + ','.join([code_str] + ind_codes)
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().strip()
        data = data.decode('gbk').encode('utf-8')
        data = data.replace('";', '')
        data = [x.split('"')[1] for x in data.splitlines()]
        data = [x.split(',') for x in data]
        return data
    except Exception, e:
        print e
        return []


def get_history_tick(code, date):
    data_dir = os.path.join(current_app.config['DB_DIR'], date)
    data_path = os.path.join(data_dir, '{}.csv'.format(code))
    if not os.path.exists(data_path):
        return pd.DataFrame()
    return pd.read_csv(data_path)


@bp.route('/<code>')
def real_time_tick(code):
    data = get_tick_data(code)
    if not data:
        return "Not Found"
    return render_template('tick/real_time_tick.html', data=data, t=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def up_or_down(row, flag=None):
    if not flag:
        if row['price'] > row['last_price'] or (row['price'] > row['last_bid_price_1'] and row['last_bid_price_1'] > 0):
            return 1
        elif row['price'] == row['last_price']:
            return 0
        return -1
    else:
        if row['up_down'] * flag > 0:
            return 1
        return 0


@bp.route('/<code>/<date>')
def history_tick(code, date):
    df = get_history_tick(code, date)
    if df.empty:
        return "No Data"
    df.drop_duplicates(['price', 'volumn'], inplace=True)
    df['last_price'] = df['price'].shift(1)
    df['vol_chg'] = df['volumn'] - df['volumn'].shift(1)
    df['money_chg'] = df['turnover'] - df['turnover'].shift(1)
    df['last_bid_price_1'] = df['bid_price_1'].shift(1)

    df.at[df.index[0], 'last_price'] = df.iloc[0]['prev_close']
    df.at[df.index[0], 'vol_chg'] = df.iloc[0]['volumn']
    df.at[df.index[0], 'money_chg'] = df.iloc[0]['turnover']
    df.at[df.index[0], 'last_bid_price_1'] = df.iloc[0]['ask_price_1']

    df['up_down'] = df.apply(lambda row: up_or_down(row), axis=1)
    df['is_up'] = df.apply(lambda row: up_or_down(row, 1), axis=1)
    df['is_down'] = df.apply(lambda row: up_or_down(row, -1), axis=1)

    df['up_vol'] = df.eval('vol_chg * is_up').cumsum()
    df['down_vol'] = df.eval('vol_chg * is_down').cumsum()
    df['up_mean'] = df.eval('money_chg * is_up').cumsum() / df['up_vol']
    df['down_mean'] = df.eval('money_chg * is_down').cumsum() / df['down_vol']
    df['t_mean'] = df.eval('turnover / volumn')
    df['chg'] = df.eval('(price - prev_close) / prev_close')
    df.fillna(0, inplace=True)

    cols = ['price', 'chg', 'vol_chg', 'up_vol', 'down_vol', 'volumn', 'up_mean', 'down_mean', 't_mean', 'ask_price_1','bid_price_1', 'time', 'up_down', 'ask_vol_1', 'bid_vol_1']
    return render_template('tick/history_tick.html', data=df[cols])
