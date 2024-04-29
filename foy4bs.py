import numpy as np
import math
from transformer import CoordinateTransformer

BS0 = np.array([49.449010, 11.064284, 0])
BS1 = np.array([49.457646, 11.088916, 0])
BS2 = np.array([49.447273, 11.088916, 0])
BS3 = np.array([49.452778, 11.077613, 500])
MS = np.array([49.449611, 11.075628, 300.57])

bs_list = [BS0, BS1, BS2, BS3, MS]
converted_bs = []
R_i_0 = [0, 0, 0, 0]
R_i_real = [0, 0, 0, 0]
R_i_guess = [0, 0, 0, 0]

h = np.zeros(3)
G = np.zeros((3, 3))

deltaXY = np.zeros(3)

guessed_position = [650745.995, 5479748.09, 250.]

def update_x_y():
    global guessed_position
    print(f"Old position: {guessed_position}")
    guessed_position[0] += deltaXY[0]
    guessed_position[1] += deltaXY[1]
    guessed_position[2] += deltaXY[2]
    print(f"New position: {guessed_position}")
    print(f"Real position: {converted_bs[4]}\n")
    print(f"Difference: {guessed_position[0] - converted_bs[4][0]}, {guessed_position[1] - converted_bs[4][1]}, {guessed_position[2] - converted_bs[4][2]}\n")


def calculate_deltaXY():
    global deltaXY
    GT_G = np.matmul(np.transpose(G), G)
    GT_G_inv = np.linalg.inv(GT_G)
    GT_G_inv_GT = np.matmul(GT_G_inv, np.transpose(G))
    deltaXY = np.matmul(GT_G_inv_GT, h)
    print(f"deltaXY: {deltaXY}\n")

def calculate_G():
    global G
    G[0, 0] = ((converted_bs[0][0] - guessed_position[0]) / R_i_guess[0]) - ((converted_bs[1][0] - guessed_position[0]) / R_i_guess[1])
    G[0, 1] = ((converted_bs[0][1] - guessed_position[1]) / R_i_guess[0]) - ((converted_bs[1][1] - guessed_position[1]) / R_i_guess[1])
    G[0, 2] = ((converted_bs[0][2] - guessed_position[2]) / R_i_guess[0]) - ((converted_bs[1][2] - guessed_position[2]) / R_i_guess[1])
    G[1, 0] = ((converted_bs[0][0] - guessed_position[0]) / R_i_guess[0]) - ((converted_bs[2][0] - guessed_position[0]) / R_i_guess[2])
    G[1, 1] = ((converted_bs[0][1] - guessed_position[1]) / R_i_guess[0]) - ((converted_bs[2][1] - guessed_position[1]) / R_i_guess[2])
    G[1, 2] = ((converted_bs[0][2] - guessed_position[2]) / R_i_guess[0]) - ((converted_bs[2][2] - guessed_position[2]) / R_i_guess[2])
    G[2, 0] = ((converted_bs[0][0] - guessed_position[0]) / R_i_guess[0]) - ((converted_bs[3][0] - guessed_position[0]) / R_i_guess[3])
    G[2, 1] = ((converted_bs[0][1] - guessed_position[1]) / R_i_guess[0]) - ((converted_bs[3][1] - guessed_position[1]) / R_i_guess[3])
    G[2, 2] = ((converted_bs[0][2] - guessed_position[2]) / R_i_guess[0]) - ((converted_bs[3][2] - guessed_position[2]) / R_i_guess[3])

    print(f"G: {G}\n")

def calculate_h():
    # Calculate the h vector
    for i in range(1, 4):
        print(f"R_i_0[i]: {R_i_0[i]}, R_iguess[i]: {R_i_guess[i]}, R_iguess[i-1]: {R_i_guess[i-1]}")
        h[i-1] = (R_i_0[i] - (R_i_guess[i] - R_i_guess[0]))

    print(f"h: {h}\n")

def calculate_R_i_guess():
    for i in range(4):
        R_i_guess[i] = math.sqrt((converted_bs[i][0] - guessed_position[0]) ** 2 + (converted_bs[i][1] - guessed_position[1]) ** 2 + (converted_bs[i][2] - guessed_position[2]) ** 2)

    print(f"R_i_guess: {R_i_guess}\n")


def make_init_guess():
    global guessed_position
    # Convert bs_list to a NumPy array
    bs_array = np.array([converted_bs[0], converted_bs[1], converted_bs[2], converted_bs[3]])

    # Compute the center coordinates
    x_vals = np.sum(bs_array[:, 0]) / 4
    y_vals = np.sum(bs_array[:, 1]) / 4
    center = np.array([x_vals, y_vals, converted_bs[3][2] / 2])

    # Print the result
    print(f"Initial guess: {center}\n")
    guessed_position = center


def calculate_tdoa_s():
    for i in range(4):
        R_i_real[i] = math.sqrt((converted_bs[i][0] - converted_bs[4][0]) ** 2 + (converted_bs[i][1] - converted_bs[4][1]) ** 2 + (converted_bs[i][2] - converted_bs[4][2]) ** 2)
        R_i_0[i] = math.sqrt((converted_bs[i][0] - converted_bs[4][0])**2 + (converted_bs[i][1] - converted_bs[4][1])**2 + (converted_bs[i][2] - converted_bs[4][2])**2) - math.sqrt((converted_bs[0][0] - converted_bs[4][0])**2 + (converted_bs[0][1] - converted_bs[4][1])**2 + (converted_bs[0][2] - converted_bs[4][2])**2)

    print(f"R_i: {R_i_real}")
    print(f"R_i_0: {R_i_0}\n")

def convert_coordinates():
    for bs in bs_list:
        utm_list = list(CoordinateTransformer.long_to_utm(bs))
        utm_list.append(bs[2])
        converted_bs.append(utm_list)

    print(f"UTM Coordinates (x/y/z):\nBS0: {converted_bs[0]}\nBS1: {converted_bs[1]}\nBS2: {converted_bs[2]}\nBS3: {converted_bs[3]}\nMS: {converted_bs[4]}\n")


print(f"Coordinates (lat/lon/alt):\nBS0: {BS0}\nBS1: {BS1}\nBS2: {BS2}\nBS3: {BS3}\nMS: {MS}\n")
convert_coordinates()
make_init_guess()
for i in range(20):
    print(f"Step {i+1}")
    calculate_R_i_guess()
    calculate_tdoa_s()
    calculate_h()
    calculate_G()
    calculate_deltaXY()
    update_x_y()