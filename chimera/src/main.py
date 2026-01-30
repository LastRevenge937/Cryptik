import sys
from datetime import datetime
from pathlib import Path
import configparser

NAME = "Химера"

LOG_PATH = Path("logs/chimera.log")
CONFIG_PATH = Path("configs/chimera.conf")

# ---------- logging ----------
def log_event(message):
    LOG_PATH.parent.mkdir(exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now().isoformat()}] {message}\n")

# ---------- config ----------
config = configparser.ConfigParser()

if not CONFIG_PATH.exists():
    print("[ERROR] Missing config file")
    log_event("Startup failed: missing config")
    sys.exit(1)

config.read(CONFIG_PATH)

ALLOWED_USERS = [
    u.strip()
    for u in config.get("DEFAULT", "users", fallback="").split(",")
    if u.strip()
]

MODE = config.get("DEFAULT", "mode", fallback="safe")

# ---------- lifecycle ----------
def wake(user):
    if user not in ALLOWED_USERS:
        msg = f"{NAME} denied wake by {user} (unauthorized)"
        print(msg)
        log_event(msg)
        return False

    msg = f"{NAME} awakened by {user} in mode: {MODE}"
    print(msg)
    log_event(msg)
    return True

def sleep():
    msg = f"{NAME} entering dormant state"
    print(msg)
    log_event(msg)

# ---------- main ----------
if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "unknown_user"
    session_id = datetime.now().strftime("%Y%m%d%H%M%S")

    print(f"Session ID: {session_id}")
    log_event(f"Session started: {session_id}")

    if wake(user):
        sleep()

