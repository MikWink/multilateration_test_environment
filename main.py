import sys
from PyQt5.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QWidget

class CustomGridLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()

        # Define the labels for each block
        block_labels = ['BS0:', 'BS1:']

        for i, block_label in enumerate(block_labels):
            # Add the block label
            layout.addWidget(QLabel(block_label), 0, i*4)

            # Add the 'x:', 'y:', 'z:' labels
            for j in range(1, 4):
                layout.addWidget(QLabel(f'{chr(120 + j - 1)}:'), j, i*4)

            # Add the text inputs for 'x', 'y', 'z'
            for j in range(1, 4):
                layout.addWidget(QLineEdit(), j, i*4 + 1)

        self.setLayout(layout)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomGridLayout()
    window.show()
    sys.exit(app.exec_())
