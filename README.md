# <a href="https://github.com/vitoryl/PassVault"><img src="https://imgur.com/ZTbAS6w.png"></a>

[![python](https://img.shields.io/badge/python->=3.7-blue.svg)](https://www.python.org) [![repo size](https://img.shields.io/github/repo-size/vitoryl/PassVault)](#) [![build](https://img.shields.io/badge/build-Passing-green)](#) [![license](https://img.shields.io/github/license/vitoryl/PassVault.svg)](LICENSE)

[![asciicast](https://asciinema.org/a/tJaauMOKBy6tp47KSDEQxkm3H.svg)](https://asciinema.org/a/tJaauMOKBy6tp47KSDEQxkm3H)

## What is this? 
Command-line password vault, for educational purposes, that stores localy, in AES encryption, your sensitives datas in a SQLite database (.db). This project was made to learn more about cryptography and **not for intended for actual use**.

## Installation
Clone this repository: `git clone https://github.com/vitoryl/PassVault.git` or <a href="https://github.com/vitoryl/PassVault/archive/refs/heads/main.zip">download zip</a>
- Enter the folder: `cd PassVault/`
- Install python3 and dependecies
  - Linux
    - `python3 -m pip install -r requirements.txt`
    - Finished!

  - Windows and macOS
    - [Python 3, download and install](https://www.python.org/downloads/)
    - `python -m pip install -r requirements.txt`
    - Finished!

## Usage
Use the following commands to run the program
```bash
Linux
  # in the diretory
  $ python3 .
    
  # out of the diretory
  $ python3 PassVault
    
Windows and macOS
  # in the diretory
  python .
    
  # out of the diretory
  python PassVault
```
**⚠️** The program needs all the files, be sure to have all the dependecies and files <a href="https://github.com/vitoryl/PassVault#installation">installed</a>.

## How It Works
When running, the program will ask to create a master password. This master password will be encrypted and this key will be used to indenty if the user is actually you, be sure you have saved, because the master password is **unrecoverable**.

### Hash Verification
To authenticate the user, they are prompted to create a master password (that is also used to decrypt data), which is then stored using HMAC autentication code (that use SHA3_512 Hash Function as the digest mod). Whenever the user is prompted to verify their master password, the password they enter is compared to the hash of the stored master password and access if granted if the two hashes match.

```py
try: # try to connect with the database
    self.cur.execute("SELECT * FROM masterpassword")
    for i in self.cur.fetchall():
        stored_master = i[0]
        salt = i[1] 

    self.master_pw = getpass.getpass("Enter the master password: ").strip()
            
    encode_masterpassword = self.master_pw.encode("utf-8")
    encode_salt = str(salt).encode()

    # compare two hashes
    if b64encode(pbkdf2_hmac("sha3-512", encode_masterpassword, encode_salt, 500000)).decode() == stored_master:
        # master password is correct

except sqlite3.Error: # if the connection does not work
    # rest of the program
```

### AES Encryption
The encryption method used in this program comes from the python library [PyCryptoDome](https://pypi.org/project/pycryptodome/). This program uses AES encryption methods to store sensitive data (in this case passwords) into a SQLite database.

### SQLite Functions
The SQLite database is used to store sensitive data, as mentioned above. This type of database was used instead of MySQL, as it is easily transported and lightweight. Despite being less secure, it can be easily used and manipulated, so it is possible to keep it in a backup, in case the database is localy lost, you only need the PassVault to be able to decrypt the passwords stored in your backup database.

Your informations is stored in a data base with the name of your machine in a table called `passwords` with your master password named `masterpassword`. The table `passwords` has 4 columns: `id`, `name`, `username` and `password`. The table `masterpassword` has 2 columns: `masterpassword` and `salt`.

## Contributing
Please read [CONTRIBUTING.md](docs/CONTRIBUTING.md) for details on our code of conduct.

## License 
This project is licensed under the MIT License, see the [LICENSE](https://github.com/vitoryl/PassVault/blob/master/LICENSE) file for details

[⬆ Back to top](https://github.com/vitoryl/PassVault#)<br>
