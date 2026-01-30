from pathlib import Path

# Cryptik filesystem root
FS_ROOT = Path(__file__).resolve().parents[1] / "fs"

# Map folder names to clearance levels
CLEARANCE_MAP = {
    "confidential": 1,
    "secret": 2,
    "top_secret": 3
}

def get_accessible_folders(user_clearance: int):
    """
    Return a list of folder names the user can access based on clearance.
    """
    accessible = []
    for folder, level in CLEARANCE_MAP.items():
        if user_clearance >= level:
            folder_path = FS_ROOT / folder
            if folder_path.exists():
                accessible.append(folder_path)
    return accessible

def list_files(user_clearance: int):
    """
    List all files in folders the user can access.
    Skips placeholder files like KEEP_EMPTY_FOLDER.txt.
    """
    accessible_folders = get_accessible_folders(user_clearance)
    files_list = []

    for folder_path in accessible_folders:
        for f in folder_path.iterdir():
            if f.is_file() and f.name != "KEEP_EMPTY_FOLDER.txt":
                files_list.append(f)
    return files_list

def has_access(user_clearance: int, folder_name: str) -> bool:
    """
    Check if the user has clearance to access a specific folder.
    """
    required_level = CLEARANCE_MAP.get(folder_name)
    if required_level is None:
        return False
    return user_clearance >= required_level
