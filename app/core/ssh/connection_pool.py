class SSHConnectionPool:

    def __init__(self):

        self.connections = {}

    def get_connection(self, host):

        return self.connections.get(host)

    def add_connection(
        self,
        host,
        connection
    ):

        self.connections[host] = connection

    def close_all(self):

        for conn in self.connections.values():

            conn.close()

        self.connections.clear()