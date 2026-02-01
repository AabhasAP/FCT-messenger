from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
from app.core.config import settings


class MessageEncryption:
    """Handle message encryption and decryption using AES-256."""
    
    def __init__(self):
        # Derive a key from the encryption key setting
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'forensic_messenger_salt',  # In production, use a random salt per workspace
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(settings.ENCRYPTION_KEY.encode()))
        self.cipher = Fernet(key)
    
    def encrypt(self, plaintext: str) -> str:
        """Encrypt a message."""
        if not plaintext:
            return ""
        encrypted = self.cipher.encrypt(plaintext.encode())
        return base64.urlsafe_b64encode(encrypted).decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Decrypt a message."""
        if not ciphertext:
            return ""
        try:
            decoded = base64.urlsafe_b64decode(ciphertext.encode())
            decrypted = self.cipher.decrypt(decoded)
            return decrypted.decode()
        except Exception as e:
            # Log the error in production
            raise ValueError(f"Failed to decrypt message: {str(e)}")


# Global encryption instance
encryption = MessageEncryption()
