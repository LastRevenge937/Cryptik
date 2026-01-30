import json
import hashlib
from pathlib import Path

USERS_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"

def authenticate(username: str, password: str) -> int:
    """Verify user credentials and return clearance."""
    if not USERS_FILE.exists():
        raise RuntimeError("users.json not found")

    with open(USERS_FILE, "r") as f:
        users = json.load(f)

    user = users.get(username)
    if not user:
        raise PermissionError("Invalid user")

    password_hash = hashlib.sha256(password.encode()).hexdigest()
    if password_hash != user["password_hash"]:
        raise PermissionError("Invalid password")

    return user["clearance"]

def create_admin():
    """First-run admin setup."""
    import getpass

    username = input("Create admin username: ").strip()
    while not username:
        username = input("Username cannot be empty. Enter admin username: ").strip()

    password = getpass.getpass("Create admin password: ")
    confirm = getpass.getpass("Confirm password: ")

    while password != confirm or not password:
        print("Passwords do not match or are empty. Try again.")
        password = getpass.getpass("Create admin password: ")
        confirm = getpass.getpass("Confirm password: ")

    clearance = 3  # top_secret for admin

    # Save to users.json
    if USERS_FILE.exists():
        with open(USERS_FILE, "r") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    users[username] = {
        "password_hash": hashlib.sha256(password.encode()).hexdigest(),
        "clearance": clearance
    }

    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

    print(f"Admin user '{username}' created with clearance {clearance}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "-c":
        create_admin()
    else:
        username = input("Username: ")
        import getpass
        password = getpass.getpass("Password: ")

        try:
            clearance = authenticate(username, password)
            print(f"Authenticated. Clearance level: {clearance}")
        except Exception as e:
            print(f"Authentication failed: {e}")
            sys.exit(1)
