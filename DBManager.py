import cx_Oracle


class DBManager:
    def __init__(self,user, password, host, port):
        print("Connecting to database")
        self.con = cx_Oracle.connect(user + '/' + password + '@' + host + ':' + port + '/orcl')
        print("Connected!")
        self.cur = self.con.cursor()

    def get_intersection(self):
        self.cur.execute('SELECT * FROM intersection')
        for row in self.cur:
            intersection = row
        return intersection

    def get_lanes(self):
        self.cur.execute('SELECT * FROM traffic_lanes')
        lanes = []
        for row in self.cur:
            lanes.append(row)
        return lanes

    def get_vehicles(self):
        self.cur.execute('SELECT * FROM vehicles')
        vehicles = []
        for row in self.cur:
            vehicles.append(row)
        return vehicles

    def get_weather(self):
        self.cur.execute('SELECT * FROM weather_conditions')
        for row in self.cur:
            weather = row
        return weather

    def get_events(self):
        self.cur.execute('SELECT * FROM i_events')
        events = []
        for row in self.cur:
            events.append(row)
        return events