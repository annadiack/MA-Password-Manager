# API-Dokumentation

## PasswordManager

Hauptklasse für Passwortmanagement-Operationen.

### Konstruktor

```python
PasswordManager(master_password: str)
```

**Parameter:**
- `master_password` (str): Das Master-Passwort zur Verschlüsselung

**Beispiel:**
```python
from password_manager import PasswordManager

manager = PasswordManager("my_secure_password")
```

---

### save_password()

```python
def save_password(service: str, username: str, password: str, notes: str = "") -> None
```

Speichert ein neues Passwort oder aktualisiert ein bestehendes.

**Parameter:**
- `service` (str): Name des Services (z.B. "Gmail", "GitHub")
- `username` (str): Benutzername oder E-Mail-Adresse
- `password` (str): Das zu speichernde Passwort
- `notes` (str, optional): Zusätzliche Notizen (Standard: "")

**Exceptions:**
- `ValueError`: Wenn Eingaben leer sind

**Beispiel:**
```python
manager.save_password(
    service="Gmail",
    username="user@gmail.com",
    password="MySecurePassword123",
    notes="Persönliches Konto"
)
```

---

### get_password()

```python
def get_password(service: str) -> Optional[dict]
```

Ruft ein gespeichertes Passwort ab und entschlüsselt es.

**Parameter:**
- `service` (str): Name des Services

**Returns:**
- dict mit Schlüsseln: `service`, `username`, `password`, `notes`, `created_at`, `updated_at`
- None: Falls Service nicht gefunden

**Beispiel:**
```python
result = manager.get_password("Gmail")

if result:
    print(f"Username: {result['username']}")
    print(f"Password: {result['password']}")
else:
    print("Service nicht gefunden")
```

---

### delete_password()

```python
def delete_password(service: str) -> bool
```

Löscht einen Passwort-Eintrag.

**Parameter:**
- `service` (str): Name des Services

**Returns:**
- bool: True wenn gelöscht, False wenn nicht gefunden

**Beispiel:**
```python
if manager.delete_password("Gmail"):
    print("Passwort gelöscht")
else:
    print("Service nicht gefunden")
```

---

### list_all_services()

```python
def list_all_services() -> list
```

Listet alle gespeicherten Service-Namen auf.

**Returns:**
- list: Liste von Service-Namen

**Beispiel:**
```python
services = manager.list_all_services()
for service in services:
    print(f"- {service}")
```

---

### generate_password()

```python
def generate_password(
    length: int = 16,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str
```

Generiert ein neues starkes Passwort.

**Parameter:**
- `length` (int): Passwortlänge (Minimum: 8)
- `use_lowercase` (bool): Kleinbuchstaben einbeziehen
- `use_uppercase` (bool): Großbuchstaben einbeziehen
- `use_digits` (bool): Zahlen einbeziehen
- `use_special` (bool): Sonderzeichen einbeziehen

**Returns:**
- str: Generiertes Passwort

**Exceptions:**
- `ValueError`: Wenn Länge < 8 oder keine Zeichensätze gewählt

**Beispiele:**
```python
# Standard: 16 Zeichen, alle Zeichensätze
password = manager.generate_password()

# Custom: 20 Zeichen ohne Sonderzeichen
password = manager.generate_password(length=20, use_special=False)

# Nur alphanumerisch
password = manager.generate_password(use_special=False)
```

---

## CryptoManager

Statische Klasse für kryptographische Operationen.

### encrypt()

```python
@staticmethod
def encrypt(plaintext: str, password: str) -> str
```

Verschlüsselt einen Text mit AES-256-GCM.

**Parameter:**
- `plaintext` (str): Zu verschlüsselnder Text
- `password` (str): Master-Passwort für Key-Derivation

**Returns:**
- str: Base64-kodierter verschlüsselter Text

**Beispiel:**
```python
from password_manager.crypto import CryptoManager

encrypted = CryptoManager.encrypt("MyPassword", "master_password")
print(encrypted)  # Base64-String
```

---

### decrypt()

```python
@staticmethod
def decrypt(ciphertext_b64: str, password: str) -> str
```

Entschlüsselt einen AES-256-GCM verschlüsselten Text.

**Parameter:**
- `ciphertext_b64` (str): Base64-kodierter verschlüsselter Text
- `password` (str): Master-Passwort zur Key-Derivation

**Returns:**
- str: Entschlüsselter Plaintext

**Exceptions:**
- `ValueError`: Bei Entschlüsselungsfehlern

**Beispiel:**
```python
try:
    decrypted = CryptoManager.decrypt(encrypted, "master_password")
    print(decrypted)  # "MyPassword"
except ValueError as e:
    print(f"Entschlüsselung fehlgeschlagen: {e}")
```

---

### derive_key()

```python
@staticmethod
def derive_key(password: str, salt: bytes = None) -> tuple[bytes, bytes]
```

Leitet einen kryptographischen Schlüssel vom Master-Passwort ab.

**Parameter:**
- `password` (str): Das Master-Passwort
- `salt` (bytes, optional): Salt (wird generiert wenn nicht vorhanden)

**Returns:**
- tuple: (schlüssel: bytes, salt: bytes)

**Beispiel:**
```python
key, salt = CryptoManager.derive_key("master_password")
print(f"Schlüssellänge: {len(key)} bytes")
```

---

## PasswordGenerator

Statische Klasse für Passwortgenerierung und -validierung.

### generate()

```python
@staticmethod
def generate(
    length: int = 16,
    use_lowercase: bool = True,
    use_uppercase: bool = True,
    use_digits: bool = True,
    use_special: bool = True
) -> str
```

Generiert ein Passwort mit konfigurierbaren Anforderungen.

**Parameter:** (siehe oben)

**Returns:**
- str: Generiertes Passwort

---

### generate_strong()

```python
@staticmethod
def generate_strong(length: int = 16) -> str
```

Generiert ein starkes Passwort mit allen Zeichensatztypen.

**Parameter:**
- `length` (int): Passwortlänge

**Returns:**
- str: Starkes Passwort

**Beispiel:**
```python
from password_manager.generator import PasswordGenerator

password = PasswordGenerator.generate_strong(20)
```

---

### validate_strength()

```python
@staticmethod
def validate_strength(password: str) -> dict
```

Bewertet die Stärke eines Passworts.

**Parameter:**
- `password` (str): Zu bewertendes Passwort

**Returns:**
- dict mit Schlüsseln:
  - `score` (int): Bewertungspunkte 0-8
  - `strength` (str): "Sehr schwach" bis "Sehr stark"
  - `feedback` (list): Verbesserungsvorschläge

**Beispiel:**
```python
result = PasswordGenerator.validate_strength("Test123")
print(result['strength'])  # "Mittel"
for feedback in result['feedback']:
    print(f"  → {feedback}")
```

---

## StorageManager

Klasse für Dateiverwaltung und Persistierung.

### load_entries()

```python
def load_entries() -> List[PasswordEntry]
```

Lädt alle Passworteinträge aus der Speicherdatei.

**Returns:**
- List[PasswordEntry]: Liste aller Einträge

---

### save_entries()

```python
def save_entries(entries: List[PasswordEntry]) -> None
```

Speichert Einträge in die Datei.

**Parameter:**
- `entries` (List[PasswordEntry]): Zu speichernde Einträge

---

### add_entry()

```python
def add_entry(entry: PasswordEntry) -> None
```

Fügt einen neuen Eintrag hinzu oder aktualisiert einen existierenden.

**Parameter:**
- `entry` (PasswordEntry): Zu speichernder Eintrag

---

### get_entry()

```python
def get_entry(service: str) -> Optional[PasswordEntry]
```

Ruft einen Eintrag für einen bestimmten Service ab.

**Returns:**
- PasswordEntry oder None

---

### delete_entry()

```python
def delete_entry(service: str) -> bool
```

Löscht einen Eintrag.

**Returns:**
- bool: True wenn gelöscht, False wenn nicht gefunden

---

### list_services()

```python
def list_services() -> List[str]
```

Listet alle Service-Namen auf.

**Returns:**
- List[str]: Liste der Service-Namen
