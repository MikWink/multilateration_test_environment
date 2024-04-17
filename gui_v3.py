import tkinter as tk
import webview
import plotly.io as pio
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.subplots as sp

# Create a Tkinter window
window = tk.Tk()
window.title("Terrain Map")
window.geometry("800x600")

# Load the image
im = Image.open('ilmenau_r5km_c3.tif')
imarray = np.array(im)

# Define the real-world coordinates
ilmenau_area = np.array([[632621, 5609803], [641086, 5623932]])
x_step = (ilmenau_area[1][1] - ilmenau_area[0][1]) / imarray.shape[1]
y_step = (ilmenau_area[1][0] - ilmenau_area[0][0]) / imarray.shape[0]
y_coords = np.arange(632621, 641086, y_step)
x_coords = np.arange(5609803, 5623932, x_step)

# Create x and y coordinate arrays
x = np.arange(10000, imarray.shape[1]+10000, 1)
y = np.arange(6000000, imarray.shape[0]+6000000, 1)

# Create a meshgrid from x and y coordinates
X, Y = np.meshgrid(x_coords, y_coords)

# Create a subplot with a 3D surface plot and a scatter plot
fig = sp.make_subplots(rows=1, cols=1, specs=[[{'type': 'surface'}]])
fig.add_trace(go.Surface(x=X, y=Y, z=imarray, colorscale='Viridis', showscale=False, name='Terrain'), row=1, col=1)
fig.add_trace(go.Scatter3d(x=[5616652], y=[636156], z=[200], name='Ilmenau', mode='markers', marker=dict(size=5, color='grey')), row=1, col=1)

# Set the title and axis labels
fig.update_layout(title='Heightmap', scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Height'))
fig.update_scenes(aspectmode='manual', aspectratio=dict(x=2, y=1, z=0.2))

# Convert the figure to JSON format
fig_json = pio.to_json(fig)

# Create a HTML file to display the Plotly figure
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
</head>
<body>
    <div id="figure"></div>
    <script>
        var figure = {fig_json};
        Plotly.newPlot('figure', figure.data, figure.layout);
    </script>
</body>
</html>
"""
with open('terrain_map.html', 'w') as file:
    file.write(html_content)

# Open the HTML file in a WebView component
webview.create_window(window, url="terrain_map.html", width=800, height=600)

# Start the Tkinter event loop
window.mainloop()