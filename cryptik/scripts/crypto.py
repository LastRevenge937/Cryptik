from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

KEY_FILE = Path(__file__).resolve().parents[1] / "data" / "crypto_key.key"

# Generate or load key
def load_key():
    if KEY_FILE.exists():
        return KEY_FILE.read_bytes()
    else:
        key = get_random_bytes(32)  # AES-256
        KEY_FILE.write_bytes(key)
        return key

KEY = load_key()

def pad(data: bytes) -> bytes:
    # Pad to multiple of 16 bytes
    pad_len = 16 - len(data) % 16
    return data + bytes([pad_len] * pad_len)

def unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_file(file_path: Path):
    if file_path.name == "KEEP_EMPTY_FOLDER.txt":
        return  # skip placeholders

    data = file_path.read_bytes()
    cipher = AES.new(KEY, AES.MODE_ECB)  # simple mode for now
    encrypted = cipher.encrypt(pad(data))
    file_path.write_bytes(encrypted)

def decrypt_file(file_path: Path) -> bytes:
    if file_path.name == "KEEP_EMPTY_FOLDER.txt":
        return b""

    data = file_path.read_bytes()
    cipher = AES.new(KEY, AES.MODE_ECB)
    decrypted = unpad(cipher.decrypt(data))
    return decrypted
