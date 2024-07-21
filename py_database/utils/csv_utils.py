import csv

def read_csv(file_path):
    try:
        with open(file_path, newline="") as csv_file:
            csv_reader = csv.reader(csv_file)
            headers = next(csv_reader)
            rows = [row for row in csv_reader]
            return headers, rows
    except FileNotFoundError as e:
        print(f"File not found: {e}")
        return None, None
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return None, None

def write_csv(file_path, headers, rows):
    try:
        with open(file_path, 'w', newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            if headers:
                csv_writer.writerow(headers)
            csv_writer.writerows(rows)
        print(f"Data written to {file_path} successfully.")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

def append_to_csv(file_path, rows):
    try:
        with open(file_path, 'a', newline="") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(rows)
        print(f"Data appended to {file_path} successfully.")
    except Exception as e:
        print(f"Error appending to CSV file: {e}")
