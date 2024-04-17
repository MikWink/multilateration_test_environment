from PIL import Image
import numpy as np
import plotly.graph_objects as go
import plotly.offline as pyo

im = Image.open('ilmenau_r5km_c3.tif')


imarray = np.array(im)

ilmenau_area = np.array([[632621, 5609803], [641086, 5623932]])

x_step = (ilmenau_area[1][0] - ilmenau_area[0][0]) / imarray.shape[0]
y_step = (ilmenau_area[1][1] - ilmenau_area[0][1]) / imarray.shape[1]
print(x_step, y_step)

# Define the real-world coordinates
y_coords = np.arange(632621, 641086, x_step)
x_coords = np.arange(5609803, 5623932, y_step)

print(len(x_coords), len(y_coords))

# Create x and y coordinate arrays
x = np.arange(0, imarray.shape[1], 1)
y = np.arange(0, imarray.shape[0], 1)

# Create a meshgrid from x and y coordinates
X, Y = np.meshgrid(x_coords, y_coords)



# Create a 3D surface plot
fig = go.Figure(data=[go.Surface(x=x_coords, y=y_coords, z=imarray, colorscale='Viridis', showscale=False, name='Terrain')])

# Add a scatter3d trace for the point
point_name = "Ilmenau"
point_x = 5616652
point_y = 636156
#fig.add_trace(go.Scatter3d(x=[point_x], y=[point_y], z=[imarray[int(point_y), int(point_x)]], name='Ilmenau', marker=dict(size=5, color='grey')))


# Set the title and axis labels
fig.update_layout(title='Heightmap', scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Height'))

# Generate the HTML string of the figure
html_string = pyo.plot(fig, include_plotlyjs='cdn', output_type='div')

# Update the map window with the new plot
with open('terrain_map.html', 'w') as file:
    file.write(html_string)


print(imarray.shape)
print(im.size)
print(imarray)