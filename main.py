from UserInterface import *
from DBManager import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    window.show()
    app.exec_()