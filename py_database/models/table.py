import json
import os
import csv
from utils.json_utils import read_json, write_json
from utils.csv_utils import read_csv, write_csv

class Table:
    def __init__(self, connection, database_name, name):
        self.connection = connection
        self.database_name = database_name
        self.name = name

    def show_structure(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DESCRIBE {self.database_name}.{self.name}")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        except Exception as error:
            print("Error:", error)

    def view_data(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.database_name}.{self.name}")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        except Exception as error:
            print("Error:", error)

    def insert_record(self, values):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO {self.database_name}.{self.name} VALUES ({values})")
                self.connection.commit()
                print("Record inserted successfully.")
        except Exception as error:
            print("Error inserting record:", error)

    def update_record(self, column, new_value, condition):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"UPDATE {self.database_name}.{self.name} SET {column} = %s WHERE {condition}", (new_value,))
                self.connection.commit()
                print("Record updated successfully.")
        except Exception as error:
            print("Error updating record:", error)

    def delete_record(self, condition):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"DELETE FROM {self.database_name}.{self.name} WHERE {condition}")
                self.connection.commit()
                print("Record deleted successfully.")
        except Exception as error:
            print("Error deleting record:", error)

    def view_specific_record(self, condition):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.database_name}.{self.name} WHERE {condition}")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        except Exception as error:
            print("Error:", error)

    def sort_data(self, column):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.database_name}.{self.name} ORDER BY {column}")
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        except Exception as error:
            print("Error:", error)

    def export_to_json(self, file_path):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.database_name}.{self.name}")
                rows = cursor.fetchall()
                write_json(file_path, rows)
            print("Data exported to JSON successfully.")
        except Exception as error:
            print("Error exporting to JSON:", error)

    def export_to_csv(self, file_path):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SELECT * FROM {self.database_name}.{self.name}")
                headers, rows = cursor.description, cursor.fetchall()
                write_csv(file_path, headers, rows)
            print("Data exported to CSV successfully.")
        except Exception as error:
            print("Error exporting to CSV:", error)

    def import_from_json(self, file_path):
        try:
            data = read_json(file_path)
            if data:
                column_names = data[0].keys()
                placeholders = ', '.join(['%s'] * len(column_names))
                query = f"INSERT INTO {self.database_name}.{self.name} ({', '.join(column_names)}) VALUES ({placeholders})"
                with self.connection.cursor() as cursor:
                    cursor.executemany(query, [tuple(record.values()) for record in data])
                    self.connection.commit()
                print("Data imported from JSON successfully.")
        except Exception as error:
            print("Error importing from JSON:", error)

    def import_from_csv(self, file_path):
        try:
            headers, rows = read_csv(file_path)
            if headers and rows:
                placeholders = ', '.join(['%s'] * len(headers))
                query = f"INSERT INTO {self.database_name}.{self.name} ({', '.join(headers)}) VALUES ({placeholders})"
                with self.connection.cursor() as cursor:
                    cursor.executemany(query, rows)
                    self.connection.commit()
                print("Data imported from CSV successfully.")
        except Exception as error:
            print("Error importing from CSV:", error)
