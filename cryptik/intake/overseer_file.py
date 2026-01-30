from scripts.auth import authenticate
from scripts.overseer import interactive_import

# Example: login first
user = input("Username: ")
from getpass import getpass
password = getpass("Password: ")

clearance = authenticate(user, password)

# Run interactive overseer
interactive_import(clearance)

from crypto import encrypt_file

# After moving the file
encrypt_file(dest)
print(f"File '{source.name}' imported and encrypted in '{target_folder}'.")
