import psycopg2

class Connection(object):

    def __init__(self):

        self._database = "bjp19"
        self._host = "cloud-vm-42-77.doc.ic.ac.uk"
        self._user = "bjp19"
        self._port = "5432"
        self._connected = False

        # for system specific tests
        self.has_connected = False
        self.has_disconnected = False
        self.crime_type_queried = False
        self.crime_location_queried = False
        self.crime_date_queried = False

    def connect(self):

        try:

            self.connection = psycopg2.connect(user=self._user,
                                               password="bjp19123",
                                               host=self._host,
                                               port=self._port,
                                               database=self._database)

            self.cursor = self.connection.cursor()
            # Print PostgreSQL Connection properties
           # print(self.connection.get_dsn_parameters(), "\n")

            # Print PostgreSQL version
            self.cursor.execute("SELECT version();")
            self.record = self.cursor.fetchone()
            print("You are connected to - ", self.record, "\n")
            self._connected = True
            self.has_connected = True

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            self._connected = False

    def disconnect(self):
        # closing database connection.
        if self.connection:
            self.cursor.close()
            self.connection.close()
            #print("PostgreSQL connection is closed")
            self._connected = False
            self.has_disconnected = True

    def connection(self):
        return self.connection

    def connected(self):
        return self._connected

    def database(self):
        return self._database

    def user(self):
        return self._user

    def host(self):
        return self._host

    def __repr__(self):
        return "a"
