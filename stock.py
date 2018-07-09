# -*- coding: utf-8 -*-
import os
import sys
import urllib2
import datetime
import tushare as ts


reload(sys)
sys.setdefaultencoding('utf-8')


base_url = "http://hq.sinajs.cn/list="
ind_codes = ['s_sh000001', 's_sz399001']
up_down = [u'↑', '=', u'↓']


def safe_div(x, y):
    if y == 0:
        return 0
    else:
        return '%.3f' % (x / y)


def get_tick_data(code_str):
    url = base_url + ','.join([code_str] + ind_codes)
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        data = response.read().strip()
        data = data.replace('";', '')
        return [x.split('"')[1] for x in data.splitlines()]
    except Exception, e:
        print e
        return []


def show_tick_data(code_str):
    file_path = code_str + '.csv'
    with open(file_path, 'w+') as f:
        last_price, last_vol, last_bid1 = 0.0, 0, 0.0
        last_sh_ind, last_sz_ind = 0.0, 0.0
        is_down, is_down_now = 0, 0
        sh_is_down, sh_is_down_now = 0, 0
        sz_is_down, sz_is_down_now = 0, 0
        up_vol, down_vol = 0, 0
        up_money, down_money = 0, 0
        last_money = 0.0
        while True:
            data = get_tick_data(code_str)
            if len(data) < 3:
                continue
            now_time = datetime.datetime.now().strftime('%H%M%S')
            st_items, sh_items, sz_items = [x.split(',') for x in data]

            st_price, st_vol, turnover = float(st_items[3]), int(st_items[8]), float(st_items[9])
            st_bid1, tick_time = float(st_items[6]), st_items[31]
            prev_close, vol_chg = float(st_items[2]), st_vol - last_vol

            if now_time.startswith('09') and tick_time.startswith('15'):
                continue
            if int(now_time) > 150300:
                break
            if st_vol == last_vol:
                continue
                
            sh_ind, sh_chg = float(sh_items[1]), float(sh_items[2])
            sz_ind, sz_chg = float(sz_items[1]), float(sz_items[2])

            if last_price == 0.0:
                last_price, last_vol, last_bid1 = st_price, st_vol, st_bid1
                last_sh_ind, last_sz_ind = sh_ind, sz_ind
                last_money = turnover
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
                
                if sh_chg > 0.0:
                    sh_is_down = 0
                elif sh_chg == 0.0:
                    sh_is_down = 1
                else:
                    sh_is_down = 2
                if sh_ind > last_sh_ind:
                    sh_is_down_now = 0
                elif sh_ind == last_sh_ind:
                    sh_is_down_now = 1
                else:
                    sh_is_down_now = 2

                if sz_chg > 0.0:
                    sz_is_down = 0
                elif sz_chg == 0.0:
                    sz_is_down = 1
                else:
                    sz_is_down = 2
                if sz_ind > last_sz_ind:
                    sz_is_down_now = 0
                elif sz_ind == last_sz_ind:
                    sz_is_down_now = 1
                else:
                    sz_is_down_now = 2

            # header = ['price', 'chg_rate', 'vol_chg', 'up_vol', 'down_vol',
            #           'vol', 'up_mean', 'down_mean', 'mean', 'sh_ind', 'sz_ind', 'time']
            # print st_vol, last_vol, tick_time
            if st_vol > last_vol:
                line = ','.join(st_items).decode('gbk').encode('utf-8')
                f.write(line + '\n')

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
                s_sz_ind = up_down[sz_is_down] + str(sz_ind) + up_down[sz_is_down_now]
                output = '  %-8s%-10s%-8s%-10s%-10s%-12s%-10s%-10s%-10s%-16s%-16s%-12s'
                output = output % (s_price, chg_rate, s_vol_chg, s_up_vol, s_down_vol, s_vol, up_mean, down_mean, t_mean, s_sh_ind, s_sz_ind, tick_time)
                print output
                print 

            last_price, last_vol, last_bid1 = st_price, st_vol, st_bid1
            last_sh_ind, last_sz_ind, last_money = sh_ind, sz_ind, turnover


if __name__ == '__main__':
    if len(sys.argv) < 2:
        code = 'sz002455'
    else:
        code = sys.argv[1]
    codes = ts.get_stock_basics().index.tolist()
    if code[2:] not in codes:
        print "Please input one correct stock code"
        sys.exit()
    show_tick_data(code)
