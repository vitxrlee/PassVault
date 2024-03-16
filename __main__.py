from src import *
from sys import exit

try:
    import Crypto
    import requests
    import rich
    import backports.pbkdf2
    
except ImportError as i:
    exit(f"[ERROR - {i}] Please install the required modules before running this program.")

if __name__ == '__main__':
    Vault().main()
