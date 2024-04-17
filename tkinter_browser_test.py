import sys
from PyQt5.QtCore import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)

url = QUrl.fromLocalFile("C:/Users/winkler/Desktop/Cloud/Dokumente/Studium/Bachelorarbeit/Code/multilateration_test_environment/terrain_map.html")

web = QWebEngineView()
web.load(url)
web.show()

sys.exit(app.exec_())