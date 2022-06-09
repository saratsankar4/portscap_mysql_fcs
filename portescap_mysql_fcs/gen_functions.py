from config import config as cfg
from db_connection import read_from_db, save_to_db
from mysqldb_connection import read_from_mysqldb, save_to_mysqldb
import os, os.path
import numpy as np
import pandas as pd
from datetime import datetime, time
import schedule
import time


neewee_tab = cfg('neewee_tables')

mysql_tab = cfg('mysql_tables')

db_details = cfg('db')

mysqldb_details = cfg('mysql')


def get_batchqr(f_info):
    print(f_info['station_id'])
    b_qr = read_from_db("select id_work_order from production.work_order_batch wob "
                        "where wob.station_id = " + f_info['station_id'] +
                        " and wob.creation_date <= (select max(creation_date) from production.work_order_batch wo"
                        " where wo.station_id = " + f_info['station_id'] +
                        " and wo.creation_date <= " + f_info['timedate'] + " )", db_details)

    return b_qr['id_work_order'][0]


def update_details(neewee_info):
    df_nw = pd.DataFrame()
    df_mysql = pd.DataFrame()

    batchqr = get_batchqr(neewee_info)

    oprvalid = neewee_info['oprvalid'][0]

    df_nw = df_nw.append({'batchqr': batchqr}, ignore_index=True)

    df_mysql = df_mysql.append({'batchqr': batchqr, 'oprvalid': oprvalid}, ignore_index=True)

    save_to_db(neewee_tab['in4db_neewee'], "update", db_details, df_nw)

    save_to_mysqldb(mysql_tab['in4db_mysql'], "update", mysqldb_details, df_mysql)


def get_last_serial():
    mysql_df = read_from_mysqldb("select serialno from " + mysql_tab['testsystem1_mysql'] + " where serialno = "
                                 "(select serialno from " + mysql_tab['in4db_mysql'] + " where timedate = "
                                 "(select max(timedate) from " + mysql_tab['in4db_mysql'] + "))", mysqldb_details)

    return mysql_df['serialno'][0]


def get_all_serial():
    mysql_df = read_from_db("select distinct serialno from " + neewee_tab['testsystem1_neewee'], db_details)
    serial_list = mysql_df["serialno"].tolist()
    return serial_list


def check_update():
    serial_no = get_last_serial()
    serial_list = get_all_serial()
    print(serial_no, serial_list)
    if serial_no in serial_list:
        return False
    else:
        return True


def copy_latest_data():
    mysql_df = read_from_mysqldb("select * from " + mysql_tab['testsystem1_mysql'] + " where serialno = "
                                 "(select serialno from " + mysql_tab['in4db_mysql'] + " where timedate = "
                                 "(select max(timedate) from " + mysql_tab['in4db_mysql'] + "))", mysqldb_details)

    print(mysql_df.head())
    save_to_db(neewee_tab['testsystem1_neewee'], "append", db_details, mysql_df)

    save_to_mysqldb(mysql_tab['testsystem1_mysql'], "append", mysqldb_details, mysql_df)


def job():

    # files = os.listdir(str(folder_path))
    neewee_info = read_from_db("select * from " + neewee_tab['in4db_neewee'] + " where batchqr is null", db_details)
    mysql_info = read_from_mysqldb("select * from " + mysql_tab['in4db_mysql'] + " where batchqr is null",
                                   mysqldb_details)

    if neewee_info.shape[0] != 0 and mysql_info.shape[0] != 0:
        update_details(neewee_info)
        if check_update():
            copy_latest_data()

schedule.every(5).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(5-1)
