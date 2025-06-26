import re

def adjust_angle(angle):
    """
    Adjust the angle by subtracting 90 and ensuring it wraps around correctly.
    The valid range is between -180 to 180.
    """
    adjusted_angle = angle + 90
    
    # Wrap around logic
    if adjusted_angle < -180:
        adjusted_angle += 360
    elif adjusted_angle > 180:
        adjusted_angle -= 360
    
    return adjusted_angle

def adjust_angles_in_map(map_file_path):
    with open(map_file_path, 'r') as file:
        lines = file.readlines()

    updated_lines = []

    for line in lines:
        # Look for "angle" "0" and adjust it
        angle_match = re.search(r'"angle"\s*"0"\s*"\s*(-?\d+)', line)
        if angle_match:
            angle_value = int(angle_match.group(1))
            adjusted_angle = adjust_angle(angle_value)
            line = line.replace(f'"angle" "0" "{angle_value}"', f'"angle" "0" "{adjusted_angle}"')
        
        # Look for "angles" "y z x" and adjust the z value and swap y and x
        angles_match = re.search(r'"angles"\s*"(\d+)\s*(-?\d+)\s*(-?\d+)', line)
        if angles_match:
            y, z, x = map(int, angles_match.groups())
            adjusted_z = adjust_angle(z)
            # Swap y and x
            line = line.replace(f'"angles" "{y} {z} {x}"', f'"angles" "{x} {adjusted_z} {y}"')

        updated_lines.append(line)

    # Write the updated lines back to the file
    with open(map_file_path, 'w') as file:
        file.writelines(updated_lines)
    print("Adjustments complete.")

# Example usage
map_file_path = 'mp_wallkick.map'
adjust_angles_in_map(map_file_path)


