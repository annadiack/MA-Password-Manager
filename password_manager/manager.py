"""
Hauptmanager für den Passwortmanager.

Dieses Modul orchestriert alle Funktionen des Passwortmanagers:
Speichern, Abrufen, Generieren von Passwörtern.
"""

from typing import Optional
from .crypto import CryptoManager, hash_password
from .storage import StorageManager, PasswordEntry
from .generator import PasswordGenerator


class PasswordManager:
    """Hauptklasse für die Passwortmanagement-Logik."""
    
    def __init__(self, master_password: str):
        """
        Initialisiert den Passwortmanager mit einem Master-Passwort.
        
        Args:
            master_password: Das Master-Passwort zur Verschlüsselung
        """
        self.master_password = master_password
        self.storage = StorageManager()
    
    def save_password(self, service: str, username: str, password: str, notes: str = "") -> None:
        """
        Speichert ein Passwort für einen Service.
        
        Args:
            service: Name des Services (z.B. "Gmail", "GitHub")
            username: Benutzername/E-Mail
            password: Das zu speichernde Passwort
            notes: Optionale Notizen
        """
        # Passwort verschlüsseln
        encrypted_password = CryptoManager.encrypt(password, self.master_password)
        
        # Eintrag erstellen
        timestamp = self.storage.get_current_timestamp()
        entry = PasswordEntry(
            service=service,
            username=username,
            password=encrypted_password,
            created_at=timestamp,
            updated_at=timestamp,
            notes=notes
        )
        
        # Speichern
        self.storage.add_entry(entry)
    
    def get_password(self, service: str) -> Optional[dict]:
        """
        Ruft ein gespeichertes Passwort für einen Service ab.
        
        Args:
            service: Name des Services
            
        Returns:
            Dict mit Service, Username und Passwort, oder None falls nicht gefunden
        """
        entry = self.storage.get_entry(service)
        if entry is None:
            return None
        
        try:
            # Passwort entschlüsseln
            decrypted_password = CryptoManager.decrypt(entry.password, self.master_password)
            
            return {
                "service": entry.service,
                "username": entry.username,
                "password": decrypted_password,
                "notes": entry.notes,
                "created_at": entry.created_at,
                "updated_at": entry.updated_at
            }
        except ValueError as e:
            return None
    
    def delete_password(self, service: str) -> bool:
        """
        Löscht einen Passwort-Eintrag.
        
        Args:
            service: Name des Services
            
        Returns:
            True falls gelöscht, False falls nicht gefunden
        """
        return self.storage.delete_entry(service)
    
    def list_all_services(self) -> list:
        """
        Listet alle gespeicherten Services auf.
        
        Returns:
            Liste der Service-Namen
        """
        return self.storage.list_services()
    
    def generate_password(
        self,
        length: int = 16,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True
    ) -> str:
        """
        Generiert ein neues starkes Passwort.
        
        Args:
            length: Passwortlänge
            use_lowercase: Kleinbuchstaben
            use_uppercase: Großbuchstaben
            use_digits: Zahlen
            use_special: Sonderzeichen
            
        Returns:
            Generiertes Passwort
        """
        return PasswordGenerator.generate(
            length=length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special=use_special
        )
    
    def check_master_password(self, password: str) -> bool:
        """
        Prüft ob das eingegebene Passwort dem Master-Passwort entspricht.
        
        Args:
            password: Zu prüfendes Passwort
            
        Returns:
            True falls korrekt
        """
        return password == self.master_password
    
    @staticmethod
    def is_first_launch() -> bool:
        """
        Prüft ob dies die erste Ausführung ist.
        
        Returns:
            True falls keine Master-Hash gefunden
        """
        storage = StorageManager()
        return storage.load_master_hash() is None
    
    @staticmethod
    def verify_master_password(password: str) -> bool:
        """
        Verifiziert das Master-Passwort gegen den gespeicherten Hash.
        
        Args:
            password: Zu verifizierendes Passwort
            
        Returns:
            True falls korrekt
        """
        storage = StorageManager()
        stored_hash = storage.load_master_hash()
        
        if stored_hash is None:
            return True  # Erste Ausführung
        
        return hash_password(password) == stored_hash
    
    @staticmethod
    def setup_master_password(password: str) -> None:
        """
        Speichert den Master-Passwort-Hash für zukünftige Verifizierungen.
        
        Args:
            password: Das Master-Passwort
        """
        storage = StorageManager()
        password_hash = hash_password(password)
        storage.save_master_hash(password_hash)
