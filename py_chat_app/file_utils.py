import os

def read_static_context(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading static context file: {e}")
        return ""

def process_files(directory, output_file):
    try:
        with open(output_file, 'w') as outfile:
            for root, dirs, files in os.walk(directory):
                for filename in files:
                    file_path = os.path.join(root, filename)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                            content = infile.read()
                            outfile.write(f"// {filename}\n")
                            outfile.write(content)
                            outfile.write("\n\n")
                            print(f"Processed: {file_path}")
                    except PermissionError:
                        print(f"Permission denied: {file_path}. Skipping this file.")
                    except Exception as e:
                        print(f"Error reading {file_path}: {e}")
        print(f"All files have been processed and written to '{output_file}'.")
    except Exception as e:
        print(f"Error: {e}")
