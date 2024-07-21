import os
from utils.csv_utils import write_csv
from connectors.base_connector import BaseConnector

class Database:
    def __init__(self, connection: BaseConnector, name: str):
        self.connection = connection
        self.name = name

    def show_tables(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(f"SHOW TABLES IN {self.name}")
                tables = cursor.fetchall()
                for table in tables:
                    print(table[0])
        except Exception as error:
            print("Error:", error)

    def execute_query(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                for row in rows:
                    print(row)
        except Exception as error:
            print("Error:", error)

    def backup_schema(self, backup_folder):
        try:
            if not os.path.exists(backup_folder):
                os.makedirs(backup_folder)
            with self.connection.cursor() as cursor:
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT * FROM {table_name}")
                    rows = cursor.fetchall()
                    write_csv(os.path.join(backup_folder, f"{table_name}.csv"), None, rows)
            print("Schema backed up successfully.")
        except Exception as error:
            print("Error backing up schema:", error)
