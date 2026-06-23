# Technische Architektur

## Überblick

Der MA-Password-Manager ist in einer layered-Architektur aufgebaut mit klarer Separation of Concerns:

```
┌─────────────────────────────────────────┐
│    Benutzeroberfläche (UI-Layer)        │ ui.py
├─────────────────────────────────────────┤
│    Geschäftslogik (Business-Layer)      │ manager.py
├─────────────────────────────────────────┤
│  Kryptographie | Generator | Storage    │
│   crypto.py   | generator.py | storage.py
├─────────────────────────────────────────┤
│    Dateisystem / Kryptographische Libs  │
└─────────────────────────────────────────┘
```

## Module

### 1. `ui.py` - Benutzeroberfläche
**Zweck:** Interaktive Konsolenschnittstelle

**Klassen:**
- `PasswordManagerUI` - Verwaltet die Benutzerinteraktion

**Funktionen:**
- Menüanzeige und Benutzereingabe
- Dialoggestaltung für alle Operationen
- Farbige Ausgabe mit Colorama
- Master-Passwort-Setup und Authentifizierung

**Abhängigkeiten:**
- `manager.py` (PasswordManager)
- `generator.py` (PasswordGenerator)
- `colorama` (externe Bibliothek)

### 2. `manager.py` - Geschäftslogik
**Zweck:** Orchestriert alle Kernfunktionalitäten

**Klassen:**
- `PasswordManager` - Hauptklasse für Passwortmanagement

**Hauptmethoden:**
- `save_password()` - Speichert Passwörter verschlüsselt
- `get_password()` - Ruft gespeicherte Passwörter ab
- `delete_password()` - Löscht Einträge
- `list_all_services()` - Listet alle Services auf
- `generate_password()` - Delegiert an Generator
- `verify_master_password()` - Prüft Master-Passwort

**Abhängigkeiten:**
- `crypto.py` (Verschlüsselung)
- `storage.py` (Datenspeicherung)
- `generator.py` (Passwortgenerierung)

### 3. `crypto.py` - Verschlüsselung
**Zweck:** Kryptographische Operationen

**Klassen:**
- `CryptoManager` - Verwaltet AES-256-GCM Verschlüsselung

**Mechanismus:**
```
Plaintext (Passwort)
    ↓
[PBKDF2 mit Master-Passwort → Schlüssel]
[Zufälliges Nonce generieren]
[AES-256-GCM Verschlüsseln]
    ↓
Base64-kodiert (salt + nonce + ciphertext)
```

**Sicherheitsparameter:**
- **Algorithmus:** AES-256-GCM
- **Key-Ableitung:** PBKDF2 mit SHA-256
- **Iterationen:** 480,000 (OWASP empfohlen)
- **Salt-Größe:** 16 Bytes
- **Nonce-Größe:** 12 Bytes

**Funktionen:**
- `derive_key()` - Leitet kryptographischen Schlüssel ab
- `encrypt()` - Verschlüsselt Daten
- `decrypt()` - Entschlüsselt Daten
- `hash_password()` - SHA256-Hash für Master-Passwort

### 4. `generator.py` - Passwortgenerator
**Zweck:** Sichere Passwortgenerierung

**Klassen:**
- `PasswordGenerator` - Generiert und validiert Passwörter

**Funktionen:**
- `generate()` - Generiert Passwort mit konfigurierbaren Optionen
- `generate_strong()` - Generiert starkes Standard-Passwort
- `validate_strength()` - Bewertet Passwort-Stärke

**Zeichensätze:**
- Kleinbuchstaben (a-z)
- Großbuchstaben (A-Z)
- Zahlen (0-9)
- Sonderzeichen (!@#$%^&*...)

### 5. `storage.py` - Datenverwaltung
**Zweck:** Persistente Speicherung von Passworteinträgen

**Klassen:**
- `PasswordEntry` - Datenstruktur für einen Eintrag
- `StorageManager` - Verwaltet Dateispeicherung

**Speicherort:**
```
~/.password_manager/
├── passwords.json      # Passworteinträge (verschlüsselt)
└── master.hash         # SHA256-Hash des Master-Passworts
```

**Dateiberechtigungen:** 0o600 (nur Besitzer)

**Datenformat:**
```json
[
  {
    "service": "Gmail",
    "username": "user@example.com",
    "password": "<base64-encrypted>",
    "created_at": "2026-06-23T15:00:00",
    "updated_at": "2026-06-23T15:00:00",
    "notes": "Persönliches Konto"
  }
]
```

**Hauptmethoden:**
- `load_entries()` - Lädt alle Einträge
- `save_entries()` - Speichert Einträge
- `add_entry()` - Fügt Eintrag hinzu/aktualisiert
- `get_entry()` - Ruft einzelnen Eintrag ab
- `delete_entry()` - Löscht Eintrag
- `list_services()` - Listet Service-Namen auf

## Datenfluss

### Passwort speichern
```
UI-Input (Service, User, Passwort)
    ↓
PasswordManager.save_password()
    ↓
CryptoManager.encrypt() [Verschlüsselung]
    ↓
PasswordEntry erstellen
    ↓
StorageManager.add_entry() [JSON speichern]
```

### Passwort abrufen
```
UI-Input (Service-Name)
    ↓
PasswordManager.get_password()
    ↓
StorageManager.get_entry()
    ↓
CryptoManager.decrypt() [Entschlüsselung]
    ↓
UI-Output (Service, User, Passwort)
```

### Passwort generieren
```
UI-Input (Länge, Optionen)
    ↓
PasswordManager.generate_password()
    ↓
PasswordGenerator.generate()
    ↓
Zufällige Zeichenauswahl
    ↓
UI-Output (Generiertes Passwort)
    ↓
Optional: Speichern
```

## Sicherheitskonzepte

### 1. Verschlüsselung
- **Transport-Verschlüsselung:** AES-256-GCM
- **Authentifizierung:** AESGCM-Tag verhindert Manipulation
- **Key-Derivation:** PBKDF2 mit 480,000 Iterationen

### 2. Master-Passwort
- SHA256-Hash wird lokal gespeichert
- Nicht reversibel - nur Vergleich möglich
- 3 Authentifizierungsversuche mit Abort

### 3. Dateisystem
- Dateiberechtigungen: 0o600 (nur Besitzer lesen/schreiben)
- Speicherort: Benutzerhome-Verzeichnis
- JSON-Format lesbar aber verschlüsselt

### 4. Eingabevalidierung
- Minimale Passwortlänge: 8 Zeichen
- Leere Eingaben werden abgelehnt
- Passwort-Bestätigung bei Setup

## Performance-Überlegungen

- **PBKDF2-Iterationen:** 480,000 = ~100ms pro Verschlüsselung
- **JSON I/O:** Linear mit Anzahl der Einträge
- **Speichernutzung:** Gering, nur aktive Einträge geladen

## Erweiterungsmöglichkeiten

1. **Datenbank-Backend** - SQLite statt JSON
2. **Clipboard-Integration** - Automatisches Kopieren
3. **Zwei-Faktor-Authentifizierung** - TOTP-Unterstützung
4. **Kategorisierung** - Tags und Kategorien für Services
5. **Export/Import** - Datensicherung in verschiedenen Formaten
6. **Passwort-Änderungstracking** - Historie und Audit-Log
