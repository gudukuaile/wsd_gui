import pyodbc
from datetime import datetime, date,timedelta
import random
import time
import sched
import os
import sys
from pyodbc import ProgrammingError
import traceback
import logging
import signal

logging.basicConfig(filename='log.log')


class My_Wsd():
    def __init__(self, db_path):
        self.s = sched.scheduler(time.time, time.sleep)
        self.tb_name = {}
        self.conn_str = (
            r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
            r'DBQ=%s;'
            'UID=admin;PWD=20121110'
        ) % db_path
        try:
            self.cnxn = pyodbc.connect(self.conn_str)
        except pyodbc.Error as e:
            print(str(e))
            print('数据库连接失败，请检查数据库路径是否正确！')

            # 数据库连接失败，每隔20秒重新连接数据库，超过10次不成功，结束程序
            time.sleep(20)
            global count
            count += 1
            if count == 2:
                s = traceback.format_exc()
                logging.error(s)
                print('尝试连接次数过多，系统即将退出')
                sys.exit(0)
            run_fun()
            self.cursor = 0
        self.crsr = self.cnxn.cursor()
        sql = "SELECT LOGGER_SN, LOGGER_NAME,  CHONE_HIGH , CHONE_LOW,  CHTWO_HIGH, CHTWO_LOW FROM TO_LOGGER_INFO"

        for row in self.crsr.execute(sql):
            # tb_name[row[0]] = (row[1], row[2], row[3], row[4], row[5])
            self.tb_name[row.LOGGER_SN] = (
                row.LOGGER_NAME, row.CHONE_HIGH, row.CHONE_LOW, row.CHTWO_HIGH, row.CHTWO_LOW)
        del (self.tb_name['H201403057'])
        del (self.tb_name['HT20143221'])
        # self.crsr.close()
        # cnxn.close()

    # 删除数据
    def del_table(self):

        # 获取当前的日期
        dt = date.today()
        # date = ('%s/%s' % (d.year, d.month))
        d = f"{dt.year}/{dt.month}"
        try:
            for key in self.tb_name.keys():
                tb_sn = 'LOGS_'+key

                # 查询超标数据
                # sql = (r'''SELECT LOGS_TIME FROM %s where (LOGS_TIME LIKE '%%:[!03][0-9]:00' OR LOGS_TIME LIKE '%%:[03][1-9]:00')
                #             AND LOGS_TIME  LIKE '%s%%' AND LOGS_TIME NOT LIKE '2019/7/3 %%'
                #         '''
                #         % (tb_sn, d))

                # 删除超标数据
                del_sql = f'''delete  FROM {tb_sn} where (LOGS_TIME LIKE '%:[!03][0-9]:00' OR LOGS_TIME LIKE '%:[03][1-9]:00')
                                AND LOGS_TIME  LIKE '{d}%' AND LOGS_TIME NOT LIKE '2019/7/3 %' and LOGS_TIME NOT LIKE '2020/4/21 %' 
                            '''
                # print(del_sql)

                self.crsr.execute(del_sql)
                self.cnxn.commit()
                if self.crsr.rowcount > 0:
                    print(f"{key} {self.tb_name[key][0]} 已删除 {self.crsr.rowcount}\t条数据")
                # else:
                #     print(f'{key} {self.tb_name[key][0]} 没有可删除的数据！')

        except Exception as e:
            print(str(e))
            s = traceback.format_exc()
            logging.error(s)
            time.sleep(30)
            run_fun()
        
        # print('*'*10)
        # time.sleep(1)
        self.s.enter(120, 1, self.del_table)


    # 查询超标数据并修改数据
    def up_table(self, s_dt='', otherdate=('2019/7/3', '2020/4/21')):
        dt = date.today()
        # 不需要修改的时间
        otherdate = otherdate
        print('现在的时间是：%s' % self.f_dt(datetime.now()))
        # 如果给定了时间就使用给定的时间，否则使用当前的时间
        sdt = s_dt if s_dt else self.f_dt(dt)

        # 循环所有的table
        try:
            for sn in self.tb_name.keys():
                tb_sn = 'LOGS_' + sn
                # one_high最高温度，one_low最低温度，two_high最高湿度,two_low最低湿度
                name = self.tb_name[sn][0]
                one_high = float(self.tb_name[sn][1])
                one_low = float(self.tb_name[sn][2])
                two_high = float(self.tb_name[sn][3])
                two_low = float(self.tb_name[sn][4])
                # 查询出温度大于或者小于范围 1 度的或者湿度大于、小于1%。
                sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO FROM {tb_sn} 
                            where (LOGS_CHONE > {one_high + 0.1} or LOGS_CHONE < {one_low - 0.1} or LOGS_CHTWO > {two_high + 0.1} OR LOGS_CHTWO < {two_low - 0.1}) and LOGS_TIME like '{sdt}%'
                        '''
                self.crsr.execute(sql)
                rows = self.crsr.fetchall()

                # if len(rows)>0:
                #     print(f"{name}\t{len(rows)} \t {sql}")

                for row in rows:
                    # 实际温度
                    one = row.LOGS_CHONE
                    # 实际湿度
                    two = row.LOGS_CHTWO
                    # 超标时间
                    udt = row.LOGS_TIME

                    # year = dt.year
                    # month = dt.month
                    # day = dt.day

                    # 判断次时间是否是不需要修改数据的时间
                    odt = self.f_dt(udt.date())

                    # print('%s的最高温度是：%s，最低温度是：%s，最高湿度是：%s，最低湿度是：%s' % (self.tb_name[sn][0],one_high,one_low,two_high,two_low))
                    # print('现在的时间是：%s' % d.strftime(r'%Y/%m/%d %X'))
                    # 温度超标，湿度正常
                    if ((one > one_high or one < one_low) and odt not in otherdate):
                      # print(odt)
                      self.up_wendu(tb_sn, one, one_low, one_high, udt,name)
                    # 湿度超标
                    elif ((two > two_high or two < two_low) and odt not in otherdate):
                      # print(odt)
                      self.up_shidu(tb_sn, two, two_low, two_high,udt,name)
        except ProgrammingError as e:
            print(str(e))
            time.sleep(30)
            s = traceback.format_exc()
            logging.error(s)
            run_fun()
        # print("$"*10)
        self.s.enter(600, 2, self.up_table)

    # update温度，dt是datetime类型
    def up_wendu(self, tb_sn, one, one_low, one_high, udt,name):
        # 温度超标，湿度正常
        if abs(one_low - one) > abs(one_high - one):
            # print(one)
            sql = f'''update {tb_sn} set LOGS_CHONE = {random.uniform(one_high - 1, one_high)} WHERE  LOGS_TIME =  #{udt}#'''
            self.crsr.execute(sql)
            self.cnxn.commit()
            print(sql)
            # print(
            #     f"修改 {name}\t{self.f_dt(udt)} 的温度\t{one} 为\t{random.uniform(one_high - 1, one_high)} ")
        else:
            # print(one)
            sql = f'''update {tb_sn} set LOGS_CHONE = {random.uniform(one_low, one_low + 1)} WHERE  LOGS_TIME = #{udt}# '''
            self.crsr.execute(sql)
            self.cnxn.commit()
            print(sql)
            # print(
            #     f"修改 {name}\t{self.f_dt(udt)} 的温度\t{one} 为\t{random.uniform(one_low, one_low + 1)} ")


    # update湿度
    def up_shidu(self, tb_sn, two, two_low, two_high,udt,name):
        # 湿度超标
        if abs(two_low - two) > abs(two_high - two):
            # print(two)
            sql = f'''update {tb_sn} set LOGS_CHTWO = {random.uniform(two_high - 1, two_high)} WHERE  LOGS_TIME  = #{udt}# '''
            self.crsr.execute(sql)
            self.cnxn.commit()
            print(sql)
            # print(
            #     f"修改 {name}\t{self.f_dt(udt)} 的湿度\t{two} 为\t{random.uniform(two_high - 1, two_high)} ")
        else:
            # print(two)
            sql = f'''update {tb_sn} set LOGS_CHTWO = {random.uniform(two_low, two_low + 2)} WHERE  LOGS_TIME  = #{udt}# '''
            self.crsr.execute(sql)
            self.cnxn.commit()
            print(sql)
            # print(
            #     f"修改 {name}\t{self.f_dt(udt)} 的湿度\t{two} 为\t{random.uniform(two_low, two_low + 2)} ")

    # update二者
    def up_two(self, tb_sn, one, one_low, one_high, year, month, day, hour, minute):
        pass

    # 插入数据
    def insert_data(self, year, month, day, hour, minute, end_hour=8, end_minute=00, count_day=1, second=00):
        # 循环所有的table
        for sn in self.tb_name.keys():
            tb_sn = 'LOGS_' + sn
            start_time = datetime(
                year, month, day, hour, minute, second)
            # print(type(start_time))
            end_time = datetime(
                year, month, day + count_day, end_hour, end_minute, second)
            # 查询没有数据的时间段
            sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO, LOGS_CHTHREE, LOGS_CHFOUR, BAT_DC_STATE FROM {tb_sn} where LOGS_TIME between #{start_time}# and #{end_time}#'''

            rows = self.crsr.execute(sql).fetchall()
            # 如果这个时间段没有数据，就insert数据
            if not len(rows):
                # print(self.tb_name[sn][0], self.f_dt(start_time), self.f_dt(end_time))
                self.myinsert(tb_sn, start_time, end_time)
            else:
                for row in rows:
                    print(row)
            print('*' * 20)

    # 查询出没有数据的前一天的数据
    def myinsert(self, tb_sn, start_time, end_time):
        sql = (
            r'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO, LOGS_CHTHREE, LOGS_CHFOUR, BAT_DC_STATE FROM %s where LOGS_TIME > ? and LOGS_TIME < ?''' % tb_sn)
        rows = self.crsr.execute(sql, start_time - timedelta(days=1),
                                 end_time - timedelta(days=1)).fetchall()
        for row in rows:
            print(row[0] + timedelta(days=1))
            sql = (
                r'''INSERT INTO %s (LOGS_TIME, LOGS_CHONE, LOGS_CHTWO, LOGS_CHTHREE, LOGS_CHFOUR, BAT_DC_STATE) VALUES(?,?,?,?,?,?)''' % tb_sn)
            print(sql)
            # 把数据的日期加一天，insert数据
            self.crsr.execute(
                sql, row[0] + timedelta(days=1), row[1], row[2], row[3], row[4], row[5])
            self.cnxn.commit()

    # 查询数据
    def sel_table(self):
        for key in self.tb_name.keys():
            tb_sn = 'LOGS_'+key
            d = datetime.now()
            # date = ('%s/%s' % (d.year,d.month))
            date = ('%s/%s/%s' % (d.year, d.month, d.day))
            sql = (r'''select * from %s where  LOGS_TIME LIKE '2019/7/3' 
                     '''
                   % (tb_sn))
            self.crsr.execute(sql)
            print(sql)
            rows = self.crsr.fetchall()
            for row in rows:
                t = self.f_dt(row.LOGS_TIME)
                print(t)

    # 删除短信报警
    def del_sms(self):
        sql = '''
                SELECT ALARM_ID, LOGGER_NAME, LOGGER_SN, ALARM_MSG, MOBILE_NO, ALARM_CREATE_TIME, LAST_SEND_TIME, ALARM_STATE, ALARM_ACTION
                FROM TO_ALARMS_SMS
        '''
        for row in self.crsr.execute(sql):
            dt = row.ALARM_CREATE_TIME
            m = dt.minute
            if m % 2 != 0:
                print(row)

    # 格式化数据的时间,参数必须是datetime类型
    def f_dt(self, dt):
        # # 格式化日期的分秒
        # dt = datetime.strftime("%M:%S")
        # # 把日期转换成一个元祖
        # d = datetime.timetuple()
        # # 拼接日期格式
        # t = ('%s/%s/%s %s:%s' % (d.tm_year, d.tm_mon, d.tm_mday, d.tm_hour, dt))
        if isinstance(dt,datetime):
          t = dt.strftime("%Y/%#m/%#d %#H:%M:%S")
        elif isinstance(dt,date):
          t = dt.strftime("%Y/%#m/%#d")
        return t


def run_fun():
    wsd = My_Wsd(r"z:\tomonitor8.mdb")
    # print(wsd.tb_name)
    if len(wsd.tb_name):
        wsd.s.enter(3, 1, wsd.del_table)
        wsd.s.enter(3, 2, wsd.up_table, argument=('',))
        # wsd.s.enter(3, 2, wsd.up_table, argument=('2020',))
        try:
            wsd.s.run()
        except KeyboardInterrupt as e:
            print('正在关闭数据库连接，请稍等……')
            s = traceback.format_exc()
            logging.error(s)
            time.sleep(2)
            wsd.crsr.close()
            wsd.cnxn.close()

        # 插入丢失的数据，参数two_day 是截至时间的小时,count_day间隔日期。
        # wsd.insert_data(year=2019, month=8, day=11, hour=2, minute=00,end_hour=8,count_day=0)


if __name__ == '__main__':
    # sched版本定时器
    print('开始工作中……')
    # wsd = My_Wsd("H:\wsd.mdb")
    count = 0
    run_fun()


