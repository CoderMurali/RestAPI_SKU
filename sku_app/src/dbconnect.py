# -*- coding: utf-8 -*-
"""
Created on Sat Jun 05 10:06:23 2021

@author: muraikv
"""
import pymysql
import logging
import pandas as pd

class Database(object):
    def __init__(self):
        self.db_config = {
            'MYSQL_HOST': 'skudatabase-dev.codj82jzwtpe.us-east-2.rds.amazonaws.com',
            'MYSQL_DATABASE': 'SKudata',
            'MYSQL_USER': 'devuser',
            'MYSQL_PASS': 'devuser@123',
            'MYSQL_PORT': 3306,
            'MYSQL_DRIVER': 'MySQL ODBC 3.51 Driver'
        }
        self.db = None
        self.cursor = ''

    def connect(self):
        try:
            self.db = pymysql.connect(host=self.db_config['MYSQL_HOST'],
                                      port=self.db_config['MYSQL_PORT'],
                                      database=self.db_config['MYSQL_DATABASE'],
                                      user=self.db_config['MYSQL_USER'],
                                      passwd=self.db_config['MYSQL_PASS'])

            self.cursor = self.db.cursor()
            logging.info("Connection Established  !")
        except pymysql.InternalError as e:
            logging.error(e)
            self.db.close()
        except Exception as e:
            logging.error(e)
            self.db.close()

    def disconnect(self):
        self.db.close()

    def execute(self, query):
        if self.db is None:
            self.connect()
        curs = self.cursor
        try:
            curs.execute(query)
            logging.info("Query Executed  !")
            return curs
        except Exception as e:
            logging.error(e)
            self.db.close()


    def exe_modiy(self, query, params):
        """Executes sql scripts to change the db which include Changes,Updates,and Deletes
               """
        if self.db is None:
            self.connect()
        try:
            curs = self.cursor
            res = curs.execute(query, args=params)
            """ Commit your changes in the database """
            self.db.commit()
            logging.info("Query Executed  !")
            return res
        except pymysql.IntegrityError as e:
            self.db.rollback()
            msg = 'Data integrity issue'
            return msg
        except Exception as e:
            """
            Error
            """
            logging.info(e)
            self.db.rollback()
            self.db.close()

    def read_sql(self, query):
        if self.db is None:
            self.connect()
        try:
            df_result = pd.read_sql(query, self.db)
            if df_result.empty:
                return None
            else:
                return df_result
        except Exception as e:
            logging.error("Read Exception: ", e)




