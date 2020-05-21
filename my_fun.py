import configparser
import pathlib
# from PyQt5.QtWidgets import *
from PySide2.QtWidgets import *
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PySide2.QtSql import QSqlDatabase,QSqlQuery
import random
from datetime import timedelta,datetime

'''
1.需要安装pyodbc库连接access数据库(参考：https://github.com/mkleehammer/pyodbc/wiki)
2.需要下载驱动(https://www.microsoft.com/zh-CN/download/details.aspx?id=13255)

'''


class My_DB(object):

    def __init__(self, db_path):
        self.tb_name = {}
        self.db = ''
        # 连接数据库
        self.db = QSqlDatabase.addDatabase("QODBC")
        self.db.setDatabaseName(
            "DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};FIL={MS Access};DBQ=" + db_path)
        # db.setUserName('sa')
        self.db.setPassword('20121110')
        # 根据ok的值判断数据库是否连接成功
        # self.ok = db.open()
        if self.db.open():
            query = QSqlQuery(self.db)
            query.exec_(
                "SELECT LOGGER_SN, LOGGER_NAME,  CHONE_HIGH , CHONE_LOW,  CHTWO_HIGH, CHTWO_LOW FROM TO_LOGGER_INFO")
            while query.next():
                # if self.tb_name[query.value(0)]!='H201403057' and self.tb_name[query.value(0)]!='HT20143221':
                self.tb_name[query.value(0)] = (
                    query.value(1), query.value(2), query.value(3), query.value(4), query.value(5))
            del(self.tb_name['H201403057'])
            del(self.tb_name['HT20143221'])

    # 显示表
    def select_table(self):
        query = QSqlQuery(self.db)
        sql = (r'''SELECT LOGGER_SN, LOGGER_NAME,  CHONE_HIGH , CHONE_LOW,  CHTWO_HIGH, CHTWO_LOW 
                    FROM TO_LOGGER_INFO 
                    where LOGGER_SN in %s ORDER BY CHONE_HIGH,LOGGER_NAME '''
               % (str(tuple(self.tb_name.keys()))))
        query.exec_(sql)
        # print('显示表' + sql)
        # print(str(tuple(self.tb_name.keys())))
        return query

    # 删除数据
    def del_table(self):
        query = QSqlQuery(self.db)

        for key in self.tb_name.keys():
            # 不修改保温箱跟冷藏车的记录
            tb_sn = 'LOGS_' + key
            # del_sql = (r'''delete from %s
            #                             where  LOGS_TIME not in
            #                             (SELECT LOGS_TIME FROM %s where LOGS_TIME LIKE '%%:[03]0:00') and LOGS_TIME like '%s%%'
            #                         '''
            #            % (tb_sn, tb_sn, date))
            del_sql = f'''delete  FROM {tb_sn} where (LOGS_TIME LIKE '%:[!03][0-9]:00' OR LOGS_TIME LIKE '%:[03][1-9]:00')
                                            AND LOGS_TIME NOT LIKE '2019/7/3 %' and LOGS_TIME NOT LIKE '2020/4/21 %'
                                        '''
            print('删除数据：' + del_sql)
            value = query.exec_(del_sql)
        return value

    # 修改数据
    def up_table(self, start_date,end_date):
        query = QSqlQuery(self.db)
        for sn in self.tb_name.keys():

            tb_sn = 'LOGS_' + sn
            # one_high最高温度，one_low最低温度，two_high最高湿度,two_low最低湿度
            one_high = float(self.tb_name[sn][1])
            one_low = float(self.tb_name[sn][2])
            two_high = float(self.tb_name[sn][3])
            two_low = float(self.tb_name[sn][4])
            # 查询出温度大于或者小于范围 1 度的或者湿度大于、小于1%。
            sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO 
                                FROM {tb_sn} 
                                where  (LOGS_CHONE > {one_high + 1} or LOGS_CHONE < {one_low - 1} or LOGS_CHTWO > {two_high + 1} OR LOGS_CHTWO < {two_low - 1}) and LOGS_TIME between #{start_date}# and #{end_date}#'
                            '''
            if(query.exec_(sql)):
                print('修改所有表' + sql)
            q = QSqlQuery(self.db)
            j = 0
            while query.next():
                t = query.value(0).toString('yyyy/M/d h:mm:ss')
                one = float(query.value(1))
                two = float(query.value(2))
                # 温度超标
                if (one > one_high or one < one_low) and (two < two_high and two > two_low):
                    if abs(one_low - one) < abs(one_high - one):
                        sql = f"update {tb_sn} set LOGS_CHONE = {random.uniform(one_low, one_low + 2)} WHERE  LOGS_TIME = #{t}#"
                        q.exec_(sql)
                        print(sql)
                    else:
                        sql = f"update {tb_sn} set LOGS_CHONE = {random.uniform(one_high - 1, one_high)} WHERE  LOGS_TIME = #{t}#"
                        q.exec_(sql)
                        print(sql)
                # 湿度超标
                elif (one < one_high and one > one_low) and (two > two_high or two < two_low):
                    if abs(one_low - one) < abs(one_high - one):
                        sql = f"update {tb_sn} set LOGS_CHTWO = {random.uniform(two_low, two_low + 2)} WHERE  LOGS_TIME = #{t}#"
                        q.exec_(sql)
                        print(sql)
                    else:
                        sql = f"update {tb_sn} set LOGS_CHTWO = {random.uniform(two_high - 1, two_high)} WHERE  LOGS_TIME = #{t}#"
                        q.exec_(sql)
                        print(sql)
                        # print(r"update %s set LOGS_CHTWO = %s WHERE  LOGS_TIME like '%s%%'" % (tb_sn, random.uniform(two_high-4, two_high), t))
            # # 修改成功后删除修改过的库
            # self.tb_name.pop(self.sel_name)

    # 显示超标数据
    def show_data(self, SN, start_date,end_date):
        tb_sn = 'LOGS_' + SN
        query = QSqlQuery(self.db)

        # sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO 
        #                     FROM {tb_sn} 
        #                     where  (LOGS_CHONE >= {self.tb_name[SN][1]} or LOGS_CHONE <= {self.tb_name[SN][2]} or LOGS_CHTWO>={ self.tb_name[SN][3]} or LOGS_CHTWO<={ self.tb_name[SN][4]} ) 
        #                     and LOGS_TIME between #{start_date}# and #{end_date}#
        #                     ORDER BY LOGS_TIME
        #                 '''

        sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO 
                            FROM {tb_sn} 
                            where   LOGS_TIME between #{start_date}# and #{end_date}#
                            ORDER BY LOGS_TIME
                        '''
        query.exec_(sql)
        # print('显示超标数据' + sql)
        return query

    # 详细修改数据
    def up_data(self, tb, high, logs_time, x):
        query = QSqlQuery(self.db)
        if x == 'one':
            sql = (r'''update %s set LOGS_CHONE=%s
                        where LOGS_TIME like '%s%%'
                    '''
                   % (tb, high, logs_time)
                   )
            # print('修改详细温度：' + sql)
            query.exec_(sql)
        elif x == 'two':
            sql = (r'''update %s set LOGS_CHTWO=%s
                                    where LOGS_TIME like '%s%%'
                                '''
                   % (tb, high, logs_time)
                   )
            # print('修改详细湿度：' + sql)
            query.exec_(sql)

    # 插入数据
    def ins_tb(self,start_date,end_date):
        q_list = []
        for key in self.tb_name.keys():
            tb_sn = 'LOGS_' + key
            query = QSqlQuery(self.db)

            sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO, LOGS_CHTHREE, LOGS_CHFOUR, BAT_DC_STATE FROM {tb_sn} 
                        where LOGS_TIME > #{start_date}# AND LOGS_TIME < #{end_date}#
                                        ORDER BY LOGS_TIME;
                                    '''
            query.exec_(sql)
        #     q_list.append(query)
        #     print(sql)
        # return q_list


            # 如果这个时间段没有数据，就insert数据
            if not query.next():
                # print(self.tb_name[sn][0], self.f_dt(start_time), self.f_dt(end_time))
                # self.myinsert(tb_sn, start_time, end_time)
                print(f'{self.tb_name[key][0]}没有数据,开始写入数据……')
                self.myinsert(tb_sn,start_date,end_date)
            else:
                print(tb_sn,self.tb_name[key][0],query.value('LOGS_TIME').toPython().strftime('%Y/%#m/%d %H:%M'))


    # 查询出没有数据的前一天的数据
    def myinsert(self, tb_sn, start_date, end_date):
        # timedelta用于计算日期，查询出来前一天的数据，然后把日期修改成后一天，最好写入到数据库
        start_date = datetime.strptime(start_date,'%Y/%m/%d %H:%M:%S') - timedelta(days=2)
        end_date = datetime.strptime(end_date,'%Y/%m/%d %H:%M:%S') - timedelta(days=2)
        query = QSqlQuery(self.db)
        # print(f"插入函数初始化{id(query)}")
        sql = f'''SELECT LOGS_TIME, LOGS_CHONE, LOGS_CHTWO, LOGS_CHTHREE, LOGS_CHFOUR, BAT_DC_STATE FROM {tb_sn} where LOGS_TIME > #{start_date}# AND LOGS_TIME < #{end_date}#'''
        
        print(sql)
        query.exec_(sql)

        while query.next():
            # print('开始插入')
            # print(query.value(0))
            LOGS_TIME = query.value('LOGS_TIME').toPython() + timedelta(days=1)
            q = QSqlQuery()
            sql = f'''INSERT INTO {tb_sn} (LOGS_TIME, LOGS_CHONE, LOGS_CHTWO, LOGS_CHTHREE, LOGS_CHFOUR, BAT_DC_STATE)
                        VALUES(#{LOGS_TIME}#,{query.value('LOGS_CHONE')},{query.value('LOGS_CHTWO')},{query.value('LOGS_CHTHREE')},{query.value('LOGS_CHFOUR')},{query.value('BAT_DC_STATE')})'''

            # 把数据的日期加一天，insert数据
            print(sql)
            q.exec_(sql)
        print('数据写入完毕！')
            # print(query.exec_(sql))


    def chaobiao(self, sn, one, two):
        one_high = self.tb_name[sn][1]
        one_low = self.tb_name[sn][2]
        two_high = self.tb_name[sn][3]
        two_low = self.tb_name[sn][4]
        if (one > one_high or one < one_low) and (two < two_high and two > two_low):
            print('温度超标')
        elif (one < one_high and one > one_low) and (two > two_high or two < two_low):
            print('湿度')


# if __name__ == '__main__':
#     my = My_DB(r"D:\tomonitor8.mdb")
#     aaa = my.ins_tb('2020/5/9 1:00','2020/5/9 9:00')


