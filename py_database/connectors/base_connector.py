class BaseConnector:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None

    def connect(self):
        raise NotImplementedError("Connect method not implemented.")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Disconnected from the database server")
