import os

def read_and_write_files_recursively(input_folder, file_type=None, output_file=None, ignore_word=None, max_file_size=None, header=None, footer=None, transform_content=None, file_tree_output=None):
    """
    Reads all files (or files of a specified type) from a given folder and its subfolders,
    then writes their contents into a single text file, while optionally ignoring files
    containing a specified word in their name, and applying additional transformations or
    filters. Additionally, generates a file tree in markup format and writes it to a separate file.

    Parameters:
    input_folder (str): The path of the folder to read files from.
    file_type (str): The file type to read (e.g., '.cs'). If None, all files are read.
    output_file (str): The path of the output text file.
    ignore_word (str): A word that, if present in a file's name, causes the file to be ignored.
    max_file_size (int): Maximum file size in bytes. Files larger than this will be ignored.
    header (str): A custom header to add to the output file.
    footer (str): A custom footer to add to the output file.
    transform_content (func): An optional function to transform the content of each file before writing.
    file_tree_output (str): The path of the file tree output file.
    """
    try:
        validate_input_folder(input_folder)
        processed_files_count = 0
        log_entries = []
        file_tree_lines = []

        if output_file:
            with open(output_file, 'w') as outfile:
                write_header(outfile, header)
                processed_files_count, file_tree_lines, log_entries = process_files(input_folder, file_type, ignore_word, max_file_size, transform_content, outfile, file_tree_lines, log_entries)
                write_footer(outfile, footer)

            generate_log_file(output_file, processed_files_count, log_entries)
            generate_file_tree_file(file_tree_output, file_tree_lines)
        
        print(f"All {file_type if file_type else ''} files from '{input_folder}' and its subfolders have been written to '{output_file}'.")
        print(f"Total files processed: {processed_files_count}")

    except Exception as e:
        print(f"Error: {e}")

def validate_input_folder(input_folder):
    """Checks if the input folder exists."""
    if not os.path.exists(input_folder):
        raise Exception(f"The folder '{input_folder}' does not exist.")

def write_header(outfile, header):
    """Writes the header to the output file."""
    if header:
        outfile.write(header + "\n\n")

def process_files(input_folder, file_type, ignore_word, max_file_size, transform_content, outfile, file_tree_lines, log_entries):
    """Processes files in the input folder and writes their content to the output file."""
    processed_files_count = 0
    for root, dirs, files in os.walk(input_folder):
        try:
            file_tree_lines = add_directory_to_file_tree(root, input_folder, file_tree_lines)
            for filename in files:
                if should_process_file(filename, file_type, ignore_word, max_file_size, os.path.join(root, filename), log_entries):
                    processed_files_count = process_single_file(root, filename, transform_content, outfile, processed_files_count, file_tree_lines, input_folder, log_entries)
        except PermissionError as e:
            log_entries.append(f"Permission denied: {root}. Skipping this directory.")
            print(f"Permission denied: {root}. Skipping this directory.")
    return processed_files_count, file_tree_lines, log_entries

def add_directory_to_file_tree(root, input_folder, file_tree_lines):
    """Adds the directory to the file tree."""
    relative_root = os.path.relpath(root, input_folder)
    if relative_root == '.':
        file_tree_lines.append(f"- {os.path.basename(input_folder)}/")
    else:
        file_tree_lines.append(f"{'  ' * relative_root.count(os.sep)}- {os.path.basename(root)}/")
    return file_tree_lines

def should_process_file(filename, file_type, ignore_word, max_file_size, file_path, log_entries):
    """Determines if a file should be processed based on the criteria."""
    if file_type and not filename.endswith(file_type):
        return False
    if ignore_word and ignore_word in filename:
        log_entries.append(f"Ignored: {filename} (contains '{ignore_word}')")
        return False
    if max_file_size and os.path.getsize(file_path) > max_file_size:
        log_entries.append(f"Ignored: {file_path} (size exceeds {max_file_size} bytes)")
        return False
    return True

def process_single_file(root, filename, transform_content, outfile, processed_files_count, file_tree_lines, input_folder, log_entries):
    """Processes a single file and writes its content to the output file."""
    file_path = os.path.join(root, filename)
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
            content = infile.read()
            if transform_content:
                content = transform_content(content)
            outfile.write(f"// Contents of {file_path}:\n")
            outfile.write(content)
            outfile.write("\n\n")  # Add a newline for separation between files
            processed_files_count += 1
            print(f"Processed: {file_path}")
            # Add the file to the file tree
            relative_root = os.path.relpath(root, input_folder)
            file_tree_lines.append(f"{'  ' * (relative_root.count(os.sep) + 1)}- {filename}")
    except PermissionError:
        log_entries.append(f"Permission denied: {file_path}. Skipping this file.")
        print(f"Permission denied: {file_path}. Skipping this file.")
    except Exception as e:
        log_entries.append(f"Error reading {file_path}: {e}")
        print(f"Error reading {file_path}: {e}")
    return processed_files_count

def write_footer(outfile, footer):
    """Writes the footer to the output file."""
    if footer:
        outfile.write("\n\n" + footer)

def generate_log_file(output_file, processed_files_count, log_entries):
    """Generates a log file with details of the processing."""
    log_file_path = output_file + ".log"
    with open(log_file_path, 'w') as log_file:
        log_file.write("\n".join(log_entries))
        log_file.write(f"\n\nTotal files processed: {processed_files_count}")
    print(f"Log file has been written to '{log_file_path}'.")

def generate_file_tree_file(file_tree_output, file_tree_lines):
    """Generates a file tree output file."""
    if file_tree_output:
        with open(file_tree_output, 'w') as tree_file:
            tree_file.write("\n".join(file_tree_lines))
        print(f"File tree has been written to '{file_tree_output}'.")

def write_titles_before_content(input_folder, output_file, file_type=None, ignore_word=None, max_file_size=None, transform_content=None):
    """
    Writes the titles of each file before its content.
    """
    try:
        validate_input_folder(input_folder)
        with open(output_file, 'w') as outfile:
            for root, dirs, files in os.walk(input_folder):
                for filename in files:
                    if should_process_file(filename, file_type, ignore_word, max_file_size, os.path.join(root, filename), []):
                        file_path = os.path.join(root, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                content = infile.read()
                                if transform_content:
                                    content = transform_content(content)
                                outfile.write(f"// {filename}\n")
                                outfile.write(content)
                                outfile.write("\n\n")
                                print(f"Processed: {file_path}")
                        except PermissionError:
                            print(f"Permission denied: {file_path}. Skipping this file.")
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")
        print(f"All files with titles have been written to '{output_file}'.")
    except Exception as e:
        print(f"Error: {e}")

def write_titles_with_tree_map(input_folder, output_file, file_type=None, ignore_word=None, max_file_size=None, transform_content=None):
    """
    Writes the titles with a tree map structure before the content.
    """
    try:
        validate_input_folder(input_folder)
        file_tree_lines = []
        with open(output_file, 'w') as outfile:
            for root, dirs, files in os.walk(input_folder):
                relative_root = os.path.relpath(root, input_folder)
                if relative_root == '.':
                    file_tree_lines.append(f"- {os.path.basename(input_folder)}/")
                else:
                    file_tree_lines.append(f"{'  ' * relative_root.count(os.sep)}- {os.path.basename(root)}/")

                for filename in files:
                    if should_process_file(filename, file_type, ignore_word, max_file_size, os.path.join(root, filename), []):
                        file_path = os.path.join(root, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                content = infile.read()
                                if transform_content:
                                    content = transform_content(content)
                                relative_path = os.path.relpath(file_path, input_folder)
                                outfile.write(f"// {relative_path}\n")
                                outfile.write(content)
                                outfile.write("\n\n")
                                print(f"Processed: {file_path}")

                                # Add file to the tree map
                                file_tree_lines.append(f"{'  ' * (relative_root.count(os.sep) + 1)}- {filename}")
                        except PermissionError:
                            print(f"Permission denied: {file_path}. Skipping this file.")
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

        with open(output_file + '.tree', 'w') as tree_file:
            tree_file.write("\n".join(file_tree_lines))
        print(f"All files with titles and tree map have been written to '{output_file}'. Tree map written to '{output_file}.tree'.")
    except Exception as e:
        print(f"Error: {e}")

def write_titles_with_tree_map_separated(input_folder, output_folder, file_type=None, ignore_word=None, max_file_size=None, transform_content=None):
    """
    Writes the titles with a tree map structure before the content, but separates each folder and its content into different text files.
    """
    try:
        validate_input_folder(input_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        file_tree_lines = []
        for root, dirs, files in os.walk(input_folder):
            relative_root = os.path.relpath(root, input_folder)
            folder_name = os.path.basename(root)
            output_file = os.path.join(output_folder, f"{folder_name}.txt")
            with open(output_file, 'w') as outfile:
                if relative_root == '.':
                    file_tree_lines.append(f"- {os.path.basename(input_folder)}/")
                else:
                    file_tree_lines.append(f"{'  ' * relative_root.count(os.sep)}- {os.path.basename(root)}/")
                
                for filename in files:
                    if should_process_file(filename, file_type, ignore_word, max_file_size, os.path.join(root, filename), []):
                        file_path = os.path.join(root, filename)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as infile:
                                content = infile.read()
                                if transform_content:
                                    content = transform_content(content)
                                relative_path = os.path.relpath(file_path, input_folder)
                                outfile.write(f"// {relative_path}\n")
                                outfile.write(content)
                                outfile.write("\n\n")
                                print(f"Processed: {file_path}")

                                # Add file to the tree map
                                file_tree_lines.append(f"{'  ' * (relative_root.count(os.sep) + 1)}- {filename}")
                        except PermissionError:
                            print(f"Permission denied: {file_path}. Skipping this file.")
                        except Exception as e:
                            print(f"Error reading {file_path}: {e}")

        with open(os.path.join(output_folder, 'file_tree.txt'), 'w') as tree_file:
            tree_file.write("\n".join(file_tree_lines))
        print(f"All files with titles and tree map have been written to separate files in '{output_folder}'. Tree map written to 'file_tree.txt'.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage:
input_folder = r"C:\Users\mario\Desktop\multiplayer-game-main"  # Replace with the path to your folder
output_folder = r"C:\Users\mario\Desktop\multiplayer-game-main-separate.txt"  # Replace with the path to your output folder
ignore_word = 'Assembly'  # Replace with the word to ignore in file names, or set to None
max_file_size = None  # Set max file size in bytes (e.g., 1MB), or set to None
transform_content = None  # Example transformation function (e.g., str.upper), or set to None

# Function call to write titles before content
write_titles_before_content(input_folder, output_folder, file_type=None, ignore_word=ignore_word, max_file_size=max_file_size, transform_content=transform_content)

# Function call to write titles with tree map
write_titles_with_tree_map(input_folder, output_folder, file_type=None, ignore_word=ignore_word, max_file_size=max_file_size, transform_content=transform_content)

# Function call to write titles with tree map separated by folders
#write_titles_with_tree_map_separated(input_folder, output_folder, file_type=None, ignore_word=ignore_word, max_file_size=max_file_size, transform_content=transform_content)

# Example usage:
#input_folder = r"C:\Users\mario\Desktop\multiplayer-game-main"  # Replace with the path to your folder
#output_file = r"C:\Users\mario\Desktop\multiplayer-game-main-readed.txt"  # Replace with the path to your output file
#ignore_word = 'Assembly'  # Replace with the word to ignore in file names, or set to None
#max_file_size = None  # Set max file size in bytes (e.g., 1MB), or set to None
#transform_content = None  # Example transformation function (e.g., str.upper), or set to None
# Example usage:
input_folder = r"C:\Users\mario\Desktop\ollama-python-main"  # Replace with the path to your folder
file_type = None                     # Set to None to include all file types, or specify a file type like '.cs'
output_file = r"C:\Users\mario\Desktop\ollama-python"   # Replace with the path to your output file
ignore_word = 'Assembly'                 # Replace with the word to ignore in file names, or set to None
max_file_size = None          # Set max file size in bytes (e.g., 1MB), or set to None
header = "This is a custom header"   # Custom header text, or set to None
footer = "This is a custom footer"   # Custom footer text, or set to None
transform_content = None             # Example transformation function (e.g., str.upper), or set to None
file_tree_output = r"C:\Users\mario\Desktop\ollama-python"  # Replace with the path to your file tree output file

# Function call to write titles before content
#write_titles_before_content(input_folder, output_file, file_type=None, ignore_word=ignore_word, max_file_size=max_file_size, transform_content=transform_content)

# Function call to write titles with tree map
write_titles_with_tree_map(input_folder, output_file, file_type=None, ignore_word=ignore_word, max_file_size=max_file_size, transform_content=transform_content)

#read_and_write_files_recursively(input_folder, file_type, output_file, ignore_word, max_file_size, header, footer, transform_content, file_tree_output)
