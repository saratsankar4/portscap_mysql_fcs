import datetime
import pandas as pd
import os, inspect

from datetime import datetime, time
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.sql import text as sa_text
import time
from datetime import date
# ========LOGGER MANAGEMENT==============
import glob
import logging
logger = logging.getLogger('raw_logger')


# ========INITIALIZE DB CONNECTIONS=============
def start_engine(conf):
    try:
        # Read DB details from config file
        param_dict = conf

        certi_path=r'C:\Users\Admin\Documents\sarat\Tools\Portescap-ssl'

        engine_string = "postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
            user=param_dict['user'],
            password=param_dict['password'],
            host=param_dict['host'],
            port=param_dict['port'],
            database=param_dict['database'],
        )

        ssl_args = dict(options = '-csearch_path={}'.format('quality') , sslmode = "verify-ca" ,
                        sslcert =f"{certi_path}""//client-cert.pem", sslkey = f"{certi_path}""//client-key.pem" ,
                        sslrootcert = f"{certi_path}""//ca-cert.pem")

        engine = create_engine(
            engine_string,
            connect_args=ssl_args)

        return engine
    except Exception as e:
        # traceback.print_exc()
        logger.exception('Exception occured in Connecting to DB :%s', e)

# =======READ DATA FROM DB=============


def read_from_db(sql_query, conf):
    try:
        # Connect to DB and read data from DB
        engine = start_engine(conf)
        print(sql_query)
        df = pd.read_sql_query(sql_query, engine)
        logger.info("Reading tables")
        engine.dispose()
    except Exception as e:
        logger.exception('Exception occured while reading data from DB :%s', e)
        df = pd.DataFrame()
    return df


# ========STORE DATA TO DB=============


def save_to_db(db_table, operation, conf, input_df):
    try:
        # Connect to DB and store data in DB
        if operation == 'update':
            batchqr = input_df['batchqr'][0]
            engine = start_engine(conf)
            que = "Update " + db_table + " set batchqr = " + "'" + str(batchqr) + "'" + " where batchqr is null"

            engine.execute(sa_text(que).execution_options(autocommit=True))
            logger.info("Updated Table {}".format(db_table))
            engine.dispose()

        else:
            engine = start_engine(conf)
            input_df.to_sql(db_table,con=engine, if_exists=operation, index=False)
            engine.dispose()
            logger.info("{} table {}".format(operation,db_table))
    except Exception as e:
        logger.exception('Exception occured while storing data in DB :%s', e)
