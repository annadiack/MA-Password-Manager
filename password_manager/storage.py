"""
Speicher-Modul für Passwörter.

Dieses Modul verwaltet die Speicherung und das Laden von Passworteinträgen
in einer JSON-Datei mit verschlüsselten Werten.
"""

import json
import os
from pathlib import Path
from typing import Optional, List
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class PasswordEntry:
    """Datenstruktur für einen Passwort-Eintrag."""
    service: str
    username: str
    password: str  # Verschlüsselt
    created_at: str
    updated_at: str
    notes: str = ""


class StorageManager:
    """Verwaltet die Speicherung von Passworteinträgen."""
    
    DATA_DIR = Path.home() / ".password_manager"
    DATA_FILE = DATA_DIR / "passwords.json"
    MASTER_HASH_FILE = DATA_DIR / "master.hash"
    
    def __init__(self):
        """Initialisiert den Storage-Manager und erstellt Verzeichnis falls nötig."""
        self.DATA_DIR.mkdir(exist_ok=True)
    
    def load_entries(self) -> List[PasswordEntry]:
        """
        Lädt alle Passworteinträge aus der Speicherdatei.
        
        Returns:
            Liste der PasswordEntry-Objekte
        """
        if not self.DATA_FILE.exists():
            return []
        
        try:
            with open(self.DATA_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [PasswordEntry(**entry) for entry in data]
        except (json.JSONDecodeError, TypeError):
            return []
    
    def save_entries(self, entries: List[PasswordEntry]) -> None:
        """
        Speichert Passworteinträge in die Datei.
        
        Args:
            entries: Liste der zu speichernden Einträge
        """
        with open(self.DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([asdict(entry) for entry in entries], f, indent=2, ensure_ascii=False)
        
        # Dateiberechtigungen einschränken (nur Besitzer)
        os.chmod(self.DATA_FILE, 0o600)
    
    def add_entry(self, entry: PasswordEntry) -> None:
        """
        Fügt einen neuen Eintrag hinzu oder aktualisiert einen bestehenden.
        
        Args:
            entry: PasswordEntry-Objekt
        """
        entries = self.load_entries()
        
        # Prüfe auf existierenden Eintrag
        existing_index = None
        for i, e in enumerate(entries):
            if e.service.lower() == entry.service.lower():
                existing_index = i
                break
        
        if existing_index is not None:
            entries[existing_index] = entry
        else:
            entries.append(entry)
        
        self.save_entries(entries)
    
    def get_entry(self, service: str) -> Optional[PasswordEntry]:
        """
        Ruft einen Eintrag für einen bestimmten Service ab.
        
        Args:
            service: Name des Services
            
        Returns:
            PasswordEntry oder None falls nicht gefunden
        """
        entries = self.load_entries()
        for entry in entries:
            if entry.service.lower() == service.lower():
                return entry
        return None
    
    def delete_entry(self, service: str) -> bool:
        """
        Löscht einen Eintrag für einen bestimmten Service.
        
        Args:
            service: Name des Services
            
        Returns:
            True falls gelöscht, False falls nicht gefunden
        """
        entries = self.load_entries()
        original_length = len(entries)
        
        entries = [e for e in entries if e.service.lower() != service.lower()]
        
        if len(entries) < original_length:
            self.save_entries(entries)
            return True
        return False
    
    def list_services(self) -> List[str]:
        """
        Gibt alle gespeicherten Service-Namen zurück.
        
        Returns:
            Liste der Service-Namen
        """
        entries = self.load_entries()
        return [entry.service for entry in entries]
    
    def save_master_hash(self, hash_value: str) -> None:
        """
        Speichert den Master-Passwort-Hash.
        
        Args:
            hash_value: SHA256-Hash des Master-Passworts
        """
        with open(self.MASTER_HASH_FILE, 'w', encoding='utf-8') as f:
            f.write(hash_value)
        os.chmod(self.MASTER_HASH_FILE, 0o600)
    
    def load_master_hash(self) -> Optional[str]:
        """
        Lädt den Master-Passwort-Hash.
        
        Returns:
            Hash-Wert oder None falls nicht gespeichert
        """
        if not self.MASTER_HASH_FILE.exists():
            return None
        
        with open(self.MASTER_HASH_FILE, 'r', encoding='utf-8') as f:
            return f.read().strip()
    
    def get_current_timestamp(self) -> str:
        """
        Gibt den aktuellen Zeitstempel im ISO-Format zurück.
        
        Returns:
            ISO-Format Zeitstempel
        """
        return datetime.now().isoformat()
