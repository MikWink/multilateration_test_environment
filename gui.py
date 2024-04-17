from tkinter import *
from tkinter import ttk
import plotly.graph_objects as go
import pandas as pd
import plotly.offline as pyo
import webview
import threading
import json
from tkinter import filedialog

axis = ["X", "Y", "Z"]


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
    file_path = filedialog.asksaveasfilename(defaultextension=".json")
    with open(file_path, "w") as file:
        json.dump(data, file)
    print("JSON file saved!")

def load_entries(entries):
    # Open file dialog to select JSON file
    Tk().withdraw()
    filename = filedialog.askopenfilename(title="Select JSON file")

    try:
        with open(filename, 'r') as json_file:
            data = json.load(json_file)

            for i, entry in enumerate(entries):
                i1 = str(i//3)
                i2 = str(i%3 +1)
                print(type(i1))
                entry.insert(0, data[i1][i2])

    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")

    return None

def update_map_window():
    print("Updating map window!")
# Create the coordinate entry window
def create_coordinate_window():
    root = Tk()
    frm = ttk.Frame(root, padding=20)
    frm.grid()
    entries = []

    def save_entries():
        entry_list = []
        for entry in entries:
            entry_list.append(entry.get())
        print("Entries saved!")
        save_json(entry_list)



    for i in range(5):
        if not i == 4:
            ttk.Label(frm, text="BS " + str(i) + ": ").grid(column=i * 2, row=0)
        else:
            ttk.Label(frm, text="MS: ").grid(column=i * 2, row=0)
        for j in range(3):
            ttk.Label(frm, text=axis[j] + ": ").grid(column=i * 2, row=j + 1)
            entry = ttk.Entry(frm)
            entry.grid(column=i * 2 + 1, row=j + 1)
            entries.append(entry)

    save_button = ttk.Button(frm, text="Save", command=save_entries)
    save_button.grid(column=10, row=4, pady=10)
    load_button = ttk.Button(frm, text="Load", command=lambda: load_entries(entries))
    load_button.grid(column=11, row=4, pady=10)
    update_button = ttk.Button(frm, text="Update", command=lambda: update_map_window(entries))
    update_button.grid(column=12, row=4, pady=10)

    root.mainloop()


# Create the map window
def create_map_window():
    # Read data from a csv
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')

    fig = go.Figure(data=[go.Surface(z=z_data.values)])

    fig.update_layout(title='Mt Bruno Elevation', autosize=True,
                      margin=dict(l=65, r=50, b=65, t=90))

    # Generate the HTML string of the figure
    html_string = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')

    entry_window = webview.create_window('Map', html=html_string, width=1600, height=900)
    webview.start()


# Create a thread to run the coordinate entry window
coordinate_thread = threading.Thread(target=create_coordinate_window)
coordinate_thread.start()

# Create the map window
create_map_window()
