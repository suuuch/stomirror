# coding: utf-8
'''
CREATE USER shaw WITH PASSWORD '123456';
CREATE DATABASE shawdb OWNER shaw;
GRANT ALL PRIVILEGES ON DATABASE shawdb to shaw;

'''


from sqlalchemy import create_engine
Engine=create_engine("postgresql://shaw:123456@127.0.0.1:5432/shawdb")

class pg_conn(object):
    def __init__(self):
        # 数据库连接
        self.conn = psycopg2.connect(host='127.0.0.1',
                                     user='shaw',
                                     password='123456',
                                     database='shawdb')

        self.cur = self.conn.cursor()

    def get_conn(self):
        return self.conn

    def get_cur(self):
        return self.cur

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()
