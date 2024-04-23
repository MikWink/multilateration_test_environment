import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Create a QWebEngineView
        self.web = QWebEngineView()
        self.web.load(QUrl.fromLocalFile("/terrain_map.html"))

        # Create a QLineEdit for text input
        self.text_input = QLineEdit(self)
        self.text_input.setPlaceholderText("Enter text here")

        # Create a QPushButton
        self.button = QPushButton("Submit", self)
        self.button.clicked.connect(self.button_clicked)

        # Create a QLabel
        self.label = QLabel("This is a label", self)

        # Create a layout and add widgets
        layout = QGridLayout()
        layout.addWidget(self.web, 2, 0)
        layout.addWidget(self.text_input, 1, 0)
        layout.addWidget(self.button, 1, 1)
        layout.addWidget(self.label, 0, 0)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def button_clicked(self):
        # Example: Get text from QLineEdit and set it as QLabel text
        text = self.text_input.text()
        self.label.setText(f"You entered: {text}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
