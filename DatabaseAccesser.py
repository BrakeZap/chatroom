import mariadb
import sys
import hashlib

class Database:
    def __init__(self):
        try:
            #TODO: Change to actual database credentials
            self.conn = mariadb.connect(
            user="root",
            password="cats56",
            host="localhost",
            port=3306,
            database="logininfo"

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

        # Get Cursor
        self.cur = self.conn.cursor()


    def checkUsername(self, username):
        self.cur.execute("SELECT Username FROM users where Username=?", (username,))
        for user in self.cur:
            if user == username:
                return True

        return False

    def checkPassword(self, username, password):
        #TODO: Implement try catch here later
        convertedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.cur.execute("SELECT Password FROM users where Username=?", (username,))
        for entry in self.cur:
            if entry == convertedPass:
                return True

        return False

    
    def insertUser(self, username, password):
        convertedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        #Implement try catch here later
        self.cur.execute("INSERT INTO users (Username, Password) VALUES (?, ?)", (username, convertedPass))


    def closeConnection(self):
        self.conn.close()
