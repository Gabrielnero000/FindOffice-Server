from multiprocessing import Lock

import mysql.connector
from mysql.connector import errorcode
from loguru import logger
import sys
import fire
import os

from backend.db.tables import TABLES

DB_USER = os.environ.get('DB_USER', 'findoffice')
DB_PWD = os.environ.get('DB_PWD', 'findoffice')
DB_NAME = os.environ.get('DB_NAME', 'findoffice')


class Database:
    __instance = None

    @staticmethod
    def getInstance():
        if Database.__instance is None:
            Database()
        return Database.__instance


    def __init__(self):
        if Database.__instance is not None:
            raise Exception('Database must be unique')
        else:
            self.__createConnection()
            self.__setupDatabase()
            self.__setupTables()
            Database.__instance = self


    def __createConnection(self):
        try:
            self._connection = mysql.connector.connect(
                host='localhost',
                user=DB_USER,
                password=DB_NAME,
            )
        except mysql.connector.Error as err:
            logger.error(f"Failed to connect to SQL:\n{err}")
            sys.exit(-1)


    def __createDatabase(self, cursor):
        try:
            cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            logger.error(f"Failed creating database:\n{err}")
            sys.exit(-1)


    def __setupDatabase(self):
        cursor = self._connection.cursor(buffered=True)
        try:
            logger.info(f"Using database '{DB_NAME}'")
            cursor.execute(f"USE {DB_NAME}")
        except mysql.connector.Error as err:
            logger.warning(f"Database '{DB_NAME}' does not exists")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                logger.info(f"Trying to create database '{DB_NAME}'")
                self.__createDatabase(cursor)
                logger.info(f"Database '{DB_NAME}' created")
                self._connection.database = DB_NAME

    
    def __setupTables(self):
        cursor = self._connection.cursor(buffered=True)
        for table_name, table_description in TABLES.items():
            try:
                logger.info(f"Creating table '{table_name}'")
                cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    logger.info(f"Table '{table_name}' already exists")
                else:
                    logger.error(f"Failed to create table '{table_name}'\n{err.msg}")

    
    def getCursor(self):
        return self._connection.cursor(dictionary=True)

    def commit(self):
        self._connection.commit()