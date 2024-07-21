import os
from config.settings import DEFAULT_DB_TYPE, DEFAULT_HOST, DEFAULT_USER, DEFAULT_PASSWORD, DEFAULT_DATABASE
from connectors.mysql_connector import MySQLConnector
from connectors.postgresql_connector import PostgreSQLConnector
from connectors.sqlserver_connector import SQLServerConnector
from models.database import Database
from models.table import Table

def main():
    db_type = input("Enter database type (MySQL/PostgreSQL/SQLServer): ")
    host = input(f"Enter host (default: {DEFAULT_HOST}): ") or DEFAULT_HOST
    user = input(f"Enter user (default: {DEFAULT_USER}): ") or DEFAULT_USER
    password = input(f"Enter password (default: {DEFAULT_PASSWORD}): ") or DEFAULT_PASSWORD
    database_name = input(f"Enter database name (default: {DEFAULT_DATABASE}): ") or DEFAULT_DATABASE

    if db_type.lower() == 'mysql':
        db_connector = MySQLConnector(host, user, password)
    elif db_type.lower() == 'postgresql':
        db_connector = PostgreSQLConnector(host, user, password)
    elif db_type.lower() == 'sqlserver':
        db_connector = SQLServerConnector(host, user, password)
    else:
        print("Unsupported database type")
        return

    db_connector.connect()

    database = Database(db_connector.connection, database_name)
    database.show_tables()
    table_name = input("Enter table name: ")
    table = Table(db_connector.connection, database_name, table_name)

    print("\nSelect an option for table '{}':".format(table_name))
    print("1. View Structure")
    print("2. View Data")
    print("3. Insert Record")
    print("4. Update Record")
    print("5. Delete Record")
    print("6. View Specific Record")
    print("7. Sort Data")
    print("8. Export to JSON")
    print("9. Export to CSV")
    print("10. Import from JSON")
    print("11. Import from CSV")
    print("12. Backup Schema")
    print("13. Back to Main Menu")

    while True:
        try:
            option = int(input("Enter your choice: "))
            if option == 1:
                table.show_structure()
            elif option == 2:
                table.view_data()
            elif option == 3:
                values = input("Enter comma-separated values for new record: ")
                table.insert_record(values)
            elif option == 4:
                column = input("Enter column name to update: ")
                new_value = input("Enter new value: ")
                condition = input("Enter condition: ")
                table.update_record(column, new_value, condition)
            elif option == 5:
                condition = input("Enter condition: ")
                table.delete_record(condition)
            elif option == 6:
                condition = input("Enter condition: ")
                table.view_specific_record(condition)
            elif option == 7:
                column = input("Enter column name to sort by: ")
                table.sort_data(column)
            elif option == 8:
                file_path = input("Enter file path for JSON export: ")
                table.export_to_json(file_path)
            elif option == 9:
                file_path = input("Enter file path for CSV export: ")
                table.export_to_csv(file_path)
            elif option == 10:
                file_path = input("Enter file path for JSON import: ")
                table.import_from_json(file_path)
            elif option == 11:
                file_path = input("Enter file path for CSV import: ")
                table.import_from_csv(file_path)
            elif option == 12:
                backup_folder = input("Enter backup folder path: ")
                database.backup_schema(backup_folder)
            elif option == 13:
                break
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    db_connector.disconnect()

if __name__ == "__main__":
    main()
