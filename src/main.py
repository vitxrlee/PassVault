from src import *
import random
import string
from sys import exit
import os
import getpass
import sqlite3
from base64 import b64encode
from backports.pbkdf2 import pbkdf2_hmac
import binascii


class Vault:
    @staticmethod
    def exit_program() -> None:
        """
        Exit the program and close the database connection
        """
        return "[red]Exiting the program...[/red]"

    def __init__(self) -> None:
        """
        Initialize the Vault class

        Variables:
            master_password (str) - master password
            conn (sqlite3.Connection) - database connection
            cursor (sqlite3.Cursor) - database cursor
            xmark_ (str) - x mark
            checkmark_ (str) - check mark
        """
        self.master_password  = None
        self.conn = self.connect_database()
        self.cursor = self.conn.cursor()
        self.xmark_ = '\u2717'
        self.checkmark_ = '\u2713'
    
    def connect_database(self):
        """
        Connect to the database. Use the name of the 
        user as the name of the database.

        Return: 
            (sqlite3.Connection) - database connection
        """
        try:
            self.conn = sqlite3.connect(f'./PassVault/{getpass.getuser()}.db')
            return self.conn
        except sqlite3.OperationalError:
            self.conn = sqlite3.connect(f'./{getpass.getuser()}.db')
            return self.conn

    def cursor_connection(self):
        """
        Try to connect with the database masterpassword table

        Return:
            (tuple) - master password and salt
        """
        try: 
            self.cursor.execute("SELECT * FROM masterpassword")
            for i in self.cursor.fetchall():
                stored_password = i[0]
                salt = i[1]

            return stored_password, salt
        
        except sqlite3.Error as e:
            raise sqlite3.Error from e

    def verificantion(self, verify, salt, stored_password) -> None:
        """
        Verify and register the user

        Args: 
            verify (bool) - verify if the user is registered
            salt (str) - salt to encrypt the master password
            stored_password (str) - master password stored in the database
        
        Return:
            (str) - master password
        """
        if verify:
            self.master_password = getpass.getpass("Enter the master password: ").strip()
            encode_masterpassword = self.master_password.encode("utf-8")
            encode_salt = str(salt).encode()

            if b64encode(pbkdf2_hmac("sha3-512", encode_masterpassword, encode_salt, 500000)).decode() == stored_password:
                print(f'[green]{self.checkmark_} Logged with success![/green]')
                key = pbkdf2_hmac("sha3-256", encode_masterpassword, encode_salt, 500000, 16)
                self.master_password = binascii.hexlify(key).decode()

                while True:
                    menu = TerminalMenu(self.master_password, Vault())
                    menu.begin_program()
                    input("Press enter to return... ")
                    os.system("cls" if os.name == "nt" else "clear")

            else:
                print(f'[red]{self.xmark_} The master password is not correct[/red]')
                return self.main()

        else: 
            print('[green]To start, you have to create a master password. Be careful not to lose it as it is unrecoverable[/green]')
            self.master_password = getpass.getpass("Create a master password to use the program: ").strip()
            verify_master = getpass.getpass("Enter your master password again to verify it: ").strip()

            if self.master_password == verify_master:
                if self.master_password.isnumeric() or self.master_password.isspace():
                    print(f'\n[red]{self.checkmark_} The password is not correct. Please try again[/red]')
                    return self.main()

                elif len(self.master_password) < 8:
                    print(f'\n[red]{self.xmark_} The password must have at least 8 caracters.[/red]')
                    return self.main()

                else:
                    self.table_raise()

            else:
                print(f'\n[red]{self.checkmark_} Password do not match. Please try again.[/red]')
                return self.main()

    def table_raise(self) -> None:
        """
        In case the user has not yet created a master password, 
        create the table and insert the master password.

        Return: 
            (str) - master password
        """
        self.cursor.execute("CREATE TABLE IF NOT EXISTS masterpassword (password TEXT NOT NULL, salt TEXT NOT NULL);")
        salt = "".join(
            random.choice(
                string.ascii_uppercase + 
                string.digits + 
                string.ascii_lowercase
            ) for _ in range(32)
        )
        masterpassword_b64encode = b64encode(
            pbkdf2_hmac(
                "sha3-512", self.master_password.encode("utf-8"), salt.encode(), 500000
            )
        ).decode()
        self.cursor.execute(f"INSERT INTO masterpassword VALUES('{masterpassword_b64encode}', '{salt}')")
        self.conn.commit()
        print(f"\n[green]{self.checkmark_} Thank you! Restart the program and enter your master password to begin.[/green]")

    def main(self) -> None:
        """
        Main function to start register and verification
        """
        try: 
            stored_password, salt = self.cursor_connection()
            self.verificantion(True, salt, stored_password)
        except sqlite3.Error:
            self.verificantion(False, None, None)
    