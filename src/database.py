from src import *


class Database:
    """
    Database is the class which contains database SQlite
    functions.
    
    If has an error which should not exist, please report 
    it at https://github.com/vlHan/PassVault/issues
    """

    def __init__(self, master_pssw: str, obj) -> None:
        """
        Args:
            obj (class) - create instance of a class
            master_pw (str) - master password
        
        Return: 
            Database SQlite functions
        """
        self.master_pw = master_pssw
        self.obj_ = obj
        self.query_command(
            """CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                platform TEXT NOT NULL,
                email TEXT NOT NULL, 
                password TEXT NOT NULL, 
                url TEXT NOT NULL
            );"""
        )
        self.encryption = Encryption()
    
    def query_command(self, sql: str, *args: object):
        """
        Query commands 

        Args:
            sql (str) - sqlite command
        
        Return: 
            sqlite command
        """
        return self.obj_.cursor.execute(sql, *args)
    
    def select_all(self, table: str) -> list:
        """
        Select all 

        Args: 
            table (str) - the table to be selected
            star (str) - what select from the table
        
        Return: 
            All datas from the table
        """
        return self.query_command(f"SELECT * FROM {table}")
    
    def update_where(self, value: str, new: str, id_opt: str) -> None:
        """
        Update somewhere

        Args: 
            value (str) - the value to update
            new (str) - new data to be informed
            id_opt (str) - the id to be selected
        
        Return:
            The value updated
        """
        self.query_command(f"UPDATE passwords SET {value} = '{new}' WHERE id = '{id_opt}'")
        self.obj_.conn.commit()
        
    def delete_where(self, id_opt: str) -> None:
        """
        Delete somewhere 

        Args: 
            id_opt (str) - the id to be deleted
        
        Return:
            The value deleted
        """
        self.query_command(f"DELETE FROM passwords WHERE id = '{id_opt}'")
        self.obj_.conn.commit()

    def drop_table(self, table: str) -> None: 
        """
        Drop tables

        Args: 
            table (str) - table to be deleted
        
        Return: 
            The table deleted
        """
        self.query_command(f"DROP TABLE {table}")
        self.obj_.conn.commit()

    def verify_id(self, id_opt: str):
        """
        Verify if the ID is correct 

        Args:
            id_opt (str) - the id informed
        
        Return:
            The ID is correct or not
        """
        id_list = [row[0] for row in self.select_all('passwords')]
        if id_opt not in str(id_list): 
            return print(f"[red]{self.obj_.xmark_} The ID is not correct[/]")

    def save_password(self, platform: str, mail: str, password: str, url: str) -> None:
        """
        Add values in the Database SQlite.

        Args: 
            platform (str) - the platform of the password
            mail (str) - email of the account
            password (str) - password of the account to save in the database
            url (str) - URL of the platform
        
        Return 
            Sensitives datas saved in the SQLite.
        """
        id_db = len(self.query_command("SELECT id FROM passwords;").fetchall())
        while True:
            if id_db in self.query_command("SELECT id FROM passwords;"):
                id_db += 1
            else: 
                id_db += 1
                break

        datas = []
        stored_infos = [platform, mail, password, url]
        
        for i in stored_infos:
            tag, nonce, concatenate_encrypted = self.encryption.encrypt(i, self.master_pw)
            concatenate = f'{tag}|{nonce}|{concatenate_encrypted}'
            datas.append(concatenate)

        self.query_command(f"INSERT INTO passwords VALUES('{id_db}', '{datas[0]}', '{datas[1]}', '{datas[2]}', '{datas[3]}')")
        self.obj_.conn.commit()
        print(f"[green]\n{self.obj_.checkmark_} Thank you! Datas were successfully added.[/green]")

    def edit_password(self, new: str, option: str, id_opt: str ) -> None:
        """
        Update values in the database SQlite.

        Args:: 
            option (str) - what need to be changed
            new (str) - the new password
            id (str) - the id of the data

        Return
            (str) The new password changed in the database
        """
        self.verify_id(id_opt)
        tag, nonce, concatenate = self.encryption.encrypt(new, self.master_pw)
        concatenate_new_info = f'{tag}|{nonce}|{concatenate}'
        self.update_where(option, concatenate_new_info, id_opt)
        print(f"[green]{self.obj_.checkmark_} The {option} of the ID {id_opt} has successfully changed to {new}.[/green]")

    def look_up(self, id_opt: str) -> str:
        """
        See all passwords stored in the database.

        Args: 
            id_opt (str) - the ID chosed

        Return
            (str) The passwords stored
        """
        self.verify_id(id_opt)
        infos = []
        for row in self.query_command(f"SELECT * FROM passwords WHERE id = '{id_opt}';"):
            infos.extend((row[1], row[2], row[3], row[4]))
            decrypted = [
                self.encryption.decrypt(
                    str(i).split("|")[0], 
                    str(i).split("|")[1],
                    str(i).split("|")[2],
                    self.master_pw
                )
                for i in infos
            ]
            infos.clear()
            return (
                f"\n[yellow][ID: {row[0]}] {decrypted[0]}[/yellow]\n"
                f"[green]Email: {decrypted[1]}\n"
                f"Password: {decrypted[2]}\n"
                f"URL: {decrypted[3]}[/green]\n"
            )

    def stored_passwords(self) -> None:
        """
        Stored passwords

        Return 
            (str) - List of passwords
        """
        if self.query_command("SELECT COUNT(*) from passwords;").fetchall()[0][0] == 0:
            # verify if the database is empty - cannot opperate in a empty database
            raise PermissionError

        print('[yellow]Current passwords stored:[/yellow]')
        infos = []
        for row in self.select_all('passwords'):
            infos.extend((row[1], row[2], row[3]))
            decrypted = [
                self.encryption.decrypt(
                    str(i).split("|")[0], 
                    str(i).split("|")[1],
                    str(i).split("|")[2],
                    self.master_pw
                )
                for i in infos
            ]
            infos.clear()
            print(f"[yellow][ID: {row[0]}] Platform: {decrypted[0]}[/yellow]")
        
    def delete_one_password(self, id_opt: str) -> None:
        """
        Delete one password

        Args: 
            id_opt (str) - the ID chosed
        
        Return: 
            (str) - The password deleted
        """
        self.verify_id(id_opt)
        self.delete_where(id_opt)
        print(f"[green]\n{self.obj_.checkmark_} The password was successfully deleted.\n[/green]")

    def delete_all_passwords(self) -> None:
        """
        Delete all passwords stored in the database

        Args:
            entered_master (str) - master password to verify 
        
        Return:
            (str) - All passwords deleted
        """
        if self.query_command("SELECT COUNT(*) from passwords;").fetchall()[0][0] == 0: 
            return print(f"[red]{self.obj_.xmark_} The database is empty. Try adding a password.[/]")

        self.drop_table('passwords')
        print(f"[green]{self.obj_.checkmark_} All normal passwords deleted successfully.[/green]")

    def delete_all_data(self):
        """
        Delete all data including the master password

        Return: 
            (str) - All data deleted
        """
        self.drop_table("passwords")
        self.drop_table("masterpassword")
