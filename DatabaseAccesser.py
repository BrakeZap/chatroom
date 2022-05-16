import json
import os.path

import mariadb
import sys
import hashlib


class Database:
    def __init__(self):
        with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "info.json")) as jsonFile:
            data = json.load(jsonFile)
        try:
            # TODO: Change to actual database credentials
            self.conn = mariadb.connect(
                user=data["database_user"],
                password=data["database_pass"],
                host=data["host"],
                port=data["port"],
                database=data["database"]

            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)
        print("Successfully connected to database")
        # Get Cursor
        self.cur = self.conn.cursor()

    def checkPassword(self, username, password):
        # TODO: Implement try catch here later
        convertedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.cur.execute("SELECT Password FROM users where Username=?", (username,))
        for entry in self.cur:
            if entry[0] == convertedPass:
                return True

        return False

    def insertUser(self, username, password):
        convertedPass = hashlib.sha256(password.encode('utf-8')).hexdigest()
        try:
            self.cur.execute("INSERT INTO users (Username, Password) VALUES (?, ?)", (username, convertedPass))
        except mariadb.Error as e:
            print(f"Error: {e}")
            self.conn.close()
            sys.exit(1)
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()
