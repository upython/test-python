# coding:utf8
import MySQLdb
import conf


class SQLdb:
    def get_connection(self):
        try:
            conn = MySQLdb.connect(host=conf.db_host,
                                   user=conf.db_user,
                                   passwd=conf.db_password,
                                   db=conf.db_name,
                                   port=conf.db_port,
                                   charset=conf.db_charset)
            cursor = conn.cursor()
            return conn, cursor
        except Exception, e:
            return False
