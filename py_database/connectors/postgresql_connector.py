import psycopg2
from connectors.base_connector import BaseConnector

class PostgreSQLConnector(BaseConnector):
    def connect(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            print("Connected to PostgreSQL server")
        except psycopg2.Error as error:
            print("Error connecting to PostgreSQL:", error)
