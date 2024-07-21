import mysql.connector
from connectors.base_connector import BaseConnector

class MySQLConnector(BaseConnector):
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            if self.connection.is_connected():
                print("Connected to MySQL server")
        except mysql.connector.Error as error:
            print("Error connecting to MySQL:", error)
