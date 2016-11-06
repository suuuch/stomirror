# coding: utf-8
'''
CREATE USER shaw WITH PASSWORD '123456';
CREATE DATABASE shawdb OWNER shaw;
GRANT ALL PRIVILEGES ON DATABASE shawdb to shaw;

'''

import psycopg2
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


    def exec_with_select(self, sql):
        self.cur.execute(sql)
        return self.cur

    def exec_with_commit(self,sql):
        self.cur.execute(sql)
        self.conn.commit()
        return self.cur.rowcount

    def __del__(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    sql = 'SELECT * FROM investment.t_163_item WHERE group_id = \'主要财务指标\''
    db = pg_conn()
    print(db.exec_with_select(sql))

