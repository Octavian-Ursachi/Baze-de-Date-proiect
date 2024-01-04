from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from DBManager import DBManager
import sys

class Ui(QMainWindow, DBManager):
    def __init__(self):
        super(DBManager, self).__init__()
        super(Ui, self).__init__(user='bd042', password='bd042', host='bd-dc.cs.tuiasi.ro', port='1539')

        uic.loadUi('.venv/UI/BD.ui', self)


        self.intersection_b = {
            'page' :  self.findChild(QPushButton, 'intersection_b'),
            'add_row' : self.findChild(QPushButton, 'add_row_bi'),
            'commit' : self.findChild(QPushButton, 'commit_bi')
        }
        self.lanes_b = {
            'page' : self.findChild(QPushButton, 'lanes_b'),
            'add_row' : self.findChild(QPushButton, 'add_row_bl'),
            'commit' : self.findChild(QPushButton, 'commit_bl')
        }
        self.vehicles_b = {
            'page' : self.findChild(QPushButton, 'vehicles_b'),
            'add_row' : self.findChild(QPushButton, 'add_row_bv'),
            'commit' : self.findChild(QPushButton, 'commit_bv')
        }
        self.weather_b = {
            'page' : self.findChild(QPushButton, 'weather_b'),
            'add_row' : self.findChild(QPushButton, 'add_row_bw'),
            'commit' : self.findChild(QPushButton, 'commit_bw')
        }
        self.events_b = {
            'page' : self.findChild(QPushButton, 'events_b'),
            'add_row' : self.findChild(QPushButton, 'add_row_be'),
            'commit' : self.findChild(QPushButton, 'commit_be')
        }

        self.intersection_b['page'].clicked.connect(self.intersection_b_clicked)
        self.lanes_b['page'].clicked.connect(self.lanes_b_clicked)
        self.vehicles_b['page'].clicked.connect(self.vehicles_b_clicked)
        self.weather_b['page'].clicked.connect(self.weather_b_clicked)
        self.events_b['page'].clicked.connect(self.events_b_clicked)

        self.intersection_b['add_row'].clicked.connect(self.add_row)
        self.lanes_b['add_row'].clicked.connect(self.add_row)
        self.vehicles_b['add_row'].clicked.connect(self.add_row)
        self.weather_b['add_row'].clicked.connect(self.add_row)
        self.events_b['add_row'].clicked.connect(self.add_row)

        self.intersection_b['commit'].clicked.connect(self.commit)
        self.lanes_b['commit'].clicked.connect(self.commit)
        self.vehicles_b['commit'].clicked.connect(self.commit)
        self.weather_b['commit'].clicked.connect(self.commit)
        self.events_b['commit'].clicked.connect(self.commit)

        self.stackedWidget = self.findChild(QStackedWidget, 'stackedWidget')
        self.import_db()
        self.show()

    def import_db(self):
        self.import_intersection()
        self.import_lanes()
        self.import_vehicles()
        self.import_weather()
        self.import_events()

    def import_intersection(self):
        intersection = self.get_intersection()
        if intersection != 0:
            table_intersection = self.findChild(QTableWidget, 'table_intersection')
            table_intersection.setColumnCount(len(intersection))
            table_intersection.setRowCount(1)
            for i in range(len(intersection)):
                item = QTableWidgetItem(str(intersection[i]))
                item.setForeground(QBrush(QColor(255, 255, 255)))
                table_intersection.setItem(0, i, item)
            
    def import_lanes(self):
        lanes = self.get_lanes()
        if len(lanes) != 0:
            table_lanes = self.findChild(QTableWidget, 'table_lanes')
            table_lanes.setColumnCount(len(lanes[0]))
            table_lanes.setRowCount(len(lanes))
            for i in range(len(lanes)):
                for j in range(len(lanes[0])):
                    item = QTableWidgetItem(str(lanes[i][j]))
                    item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_lanes.setItem(i, j, item)


    def import_vehicles(self):
        vehicles = self.get_vehicles()
        if len(vehicles) != 0:
            table_vehicles = self.findChild(QTableWidget, 'table_vehicles')
            table_vehicles.setColumnCount(len(vehicles[0]))
            table_vehicles.setRowCount(len(vehicles))
            for i in range(len(vehicles)):
                for j in range(len(vehicles[0])):
                    item = QTableWidgetItem(str(vehicles[i][j]))
                    item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_vehicles.setItem(i, j, item)

    def import_weather(self):
        weather = self.get_weather()
        if weather != 0:
            table_weather = self.findChild(QTableWidget, 'table_weather')
            table_weather.setColumnCount(len(weather))
            table_weather.setRowCount(1)
            for i in range(len(weather)):
                item = QTableWidgetItem(str(weather[i]))
                item.setForeground(QBrush(QColor(255, 255, 255)))
                table_weather.setItem(0, i, item)

    def import_events(self):
        events = self.get_events()
        if len(events) != 0:
            table_events = self.findChild(QTableWidget, 'table_events')
            table_events.setColumnCount(len(events[0]))
            table_events.setRowCount(len(events))
            for i in range(len(events)):
                for j in range(len(events[0])):
                    item = QTableWidgetItem(str(events[i][j]))
                    item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_events.setItem(i, j, item)

    def intersection_b_clicked(self):
        self.stackedWidget.setCurrentIndex(0)

    def lanes_b_clicked(self):
        self.stackedWidget.setCurrentIndex(1)

    def vehicles_b_clicked(self):
        self.stackedWidget.setCurrentIndex(2)

    def weather_b_clicked(self):
        self.stackedWidget.setCurrentIndex(3)

    def events_b_clicked(self):
        self.stackedWidget.setCurrentIndex(4)

    def add_row(self):
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget()
        table = parent_widget.findChild(QTableWidget)
        table.insertRow(table.rowCount())

    def commit(self):
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget()
        label = sender_button.parentWidget().parentWidget().findChild(QLabel)
        table = parent_widget.findChild(QTableWidget)
        data = []
        new_data = []
        rows = []

        # data for inserting
        table_name = label.text().lower()
        new_rows = []
        fields = []

        for col in range(table.columnCount()):
            fields.append(table.horizontalHeaderItem(col).text())
        for row in range(table.rowCount()):
            for col in range(table.columnCount()):
                try:
                    item = table.item(row, col)
                    text = item.text()
                    data.append(text)
                    color = self.get_text_color(item).getRgb()
                    if color == (0, 0, 0, 255):
                        new_data.append(text)
                except:
                    new_data.append('')
                    data.append("None")
            rows.append(tuple(data))
            new_rows.append(tuple(new_data))
            data = []
            new_data = []

        # momentan pentru ca o linie sa fie valida pentru a fi inserata trebuie sa aiba valori nenule pentru fiecare element
        for row in new_rows:
            if '' in row:
                print('Invalid row')
                break

        new_rows, fields = self.prepare_data(new_rows, fields)
        commands = []
        for i in range(len(new_rows)):
            commands.append("INSERT INTO {}({}) VALUES ({})".format(table_name,fields,new_rows[i]))
        for command in commands:
            try:
                print(command)
                self.cur.execute(command)
                if 1: # poate un pop-up (Atentie, sigur doriti sa modificati?)
                    self.cur.execute('commit')
                print('Insert Complete!')
            except Exception as e:
                print(e)


    def prepare_data(self,rows,fields):
        filtered_rows = [tup for tup in rows if tup]
        field_str = ''
        row_str = ''
        rows = []
        for tup in filtered_rows:
            for elem in tup:
                if elem.isdigit():
                    row_str += elem + ','
                else:
                    row_str += "'" + elem + "',"
            rows.append(row_str[:-1])
            row_str = ''
        print(rows)

        for elem in fields:
            field_str += elem + ','
        field_str = field_str[:-1]

        return rows,field_str

    def get_text_color(self, table_item):
        if table_item is not None:
            brush = table_item.foreground()
            text_color = brush.color()
            return text_color
        else:
            return None
