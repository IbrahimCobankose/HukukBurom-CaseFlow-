import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt
from views.formLogin import formLogin


def run():
    print("The program is running.")
    # QtWebEngineView hatasını gidermek için bu satır eklendi.
    # Bu, QCoreApplication oluşturulmadan önce yapılmalıdır.
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    
    app = QtWidgets.QApplication(sys.argv)
    win = formLogin()
    win.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    run()