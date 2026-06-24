"""
Kryptografische Funktionen für den Passwortmanager.

Dieses Modul bietet Verschlüsselung und Entschlüsselung von Passwörtern
mittels AES-256-GCM Verschlüsselung.
"""

import os
import hashlib
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives import hashes


class CryptoManager:
    """Verwaltet Verschlüsselung und Entschlüsselung von Daten."""
    
    SALT_SIZE = 16  # Bytes
    NONCE_SIZE = 12  # Bytes für GCM
    KEY_SIZE = 32  # 256-bit für AES-256
    ITERATIONS = 480000  # PBKDF2 Iterationen (OWASP empfohlen)
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> tuple:
        """
        Leitet einen kryptographischen Schlüssel vom Master-Passwort ab.
        
        Args:
            password: Das Master-Passwort
            salt: Optionales Salt (wird generiert, wenn nicht vorhanden)
            
        Returns:
            Tupel (schlüssel, salt)
        """
        if salt is None:
            salt = os.urandom(CryptoManager.SALT_SIZE)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=CryptoManager.KEY_SIZE,
            salt=salt,
            iterations=CryptoManager.ITERATIONS
        )
        
        key = kdf.derive(password.encode())
        return key, salt
    
    @staticmethod
    def encrypt(plaintext: str, password: str) -> str:
        """
        Verschlüsselt einen Plaintext mit dem Master-Passwort.
        
        Args:
            plaintext: Zu verschlüsselnder Text
            password: Master-Passwort
            
        Returns:
            Base64-kodierter verschlüsselter Text (salt + nonce + ciphertext + tag)
        """
        # Schlüssel ableiten
        key, salt = CryptoManager.derive_key(password)
        
        # Nonce generieren
        nonce = os.urandom(CryptoManager.NONCE_SIZE)
        
        # Verschlüsseln
        cipher = AESGCM(key)
        ciphertext = cipher.encrypt(nonce, plaintext.encode(), None)
        
        # Alles kombinieren: salt + nonce + ciphertext
        encrypted = salt + nonce + ciphertext
        
        # Base64-kodiert zurückgeben
        return base64.b64encode(encrypted).decode('utf-8')
    
    @staticmethod
    def decrypt(ciphertext_b64: str, password: str) -> str:
        """
        Entschlüsselt einen verschlüsselten Text mit dem Master-Passwort.
        
        Args:
            ciphertext_b64: Base64-kodierter verschlüsselter Text
            password: Master-Passwort
            
        Returns:
            Entschlüsselter Plaintext
            
        Raises:
            ValueError: Wenn Entschlüsselung fehlschlägt
        """
        try:
            # Dekodieren
            encrypted = base64.b64decode(ciphertext_b64)
            
            # Teile extrahieren
            salt = encrypted[:CryptoManager.SALT_SIZE]
            nonce = encrypted[CryptoManager.SALT_SIZE:CryptoManager.SALT_SIZE + CryptoManager.NONCE_SIZE]
            ciphertext = encrypted[CryptoManager.SALT_SIZE + CryptoManager.NONCE_SIZE:]
            
            # Schlüssel mit gleicher Salt ableiten
            key, _ = CryptoManager.derive_key(password, salt)
            
            # Entschlüsseln
            cipher = AESGCM(key)
            plaintext = cipher.decrypt(nonce, ciphertext, None)
            
            return plaintext.decode('utf-8')
        except Exception as e:
            raise ValueError(f"Entschlüsselung fehlgeschlagen: {str(e)}")


def hash_password(password: str) -> str:
    """
    Erstellt einen SHA256-Hash eines Passworts zur Verifizierung.
    
    Args:
        password: Zu hashendes Passwort
        
    Returns:
        Hexadezimale Hash-Darstellung
    """
    return hashlib.sha256(password.encode()).hexdigest()
