# -*- coding: utf-8 -*-
import os
import datetime
import functools
import pandas as pd
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app, redirect
)


bp = Blueprint('stat', __name__, url_prefix='/')


def get_stat_by_date(date):
    file_path = os.path.join(current_app.config['DATE_STAT_DIR'], '{}.csv'.format(date))
    if not os.path.exists(file_path):
        return pd.DataFrame()
    return pd.read_csv(file_path)


def get_stat_by_code(code):
    file_path = os.path.join(current_app.config['CODE_STAT_DIR'], '{}.csv'.format(code))
    if not os.path.exists(file_path):
        return pd.DataFrame()
    return pd.read_csv(file_path)


def get_default_date():
    d = datetime.date.today()
    file_dir = current_app.config['DATE_STAT_DIR']
    cnt = 0
    date = 'no'
    while cnt < 100:
        date = d.strftime('%Y%m%d')
        if not os.path.exists(os.path.join(file_dir, '{}.csv').format(date)):
            d = d - datetime.timedelta(days=1)
            cnt += 1
        else:
            break
    return date


@bp.route('/')
@bp.route('/<int:date>/stat/')
def index(date=0):
    if date == 0:
        date = get_default_date()
        redirect(url_for('stat.index', date=int(date)))
    else:
        date = str(date)
    data = get_stat_by_date(date)
    if data.empty:
        return "Not found"

    data = data.query('st_price > 0 and st_vol > 0')
    data['chg'] = data.eval('(st_price - prev_close) / prev_close * 100')
    data['high'] = data.eval('(high - prev_close) / prev_close * 100')
    data['low'] = data.eval('(low - prev_close) / prev_close * 100')
    data['up_vol'] = data.eval('up_vol / 100')
    data['down_vol'] = data.eval('down_vol / 100')
    data['st_vol'] = data.eval('st_vol / 100')
    select_cols = ['code', 'prev_close', 'st_open', 'st_price', 'chg', 'high', 'low', 'up_vol', 'down_vol', 'st_vol', 'up_mean', 'down_mean', 't_mean']
    
    data = data[select_cols]
    if request.args.get('type') == 'raise':
        data = data.sort_values('chg', ascending=False)
    elif request.args.get('type') == 'fall':
        data = data.sort_values('chg')
    elif request.args.get('type') == 'wave':
        data = data.query('high > 1 and low < -1')
        data = data.dropna()
    elif request.args.get('type') == 'buy':
        data = data.query('(down_vol) > 0 and (up_vol / down_vol> 1.5) and (chg > -3)')
        data = data.dropna()
        data['buy_rate'] = data.eval('up_vol / down_vol')
        data = data.sort_values('buy_rate', ascending=False)
        data = data.drop('buy_rate', axis=1)

    if request.args.get('type') not in ['wave', 'buy']:
        data = data.loc[:100, :]
    return render_template('stat/stat.html', data=data)


@bp.route('/code/<code>/stat/')
def code_stat(code):
    data = get_stat_by_code(code)
    if data.empty:
        return "Not found"

    data = data.sort_index(ascending=False)
    data['chg'] = data.eval('(st_price - prev_close) / prev_close * 100')
    data['high'] = data.eval('(high - prev_close) / prev_close * 100')
    data['low'] = data.eval('(low - prev_close) / prev_close * 100')
    data['up_vol'] = data.eval('up_vol / 100')
    data['down_vol'] = data.eval('down_vol / 100')
    data['st_vol'] = data.eval('st_vol / 100')
    select_cols = ['date', 'prev_close', 'st_open', 'st_price', 'chg', 'high', 'low', 'up_vol', 'down_vol', 'st_vol', 'up_mean', 'down_mean', 't_mean', 'sh_ind', 'sh_prev_close']
    return render_template('stat/code_stat.html', data=data[select_cols], code=code)