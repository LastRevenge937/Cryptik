from pathlib import Path
from crypto import encrypt_file, decrypt_file
from fs_core import has_access, FS_ROOT

# -----------------------------
# File import into Cryptik FS
# -----------------------------
def import_file(user_clearance: int, source_path: str, target_folder: str):
    """Move an external file into Cryptik FS and encrypt it."""
    source = Path(source_path)
    if not source.exists() or not source.is_file():
        raise FileNotFoundError(f"Source file does not exist: {source_path}")

    if not has_access(user_clearance, target_folder):
        raise PermissionError(f"Insufficient clearance for folder: {target_folder}")

    dest_folder = FS_ROOT / target_folder
    dest_folder.mkdir(exist_ok=True)

    dest = dest_folder / source.name

    if source.name == "KEEP_EMPTY_FOLDER.txt":
        raise ValueError("Cannot import placeholder files.")

    # Move and encrypt
    source.rename(dest)
    encrypt_file(dest)
    print(f"File '{source.name}' imported and encrypted into '{target_folder}'.")

# -----------------------------
# Interactive import prompt
# -----------------------------
def interactive_import(user_clearance: int):
    intake_folder = Path(__file__).resolve().parents[1] / "intake"
    intake_files = [f for f in intake_folder.iterdir() if f.is_file() and f.name != "KEEP_EMPTY_FOLDER.txt"]

    if not intake_files:
        print("No files in intake folder to import.")
        return

    print("Files available for import:")
    for i, f in enumerate(intake_files, start=1):
        print(f"{i}. {f.name}")

    choice = input("Select file number to import: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(intake_files):
        print("Invalid choice.")
        return

    selected_file = intake_files[int(choice) - 1]
    folder_choice = input("Target folder (confidential/secret/top_secret): ").strip()

    try:
        import_file(user_clearance, str(selected_file), folder_choice)
    except Exception as e:
        print(f"Error: {e}")

# -----------------------------
# File access / decryption
# -----------------------------
def access_file(user_clearance: int, folder_name: str, file_name: str) -> bytes:
    """Return decrypted content if user has clearance."""
    if not has_access(user_clearance, folder_name):
        raise PermissionError(f"Insufficient clearance for folder: {folder_name}")

    file_path = FS_ROOT / folder_name / file_name
    if not file_path.exists() or not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_name}")

    if file_path.name == "KEEP_EMPTY_FOLDER.txt":
        raise ValueError("Cannot access placeholder file.")

    return decrypt_file(file_path)

# -----------------------------
# Interactive access prompt
# -----------------------------
def interactive_access(user_clearance: int):
    folders = [f.name for f in FS_ROOT.iterdir() if f.is_dir() and has_access(user_clearance, f.name)]
    if not folders:
        print("No accessible folders.")
        return

    print("Accessible folders:")
    for f in folders:
        print(f"- {f}")

    folder_name = input("Select folder: ").strip()
    if folder_name not in folders:
        print("Invalid folder or insufficient clearance.")
        return

    folder_path = FS_ROOT / folder_name
    files = [f.name for f in folder_path.iterdir() if f.is_file() and f.name != "KEEP_EMPTY_FOLDER.txt"]

    if not files:
        print("No files available.")
        return

    print("Files available:")
    for i, fname in enumerate(files, start=1):
        print(f"{i}. {fname}")

    choice = input("Select file number to access: ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(files):
        print("Invalid choice.")
        return

    selected_file = files[int(choice) - 1]
    content = access_file(user_clearance, folder_name, selected_file)
    print(f"\n--- Decrypted content of {selected_file} ---")
    print(content.decode(errors='ignore'))

# -----------------------------
# Optional: import/export all files at once
# -----------------------------
def bulk_import(user_clearance: int):
    intake_folder = Path(__file__).resolve().parents[1] / "intake"
    for f in intake_folder.iterdir():
        if f.is_file() and f.name != "KEEP_EMPTY_FOLDER.txt":
            folder_choice = input(f"Target folder for '{f.name}': ").strip()
            try:
                import_file(user_clearance, str(f), folder_choice)
            except Exception as e:
                print(f"Error importing {f.name}: {e}")

