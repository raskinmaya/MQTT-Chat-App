from cryptography.fernet import Fernet

FERNET_KEY = Fernet.generate_key()
cipher = Fernet(FERNET_KEY)

def encrypt_message(message: str) -> str:
    return cipher.encrypt(message.encode()).decode()

def decrypt_message(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()
