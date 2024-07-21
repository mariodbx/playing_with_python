import pyodbc
from connectors.base_connector import BaseConnector

class SQLServerConnector(BaseConnector):
    def connect(self):
        try:
            self.connection = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.host};UID={self.user};PWD={self.password}"
            )
            print("Connected to SQL Server")
        except pyodbc.Error as error:
            print("Error connecting to SQL Server:", error)
