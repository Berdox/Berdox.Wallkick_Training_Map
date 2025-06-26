import re
import numpy as np
from scipy.spatial import ConvexHull

def read_map_file(path):
    with open(path, 'r') as file:
        return file.read()

def extract_entities(map_text):
    return re.findall(r'// entity \d+\n\{(.*?)\n\}', map_text, re.DOTALL)

def extract_teleport_sender_data(entity_block):
    if '"classname" "func_brush"' in entity_block and '"teleport_sender"' in entity_block:
        sender_match = re.search(r'"teleport_sender" "(\d+)"', entity_block)
        teleport_sender_value = sender_match.group(1)

        brush_block_match = re.search(r'brushDef\s*\{(.*?)\}', entity_block, re.DOTALL)
        if not brush_block_match:
            return None, None

        brush_text = brush_block_match.group(1)
        vertices = re.findall(r'\( ([\d\.-]+) ([\d\.-]+) ([\d\.-]+) \)', brush_text)
        vertices = [(float(x), float(y), float(z)) for x, y, z in vertices]

        # Use Convex Hull to find unique corners
        try:
            points = np.array(vertices)
            hull = ConvexHull(points)
            unique_indices = set(hull.vertices)
            hull_vertices = [tuple(points[i]) for i in unique_indices]

            if len(hull_vertices) != 8:
                print(f"⚠️  teleport_sender {teleport_sender_value} has {len(hull_vertices)} vertices — skipping.")
                return None, None

            named_vertices = name_vertices(hull_vertices)
            return teleport_sender_value, named_vertices

        except Exception as e:
            print(f"❌ ConvexHull failed for teleport_sender {teleport_sender_value}: {e}")
            return None, None
    return None, None

def name_vertices(vertices):
    # Sort to find min/max along each axis
    xs = [v[0] for v in vertices]
    ys = [v[1] for v in vertices]
    zs = [v[2] for v in vertices]

    named = {}
    for v in vertices:
        x, y, z = v
        name = ''
        name += 'bottom_' if z == min(zs) else 'top_'
        name += 'back_' if y == min(ys) else 'front_'
        name += 'left' if x == min(xs) else 'right'
        named[name] = v

    # fallback for duplicate names
    if len(named) != 8:
        named = {f'vertex{i+1}': v for i, v in enumerate(vertices)}
    return named

def generate_squirrel_class(class_name, named_vertices):
    class_code = f"class {class_name} {{\n"
    for name, (x, y, z) in named_vertices.items():
        class_code += f"    static const vector {name} = <{x}, {y}, {z}>;\n"
    class_code += "}\n"
    return class_code

def main():
    map_path = "your_map_file.map"  # change to your actual .map file path
    output_path = "teleport_sender.nut"

    map_text = read_map_file(map_path)
    entities = extract_entities(map_text)

    class_blocks = []

    for entity in entities:
        sender_id, named_vertices = extract_teleport_sender_data(entity)
        if sender_id and named_vertices:
            class_name = f"teleport_sender_{sender_id}"
            class_code = generate_squirrel_class(class_name, named_vertices)
            class_blocks.append(class_code)

    if class_blocks:
        with open(output_path, 'w') as f:
            f.write("// Generated teleport sender classes\n\n")
            for block in class_blocks:
                f.write(block + "\n")
        print(f"✅ Wrote {len(class_blocks)} teleport_sender classes to '{output_path}'")
    else:
        print("⚠️  No valid teleport_sender brushes found.")

if __name__ == "__main__":
    main()
