import cx_Oracle
global con
global cur


def disconectare():
    global con, cur
    print("Disconectare")
    cur.close()
    con.close()


class DBManager:
    def __init__(self):
        self.con = None
        self.cur = None

    def connect(self,user, password, host, port):
        global con, cur
        print("Connecting to database")
        self.con = cx_Oracle.connect(user + '/' + password + '@' + host + ':' + port + '/orcl')
        con = self.con
        self.cur = self.con.cursor()
        cur = self.cur
        print("Connected!")

    def localConnect(self, user, password, hostport):
        global con, cur
        print("Connecting to database")
        self.con = cx_Oracle.connect(user=user, password=password, dsn=hostport, encoding="UTF-8")
        con = self.con
        self.cur = self.con.cursor()
        cur = self.cur
        print("Connected!")

    def get_table(self, table_name):
        self.cur.execute('SELECT * FROM {table_name}'.format(table_name=table_name))
        tabel = []
        # print('SELECT * FROM {table_name}'.format(table_name=table_name))
        for row in self.cur:
            tabel.append(row)
        return tabel

