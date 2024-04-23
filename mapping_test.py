def map_value(value, min_value, max_value, new_min, new_max):
    """
    Maps a value from one range to another using linear interpolation.

    Args:
    - value (float): The value to be mapped.
    - min_value (float): The minimum value of the original range.
    - max_value (float): The maximum value of the original range.
    - new_min (float): The minimum value of the new range.
    - new_max (float): The maximum value of the new range.

    Returns:
    - mapped_value (float): The mapped value.
    """
    # Perform linear interpolation
    mapped_value = ((value - min_value) / (max_value - min_value)) * (new_max - new_min) + new_min
    return mapped_value

# Example usage:
value = 636156
min_value = 632621
max_value = 641086
new_min = 0
new_max = 450

mapped_value = map_value(value, min_value, max_value, new_min, new_max)
print("Mapped value:", round(mapped_value))
