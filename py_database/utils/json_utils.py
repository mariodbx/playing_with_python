import json

def read_json(file_path):
    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            return data
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None
    except Exception as e:
        print(f"Error reading JSON file: {e}")
        return None

def write_json(file_path, data):
    try:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data written to {file_path} successfully.")
    except Exception as e:
        print(f"Error writing to JSON file: {e}")
