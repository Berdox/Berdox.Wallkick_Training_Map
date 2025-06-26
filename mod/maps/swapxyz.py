import re

# Function to swap z and y in the angles format
def swap_z_y_in_angles(angles_str):
    # Extract x, z, y from the angles string
    angles = list(map(int, angles_str.split(', ')))
    # Swap z and y
    angles[1], angles[2] = angles[2], angles[1]
    return f"{angles[0]} {angles[1]} {angles[2]}"

def modify_map_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    modified_lines = []
    
    for line in lines:
        # Search for "angle" and modify its format to "angles 0 0 z"
        angle_match = re.search(r'"angle"\s*"(-?\d+)"', line)
        if angle_match:
            original_angle = angle_match.group(1)
            # Change angle to angles 0 0 z
            line = line.replace(f'"angle" "{original_angle}"', f'"angles" "0 0 {original_angle}"')

        # Search for "angles" in x, z, y format and swap z and y
        angles_match = re.search(r'"angles"\s*"(-?\d+),\s*(-?\d+),\s*(-?\d+)"', line)
        if angles_match:
            original_angles = angles_match.group(0)
            new_angles = swap_z_y_in_angles(f"{angles_match.group(1)}, {angles_match.group(2)}, {angles_match.group(3)}")
            line = line.replace(original_angles, f'"angles" "{new_angles}"')

        modified_lines.append(line)

    # Write the modified lines back to the file
    with open(file_path, 'w') as file:
        file.writelines(modified_lines)

# Replace 'mp_wallkick.map' with the path to your actual file
modify_map_file('mp_wallkick.map')
