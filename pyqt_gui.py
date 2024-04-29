import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QComboBox, QFileDialog, QMainWindow, QGridLayout, QWidget, QLineEdit, QPushButton, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
from map_generator import Map

input_fields = []
generated_map = Map()
bs_labels = []
ms_labels = []

def on_load_clicked():
    global input_fields
    # Open file dialog to select JSON file
    print("i crash heare1")
    file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "JSON Files (*.json);;All Files (*)")
    print("i crash heare2")
    try:
        temp = [['5621990', '636646', '0'], ['5616452', '636456', '0'], ['5618652', '640156', '0'] , ['5619990', '636346', '200']]
        print("i crash heare3")
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for i, input_field in enumerate(input_fields):
                i1 = i // 3
                i2 = i % 3 + 1
                #temp.append(data[str(i1)][str(i2)])
                test = temp[i1][i2-1]
                # Temporary solution
                input_field.setText(test)

    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

    print("i crash heare5")


def on_save_clicked():
    global input_fields
    # Collect data from input fields
    data = []
    for i in range(len(input_fields)):
        data.append(input_fields[i].text())

    # Save data to a JSON file
    save_json(data)

def save_json(data):
    data = {
        '0': {
            '1': data[0],
            '2': data[1],
            '3': data[2]
        },
        '1': {
            '1': data[3],
            '2': data[4],
            '3': data[5]
        },
        '2': {
            '1': data[6],
            '2': data[7],
            '3': data[8]
        },
        '3': {
            '1': data[9],
            '2': data[10],
            '3': data[11]
        },
        '4': {
            '1': data[12],
            '2': data[13],
            '3': data[14]
        }
    }
    file_path, _ = QFileDialog.getSaveFileName(None, "Save File", "", "JSON Files (*.json);;All Files (*)", "*.json")
    with open(file_path, "w") as file:
        json.dump(data, file)
    print("JSON file saved!")

def on_update_clicked(web):
    points = [[] for _ in range(5)]
    for i in range(5):
        points[i] = [0 for _ in range(3)]
    for i, input_field in enumerate(input_fields):
        i1 = i // 3
        i2 = i % 3
        points[i1][i2] = input_field.text()
        if i1 < 4 and i2 < 3:
            bs_labels[i1][i2].setText(input_field.text())
    generated_map.update(points)
    web.reload()

def initUI(web):
    global input_fields
    layout = QGridLayout()

    # Define the labels for each block
    block_labels = ['BS0:', 'BS1:', 'BS2:', 'BS3:', 'MS:']
    temp = [['5621990', '636646', '0'], ['5616452', '636456', '0'], ['5618652', '640156', '0'],
            ['5619990', '636346', '200'], ['5618222', '637900', '180']]
    for i, block_label in enumerate(block_labels):
        # Add the block label
        layout.addWidget(QLabel(block_label), 0, i * 4)

        # Add the 'x:', 'y:', 'z:' labels
        for j in range(1, 4):
            layout.addWidget(QLabel(f'{chr(120 + j - 1)}:'), j, i * 4)

        # Add the text inputs for 'x', 'y', 'z'
        for j in range(1, 4):
            input_field = QLineEdit()
            input_field.setText(temp[i][j-1])
            layout.addWidget(input_field, j, i * 4 + 1)
            input_fields.append(input_field)  # Keep track of input fields

    save_button = QPushButton("Save")
    save_button.clicked.connect(lambda: on_save_clicked())  # Connect the button to the slot
    load_button = QPushButton("Load")
    load_button.clicked.connect(lambda: on_load_clicked())
    update_button = QPushButton("Update")
    update_button.clicked.connect(lambda: on_update_clicked(web))
    layout.addWidget(save_button, 1, 22)
    layout.addWidget(load_button, 2, 22)
    layout.addWidget(update_button, 3, 22)

    return layout

def initUserInfo(web):
    layout = QGridLayout()
    user_info = QLabel("Info:")
    layout.addWidget(user_info, 0, 0)
    block_labels = ['BS0:', 'BS1:', 'BS2:', 'BS3:', 'MS:']
    values = [['5621990', '636646', '0'], ['5616452', '636456', '0'], ['5618652', '640156', '0'], ['5619990', '636346', '200'], ['5618222', '637900', '180']]


    for i, block_label in enumerate(block_labels):
        # Add the block label
        layout.addWidget(QLabel(block_label), i*4 + 1, 0)

        bs_labels_tmp = []
        # Add the 'x:', 'y:', 'z:' labels
        for j in range(1, 4):
            layout.addWidget(QLabel(f'{chr(120 + j - 1)}:'), i*4 + j + 1, 0)
            if i < 4:
                label = QLabel(f'{values[i][j-1]}')
                bs_labels_tmp.append(label)
                layout.addWidget(label, i * 4 + j + 1, 1)
            else:
                layout.addWidget(QLabel('-'), i * 4 + j + 1, 1)
        bs_labels.append(bs_labels_tmp)
    return layout

def initCalculationInput(web):
    layout = QGridLayout()
    dropdown = QComboBox()
    dropdown.addItem("Foy")
    layout.addWidget(dropdown, 0, 0)
    layout.addWidget(QPushButton("Calculate"), 1, 0)

    return layout

def setupGui():
    # Create a QMainWindow
    window = QMainWindow()

    # Create a QWebEngineView
    web = QWebEngineView()
    web.load(QUrl.fromLocalFile("/terrain_map.html"))

    # Create the user input widget
    user_input = QWidget()
    user_input.setLayout(initUI(web))

    # Create a user info
    user_info = QWidget()
    user_info.setLayout(initUserInfo(web))
    print(bs_labels)

    # Calculation input
    calculation_input = QWidget()
    calculation_input.setLayout(initCalculationInput(web))

    # Create a layout and add widgets
    layout = QGridLayout()
    layout.addWidget(user_input, 0, 0)
    layout.addWidget(web, 1, 0)
    layout.addWidget(user_info, 1, 1)
    layout.addWidget(calculation_input, 0, 1)

    # Create a central widget and set the layout
    central_widget = QWidget()
    central_widget.setLayout(layout)
    window.setCentralWidget(central_widget)

    return window

app = QApplication(sys.argv)
window = setupGui()
window.show()
sys.exit(app.exec_())