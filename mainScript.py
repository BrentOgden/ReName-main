import sys 
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap 
from PyQt6.QtCore import QTimer, QCoreApplication 
from appGUI import App, SplashScreen
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def main():
    QCoreApplication.processEvents()
    app = QApplication(sys.argv)

    

    
    
     # Initialize the splash screen
    splash_pixmap = QPixmap(resource_path('wireless_splash.png'))
    splash = SplashScreen(splash_pixmap)
    splash.show()
    
    
    ex = App()
    ex.show()

    
     # Close the splash screen after a delay
    QTimer.singleShot(400, splash.close)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()