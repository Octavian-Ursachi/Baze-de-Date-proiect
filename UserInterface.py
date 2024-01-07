from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from DBManager import DBManager
from PyQt5 import QtCore
import sys
import teste


class Ui(QMainWindow, DBManager):
    def __init__(self):
        super(DBManager, self).__init__()
        super(Ui, self).__init__()

        uic.loadUi('UI/BD.ui', self)
        # referinte la elemente din interfata grafica
        self.widgetTabel = self.findChild(QTableWidget, 'Database_table')
        self.widgetForeignTabel = self.findChild(QTableWidget, 'Foreign_table')
        self.buttons = {
            'intersections':  self.findChild(QPushButton, 'intersection_b'),
            'traffic_lanes': self.findChild(QPushButton, 'lanes_b'),
            'vehicles': self.findChild(QPushButton, 'vehicles_b'),
            'weather_conditions': self.findChild(QPushButton, 'weather_b'),
            'events': self.findChild(QPushButton, 'events_b'),
            'add_row': self.findChild(QPushButton, 'add_row_b'),
            'commit': self.findChild(QPushButton, 'commit_b'),
            'delete_row': self.findChild(QPushButton, 'delete_row_b'),
            'drop': self.findChild(QPushButton, 'drop_b')
        }
        # conectarea callback-urilor de la referinte la functii
        self.buttons['intersections'].clicked.connect(self.intersection_b_clicked)
        self.buttons['traffic_lanes'].clicked.connect(self.lanes_b_clicked)
        self.buttons['vehicles'].clicked.connect(self.vehicles_b_clicked)
        self.buttons['weather_conditions'].clicked.connect(self.weather_b_clicked)
        self.buttons['events'].clicked.connect(self.events_b_clicked)
        self.buttons['add_row'].clicked.connect(self.add_row)
        self.buttons['commit'].clicked.connect(self.commit)
        self.buttons['delete_row'].clicked.connect(self.delete_row)
        self.buttons['drop'].clicked.connect(self.drop)
        self.widgetTabel.cellChanged.connect(self.test_valid_valoare)
        self.widgetTabel.cellClicked.connect(self.casuta_apasata)
        self.widgetForeignTabel.cellClicked.connect(self.foreign_key_selectat)
        self.column_names = {
            'intersections': ['intersection_id', 'intersection_name', 'intersection_location', 'traffic_control_type', 'maximum_speed_limit'],
            'traffic_lanes': ['lane_id', 'lane_type', 'traffic_direction', 'intersection_id'],
            'vehicles': ['vehicle_id', 'vehicle_type', 'speed', 'direction', 'lane_id'],
            'weather_conditions':  ['intersection_id', 'temperature', 'precipitation', 'wind_speed'],
            'i_events': ['event_id', 'event_type', 'event_description', 'event_time', 'intersection_id']
        }
        self.datatypes = {
            'intersections': ['numeric', 'varchar2', 'varchar2', 'varchar2', 'numeric'],
            'traffic_lanes': ['numeric', 'varchar2', 'varchar2', 'numeric'],
            'vehicles': ['numeric', 'varchar2', 'numeric', 'varchar2', 'numeric'],
            'weather_conditions': ['numeric', 'numeric', 'varchar2', 'numeric'],
            'i_events': ['numeric', 'event_type', 'varchar2', 'timestamp', 'numeric']
        }
        self.constrangeri = {
            'intersections': ['primary_key', '', '', '', ''],
            'traffic_lanes': ['primary_key', '', 'check', 'foreign_key'],
            'vehicles': ['primary_key', '', '', 'check', 'foreign_key'],
            'weather_conditions': ['foreign_key', '', '', ''],
            'i_events': ['primary_key', '', '', '', 'foreign_key']
        }
        self.loadedTable = 'intersections'
        self.loadingReady = True
        # conexiunea la baza de date
        # self.connect(user='bd042', password='bd042', host='bd-dc.cs.tuiasi.ro', port='1539')
        self.localConnect(user='PROIECT_BD', password='123', hostport="localhost:1521")
        # incarcare tabelul initial
        self.import_tabel(self.widgetTabel, self.loadedTable)
        self.show()

    def foreign_key_selectat(self, linie, coloana):
        foreign_id_selectat = self.widgetForeignTabel.item(linie, 0).text()
        print("A selectat foreign key-ul cu id-ul "+str(foreign_id_selectat))
        if foreign_id_selectat != self.widgetTabel.item(self.widgetTabel.currentRow(), self.widgetTabel.currentColumn()).text():
            item = QTableWidgetItem()
            item.setText(foreign_id_selectat)
            self.widgetTabel.setItem(self.widgetTabel.currentRow(), self.widgetTabel.currentColumn(), item)
        self.widgetForeignTabel.clear()
        self.widgetForeignTabel.setRowCount(0)
        self.widgetForeignTabel.setColumnCount(0)

    def test_valid_valoare(self, linie, coloana):
        if self.loadingReady is True:  # daca e false, se incarca din baza de date tabela, nu e nevoie de callback
            valoare_inserata = self.widgetTabel.item(linie, coloana)
            if valoare_inserata is not None:
                if teste.verifica_constrangeri(valoare_inserata.text(), self.constrangeri[self.loadedTable][coloana]):
                    print("Constrangeri ok")
                    if valoare_inserata.text() != '':
                        if teste.verifica_datatype(valoare_inserata.text(), self.datatypes[self.loadedTable][coloana]):
                            print("Tip de data bun")
                            item = self.widgetTabel.item(linie, coloana)
                            item.setBackground(QBrush(QColor(45, 45, 45)))
                            item.setForeground(QBrush(QColor(0, 255, 0)))
                        else:
                            print("Tip de data Rau")
                            item = self.widgetTabel.item(linie, coloana)
                            item.setBackground(QBrush(QColor(255, 0, 0)))
                    else:
                        print("Itemul e gol")
                else:
                    print("Constrangeri NOT ok")
                    item = self.widgetTabel.item(linie, coloana)
                    item.setBackground(QBrush(QColor(255, 0, 0)))
            else:
                if teste.verifica_constrangeri('', self.constrangeri[self.loadedTable][coloana]):
                    print("Nimic inserat")
                else:
                    print("Constrangeri not OK")
                    item = QTableWidgetItem()
                    item.setBackground(QBrush(QColor(255, 0, 0)))
                    self.widgetTabel.setItem(linie, coloana, item)

    def casuta_apasata(self, linie, coloana):
        # print("Casuta apasata la "+str(linie)+" "+str(coloana))
        if self.constrangeri[self.loadedTable][coloana] == 'foreign_key':
            # print("Deschidere selectie pentru foreign key")
            if self.loadedTable == 'traffic_lanes':
                print("Foreign key pentru Trafiic lanes")
                self.import_tabel(self.widgetForeignTabel, 'intersections')
                self.load_columns(self.widgetForeignTabel, 'intersections')

            elif self.loadedTable == 'vehicles':
                print("Foreign key pentru Vehicles")
                self.import_tabel(self.widgetForeignTabel, 'traffic_lanes')
                self.load_columns(self.widgetForeignTabel, 'traffic_lanes')
            elif self.loadedTable == 'weather_conditions':
                print("Foreign key pentru Weather")
                self.import_tabel(self.widgetForeignTabel, 'intersections')
                self.load_columns(self.widgetForeignTabel, 'intersections')
            elif self.loadedTable == 'i_events':
                print("Foreign key pentru events")
                self.import_tabel(self.widgetForeignTabel, 'intersections')
                self.load_columns(self.widgetForeignTabel, 'intersections')

    def load_columns(self, tabel, numeTabel):
        tabel.setColumnCount(len(self.column_names[numeTabel]))
        for index in range(0, len(self.column_names[numeTabel])):
            tabel.setHorizontalHeaderItem(index, QTableWidgetItem(str(self.column_names[numeTabel][index])))

    def import_tabel(self, tabel_destinatie, numeTabel):
        self.loadingReady = False
        tabel = self.get_table(numeTabel)
        # seteaza numele coloanelor
        self.load_columns(tabel_destinatie, numeTabel)
        if len(tabel) != 0:
            # table_events = self.findChild(QTableWidget, 'Database_table')
            tabel_destinatie.setColumnCount(len(tabel[0]))
            tabel_destinatie.setRowCount(len(tabel))
            for i in range(len(tabel)):
                for j in range(len(tabel[0])):
                    item = QTableWidgetItem(str(tabel[i][j]))
                    item.setForeground(QBrush(QColor(255, 255, 255)))
                    tabel_destinatie.setItem(i, j, item)
                    # constraint check pentru ca primary key sa fie nemodificabil
                    if self.constrangeri[numeTabel][j] == 'primary_key':
                        tabel_destinatie.item(i, j).setFlags(QtCore.Qt.NoItemFlags)
                        tabel_destinatie.item(i, j).setBackground(QBrush(QColor(15, 15, 15)))
        else:
            # table_events = self.findChild(QTableWidget, 'Database_table')
            tabel_destinatie.clearContents()
            while tabel_destinatie.rowCount() > 0:
                tabel_destinatie.removeRow(0)
        self.loadingReady = True

    def intersection_b_clicked(self):
        print("Loading table Intersections")
        # schimbare stare interna
        self.loadedTable = 'intersections'
        # incarcare linii din baza de date
        self.import_tabel(self.widgetTabel, self.loadedTable)
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Intersections')
        self.widgetForeignTabel.clear()
        self.widgetForeignTabel.setRowCount(0)
        self.widgetForeignTabel.setColumnCount(0)

    def lanes_b_clicked(self):
        print("Loading table Traffic Lanes")
        self.loadedTable = 'traffic_lanes'
        self.import_tabel(self.widgetTabel, self.loadedTable)
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Traffic Lanes')
        self.widgetForeignTabel.clear()
        self.widgetForeignTabel.setRowCount(0)
        self.widgetForeignTabel.setColumnCount(0)

    def vehicles_b_clicked(self):
        print("Loading table Vehicles")
        self.loadedTable = 'vehicles'
        self.import_tabel(self.widgetTabel, self.loadedTable)
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Vehicles')
        self.widgetForeignTabel.clear()
        self.widgetForeignTabel.setRowCount(0)
        self.widgetForeignTabel.setColumnCount(0)

    def weather_b_clicked(self):
        print("Loading table Weather Conditions")
        self.loadedTable = 'weather_conditions'
        self.import_tabel(self.widgetTabel, self.loadedTable)
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Weather Conditions')
        self.widgetForeignTabel.clear()
        self.widgetForeignTabel.setRowCount(0)
        self.widgetForeignTabel.setColumnCount(0)

    def events_b_clicked(self):
        print("Loading table Events")
        self.loadedTable = 'i_events'
        self.import_tabel(self.widgetTabel, self.loadedTable)
        # modificare titlu
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget().parentWidget()
        titlu = parent_widget.findChild(QLabel, 'Title_Text')
        titlu.setText('Events')
        self.widgetForeignTabel.clear()
        self.widgetForeignTabel.setRowCount(0)
        self.widgetForeignTabel.setColumnCount(0)

    def drop(self):
        print('dropping changes!')
        self.import_tabel(self.widgetTabel, self.loadedTable)

    def delete_row(self):
        self.loadingReady = False
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget()
        table = parent_widget.findChild(QTableWidget)
        # table.removeRow(table.currentRow())
        for coloana in range(0, table.columnCount()):
            item = table.item(table.currentRow(), coloana)
            if item is not None:
                item.setForeground(QBrush(QColor(255, 0, 0)))
        self.loadingReady = True

    def add_row(self):
        self.loadingReady = False
        sender_button = self.sender()
        parent_widget = sender_button.parentWidget().parentWidget()
        table = parent_widget.findChild(QTableWidget)
        # adaugare rand
        table.insertRow(table.rowCount())
        # generare automata primary key pentru toate tabelele mai putin weather conditions
        if self.loadedTable != 'weather_conditions':
            lista_index = list()
            for i in range(0, table.rowCount()):
                item_tabel = table.item(i, 0)
                if item_tabel is not None:
                    primary_key = int(item_tabel.text())
                    lista_index.append(primary_key)
            if len(lista_index) > 0:
                minindex = -1
                lista_index.sort()
                for i in lista_index:
                    if minindex < i and i-minindex <= 1:
                        minindex = i
                minindex += 1
            else:
                minindex = 0
            item = QTableWidgetItem(str(minindex))
            item.setForeground(QBrush(QColor(0, 255, 0)))
            table.setItem(table.rowCount()-1, 0, item)
            # e putin hardcodat, ar merge imbunatatit
            if self.constrangeri[self.loadedTable][0] == 'primary_key':
                self.widgetTabel.item(self.widgetTabel.rowCount()-1, 0).setFlags(QtCore.Qt.NoItemFlags)
                self.widgetTabel.item(self.widgetTabel.rowCount()-1, 0).setBackground(QBrush(QColor(15, 15, 15)))
            self.loadingReady = True
            for coloana in range(1, self.widgetTabel.columnCount()):
                self.test_valid_valoare(self.widgetTabel.rowCount()-1, coloana)
        else:
            self.loadingReady = True
            for coloana in range(0, self.widgetTabel.columnCount()):
                self.test_valid_valoare(self.widgetTabel.rowCount() - 1, coloana)

    def check_linie(self, linie):
        for coloana in range(linie, self.widgetTabel.columnCount()):
            if self.widgetTabel.item(linie, coloana) is not None and self.widgetTabel.item(linie, coloana).background() == QBrush(QColor(255, 0, 0)):
                return False
        return True

    def commit(self):
        # self.cur.execute('begin tran\n')
        for linie in range(0, self.widgetTabel.rowCount()):
            if self.check_linie(linie) is False:
                print("Nu toate elementele sunt Valide!")
                #self.cur.execute('drop')
                return False
            if self.widgetTabel.item(linie, 0) is not None and self.widgetTabel.item(linie, 0).foreground() == QBrush(QColor(0, 255, 0)):
                print("Adaug linia "+str(linie))
                nume_coloane = ''
                valori_noi = ''
                for coloana in range(0, self.widgetTabel.columnCount()):
                    if self.widgetTabel.item(linie, coloana) is not None:
                        nume_coloane += self.column_names[self.loadedTable][coloana]+', '
                        valori_noi += "'"+self.widgetTabel.item(linie, coloana).text()+"'"+', '
                nume_coloane = nume_coloane[:-2]
                valori_noi = valori_noi[:-2]
                comanda = "insert into {} ({}) values ({})".format(self.loadedTable, nume_coloane, valori_noi)
                print(comanda)
                self.cur.execute(comanda)
            elif self.widgetTabel.item(linie, 0) is not None and self.widgetTabel.item(linie, 0).foreground() == QBrush(QColor(255, 0, 0)):
                print("Sterg linia "+str(linie))
            else:
                for coloana in range(1, self.widgetTabel.columnCount()):
                    if self.widgetTabel.item(linie, coloana) is not None and self.widgetTabel.item(linie, coloana).foreground() == QBrush(QColor(0, 255, 0)):
                        print("Modific linia "+str(linie)+" pe coloana "+str(coloana))




        return True
            #for i in range(len(new_rows)):
        #    commands.append("INSERT INTO {}({}) VALUES ({})".format(table_name, fields, new_rows[i]))
        #for command in commands:
        #    try:
        #        print(command)
        #        self.cur.execute(command)
        #        self.cur.execute('commit')
        #        print('Insert Complete!')
        #    except Exception as e:
        #        print(e)

    def prepare_data(self, rows, fields):
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

        return rows, field_str

    def get_text_color(self, table_item):
        if table_item is not None:
            brush = table_item.foreground()
            text_color = brush.color()
            return text_color
        else:
            return None
