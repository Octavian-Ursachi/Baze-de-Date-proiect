from DBManager import disconectare
from UserInterface import *

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        window = Ui()
        window.show()
        app.exec_()
    except any:
        print("Eroare")
    finally:
        disconectare()
