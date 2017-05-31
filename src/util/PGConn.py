#!/usr/bin/env python3
# coding: utf-8
# PGConn.py


import sys
import psycopg2


class PGConn:

    def __init__(self, dbhost, dbport, dbuser, dbpass, dbname, encoding):
        self.conn = psycopg2.connect(database=dbname, user=dbuser, password=dbpass, host=dbhost, port=dbport)
        self.conn.set_client_encoding(encoding)
        self.cur = self.conn.cursor()


    def cursor(self):
        return self.cur


    def create_table(self, tbname, tbsql):
        self.cur.execute("select exists (select 1 from pg_class where relname='%s')" % tbname);
        if not self.cur.fetchone()[0]:
            self.cur.execute(tbsql)
        self.conn.commit()


    # 检查记录是否存在
    def test_existence(self, tbsql):
        self.cur.execute("select exists (%s)" % tbsql);
        return self.cur.fetchone()[0]


    def execute(self, logger, sql):
        this_func_name = sys._getframe().f_code.co_name
        logger.info("%s(): start ..." % this_func_name)
        print(sql)
        logger.info("%s(): sql\t%s" % (this_func_name, sql))
        try:
            logger.debug("%s(): before execute() ..." % this_func_name)
            # 程序有可能在这里阻塞，一直不返回。
            self.cur.execute(sql)
            logger.debug("%s(): after execute() ..." % this_func_name)
        except psycopg2.DataError as e:
            logger.error("%s(): psycopg2.DataError\t%s\t%s" % (this_func_name, e.pgcode, e.pgerror))
        except psycopg2.IntegrityError as e:
            logger.error("%s(): psycopg2.IntegrityError\t%s\t%s" % (this_func_name, e.pgcode, e.pgerror))
        except psycopg2.DatabaseError as e:
            logger.error("%s(): psycopg2.DatabaseError\t%s\t%s" % (this_func_name, e.pgcode, e.pgerror))
        # rollback to savepoint savepoint_name 时，并没有对应的 savepoint_name
        # SQL 语句跟数据库表的 schema 不同
        except psycopg2.InternalError as e:
            logger.fatal("%s(): psycopg2.InternalError\t%s\t%s" % (this_func_name, e.pgcode, e.pgerror))
        # 致命错误，数据库系统在恢复模式中
        except psycopg2.OperationalError as e:
            logger.fatal("%s(): psycopg2.OperationalError\t%s\t%s" % (this_func_name, e.pgcode, e.pgerror))
        logger.info("%s(): end ..." % this_func_name)
        return


    def commit(self):
        self.conn.commit()


    def exec_commit(self, logger, sql):
        self.execute(logger, sql)
        self.commit()


    def close(self):
        self.commit()
        self.conn.close()




