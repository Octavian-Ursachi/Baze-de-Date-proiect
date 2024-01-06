import cx_Oracle


class DBManager:
    def __init__(self):
        self.con = None
        self.cur = None

    def connect(self,user, password, host, port):
        print("Connecting to database")
        self.con = cx_Oracle.connect(user + '/' + password + '@' + host + ':' + port + '/orcl')
        self.cur = self.con.cursor()
        print("Connected!")

    def localConnect(self, user, password, hostport):
        print("Connecting to database")
        self.con = cx_Oracle.connect(user=user, password=password, dsn=hostport, encoding="UTF-8")
        self.cur = self.con.cursor()
        print("Connected!")

    def get_table(self, table_name):
        self.cur.execute('SELECT * FROM {table_name}'.format(table_name=table_name))
        tabel = []
        # print('SELECT * FROM {table_name}'.format(table_name=table_name))
        for row in self.cur:
            tabel.append(row)
        return tabel
