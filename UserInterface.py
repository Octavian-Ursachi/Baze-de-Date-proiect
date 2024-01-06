from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from DBManager import DBManager
import sys


class Ui(QMainWindow, DBManager):
    def __init__(self):
        super(DBManager, self).__init__()
        super(Ui, self).__init__()

        uic.loadUi('UI/BD.ui', self)

        self.buttons = {
            'intersections' :  self.findChild(QPushButton, 'intersection_b'),
            'traffic_lanes': self.findChild(QPushButton, 'lanes_b'),
            'vehicles': self.findChild(QPushButton, 'vehicles_b'),
            'weather_conditions': self.findChild(QPushButton, 'weather_b'),
            'events': self.findChild(QPushButton, 'events_b'),
            'add_row' : self.findChild(QPushButton, 'add_row_b'),
            'commit' : self.findChild(QPushButton, 'commit_b'),
            'delete_row' : self.findChild(QPushButton, 'delete_row_b'),
            'drop' : self.findChild(QPushButton, 'drop_b')
        }
        self.buttons['intersections'].clicked.connect(self.intersection_b_clicked)
        self.buttons['traffic_lanes'].clicked.connect(self.lanes_b_clicked)
        self.buttons['vehicles'].clicked.connect(self.vehicles_b_clicked)
        self.buttons['weather_conditions'].clicked.connect(self.weather_b_clicked)
        self.buttons['events'].clicked.connect(self.events_b_clicked)
        self.buttons['add_row'].clicked.connect(self.add_row)
        self.buttons['commit'].clicked.connect(self.commit)
        self.buttons['delete_row'].clicked.connect(self.delete_row)
        self.buttons['drop'].clicked.connect(self.drop)

        self.tables = {
            'intersections': ['intersection_id', 'intersection_name', 'intersection_location', 'traffic_control_type', 'maximum_speed_limit'],
            'traffic_lanes': ['lane_id', 'lane_type', 'traffic_direction', 'intersection_id'],
            'vehicles': ['vehicle_id', 'vehicle_type', 'speed', 'direction', 'intersection_id'],
            'weather_conditions':  ['intersection_id', 'temperature', 'precipitation', 'wind_speed'],
            'events': ['event_id', 'event_type', 'event_description', 'event_time', 'intersection_id']
        }
        self.loadedTable = 'intersections'
        # conexiunea la baza de date
        # self.connect(user='bd042', password='bd042', host='bd-dc.cs.tuiasi.ro', port='1539')
        self.localConnect(user='PROIECT_BD', password='123', hostport="localhost:1521")
        self.import_tabel()
        self.show()

    def load_columns(self):
        widgetTabel = self.findChild(QTableWidget, 'Database_table')
        widgetTabel.setColumnCount(len(self.tables[self.loadedTable]))
        for index in range(0, len(self.tables[self.loadedTable])):
            widgetTabel.setHorizontalHeaderItem(index, QTableWidgetItem(str(self.tables[self.loadedTable][index])))

    def import_tabel(self):
        tabel = self.get_table(self.loadedTable)
        self.load_columns()
        if len(tabel) != 0:
            table_events = self.findChild(QTableWidget, 'Database_table')
            table_events.setColumnCount(len(tabel[0]))
            table_events.setRowCount(len(tabel))
            for i in range(len(tabel)):
                for j in range(len(tabel[0])):
                    item = QTableWidgetItem(str(tabel[i][j]))
                    item.setForeground(QBrush(QColor(255, 255, 255)))
                    table_events.setItem(i, j, item)
        else:
            table_events = self.findChild(QTableWidget, 'Database_table')
            table_events.clearContents()
            while table_events.rowCount() > 0:
                table_events.removeRow(0)

    def intersection_b_clicked(self):
        print("Loading table Intersections")
        # schimbare stare interna
        self.loadedTable = 'intersections'
        # incarcare linii din baza de date
        self.import_tabel()
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Intersections')

    def lanes_b_clicked(self):
        print("Loading table Traffic Lanes")
        self.loadedTable = 'traffic_lanes'
        self.import_tabel()
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Traffic Lanes')

    def vehicles_b_clicked(self):
        print("Loading table Vehicles")
        self.loadedTable = 'vehicles'
        self.import_tabel()
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Vehicles')

    def weather_b_clicked(self):
        print("Loading table Weather Conditions")
        self.loadedTable = 'weather_conditions'
        self.import_tabel()
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Weather Conditions')

    def events_b_clicked(self):
        print("Loading table Events")
        self.loadedTable = 'events'
        self.import_tabel()
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Events')

    def drop(self):
        print('dropping changes!')

    def delete_row(self):
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget()
        table = parent_widget.findChild(QTableWidget)
        # table.removeRow(table.currentRow())
        for coloana in range(0, table.columnCount()):
            item = table.item(table.currentRow(), coloana)
            if item is not None:
                item.setForeground(QBrush(QColor(255, 0, 0)))

    def add_row(self):
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget()
        table = parent_widget.findChild(QTableWidget)
        # adaugare rand
        table.insertRow(table.rowCount())
        # generare automata primary key pentru toate tabelele mai putin weather conditions
        if self.loadedTable != 'weather_conditions':
            lista_index = list()
            for i in range(0, table.rowCount()):
                itemTabel = table.item(i, 0)
                if itemTabel is not None:
                    primary_key = int(itemTabel.text())
                    lista_index.append(primary_key)
            if len(lista_index) > 0:
                minindex = -1
                lista_index.sort()
                print(lista_index)
                for i in lista_index:
                    if minindex < i and i-minindex <= 1:
                        minindex = i
                minindex += 1
            else:
                minindex = 0
            item = QTableWidgetItem(str(minindex))
            item.setForeground(QBrush(QColor(0, 255, 0)))
            table.setItem(table.rowCount()-1, 0, item)

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