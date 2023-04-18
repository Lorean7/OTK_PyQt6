from PyQt6.QtWidgets import QApplication

from PyQt6.QtGui import QIcon

#init window
from interface.mainWindow import mainWindow

if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon('./img/icon.png'))
    window = mainWindow()
    window.show()
    app.exec()
    


