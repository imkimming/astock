# -*- coding: utf-8 -*-
import sys
import time
import datetime
import pandas as pd
from utils import get_stock_df


up_down = [u'↑', '=', u'↓']
stat_headers = ['code', 'prev_close', 'st_open', 'st_price', 'high', 'low', 'up_vol', 'down_vol', 'up_money', 'down_money', 'up_mean', 'down_mean', 't_mean', 'st_vol', 'turnover', 'sh_prev_close', 'sh_ind', 'date']


def safe_div(x, y):
    if y == 0:
        return 0
    else:
        return '%.3f' % (x / y)


def merge_tick(code, date):
    st = get_stock_df(code, date)
    sh = get_stock_df('sh000001', date)
    
    st = st[['open', 'prev_close', 'price', 'high', 'low', 'bid1', 'volumn', 'turnover', 'time']]
    sh = sh[['price', 'prev_close', 'time']]

    sh.rename(columns={'price': 'sh_ind', 'prev_close': 'sh_prev_close'}, inplace=True)
    
    st = pd.merge(st, sh, how='left')
    st.fillna(method='bfill', inplace=True)
    st.fillna(method='ffill', inplace=True)
    return st


def replay_tick(code, date, interval=1, is_output=True):
    tick = merge_tick(code, date)
    tick = tick.set_index('time')
    tick = tick.sort_index()

    last_price, last_vol, last_bid1 = 0.0, 0, 0.0
    last_sh_ind, is_down_now = 0.0, 0
    sh_is_down, sh_is_down_now = 0, 0
    up_vol, down_vol = 0, 0
    up_money, down_money = 0, 0
    up_mean, down_mean, t_mean = 0.0, 0.0, 0.0
    last_money, cnt = 0.0, 0

    for index, row in tick.iterrows():
        st_price, st_vol, turnover = row['price'], row['volumn'], row['turnover']
        st_bid1, prev_close, vol_chg = row['bid1'], row['prev_close'], st_vol - last_vol

        sh_ind, sh_prev_close = row['sh_ind'], row['sh_prev_close']
        high, low, st_open = row['high'], row['low'], row['open']

        if last_price == 0.0:
            last_price, last_vol, last_bid1 = st_price, st_vol, st_bid1
            last_sh_ind, last_money = sh_ind, turnover
            continue
        else:
                if st_price > prev_close:
                    is_down = 0
                elif st_price == prev_close:
                    is_down = 1
                else:
                    is_down = 2
                if (st_price > last_price) or (st_price > last_bid1):
                    is_down_now = 0
                else:
                    is_down_now = 2

                if sh_ind > sh_prev_close:
                    sh_is_down = 0
                elif sh_ind == sh_prev_close:
                    sh_is_down = 1
                else:
                    sh_is_down = 2
                if sh_ind > last_sh_ind:
                    sh_is_down_now = 0
                elif sh_ind == last_sh_ind:
                    sh_is_down_now = 1
                else:
                    sh_is_down_now = 2

        if st_vol > last_vol:
            if not is_down_now:
                up_vol += vol_chg
                up_money += turnover - last_money
            else:
                down_vol += vol_chg
                down_money += turnover - last_money

            s_price = up_down[is_down] + str(st_price)
            chg_rate = '%.2f%%' % ((st_price - prev_close) / prev_close * 100)
            s_vol_chg = up_down[is_down_now] + str(vol_chg / 100)
            s_up_vol, s_down_vol, s_vol = up_vol / 100, down_vol / 100, st_vol / 100
            up_mean, down_mean, t_mean = safe_div(up_money, up_vol), safe_div(down_money, down_vol), safe_div(turnover, st_vol)
            s_sh_ind = up_down[sh_is_down] + str(sh_ind) + up_down[sh_is_down_now]
            
            if is_output:
                output = '  %-8s%-10s%-8s%-10s%-10s%-12s%-10s%-10s%-10s%-16s%-12s'
                output = output % (s_price, chg_rate, s_vol_chg, s_up_vol, s_down_vol, s_vol, up_mean, down_mean, t_mean, s_sh_ind, index)
                print output
                print
                cnt += 1
                if cnt > 0 and (cnt % 5 == 0):
                    time.sleep(interval)
        last_price, last_vol, last_bid1 = st_price, st_vol, st_bid1
        last_sh_ind, last_money = sh_ind, turnover
    return [code, prev_close, st_open, st_price, high, low, up_vol, down_vol, up_money, down_money, up_mean, down_mean, t_mean, st_vol, turnover, sh_prev_close, sh_ind, date]


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python {} code date".format(sys.argv[0]))
        sys.exit()
    code = sys.argv[1]
    if len(sys.argv) > 2:
        date = sys.argv[2]
    else:
        date = datetime.date.today().strftime('%Y%m%d')
    if len(sys.argv) > 3:
        interval = int(sys.argv[3])
    else:
        interval = 2
    start = time.time()
    replay_tick(code, date, interval)
    print time.time() - start
     