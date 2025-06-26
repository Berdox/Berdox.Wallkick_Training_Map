import sys

def swap_props(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Swap occurrences of prop_static and prop_dynamic
        content = content.replace('prop_static', 'TEMP_REPLACEMENT')
        content = content.replace('prop_dynamic', 'prop_static')
        content = content.replace('TEMP_REPLACEMENT', 'prop_dynamic')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        print(f"Successfully swapped 'prop_static' and 'prop_dynamic' in {file_path}")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python swap_props.py <file_path>")
    else:
        swap_props(sys.argv[1])