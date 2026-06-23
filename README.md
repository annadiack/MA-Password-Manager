# MA-Password-Manager

Ein sicherer Python-basierter Passwortmanager mit Konsolenschnittstelle für die Mastarbeit.

## Features

✅ **Passwörter speichern** - Sichere Speicherung mit AES-256 Verschlüsselung  
✅ **Passwörter abrufen** - Schneller Zugriff auf gespeicherte Credentials  
✅ **Passwörter generieren** - Starke, zufällige Passwörter  
✅ **Benutzerfreundliche CLI** - Intuitive Konsolenbedienung  
✅ **Vollständig dokumentiert** - Code-Dokumentation und Benutzerhandbuch  

## Installation

### Voraussetzungen
- Python 3.8 oder höher
- pip (Python Package Manager)

### Setup

1. Repository klonen:
```bash
git clone https://github.com/annadiack/MA-Password-Manager.git
cd MA-Password-Manager
```

2. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## Benutzung

Starten Sie den Passwortmanager:
```bash
python main.py
```

### Verfügbare Befehle

- **1. Passwort speichern** - Neuen Eintrag hinzufügen
- **2. Passwort abrufen** - Gespeicherte Passwörter anzeigen
- **3. Passwort generieren** - Neue sichere Passwörter erstellen
- **4. Alle Einträge anzeigen** - Liste aller Services
- **5. Eintrag löschen** - Service entfernen
- **6. Passwortmanager beenden** - Programm beenden

## Projektstruktur

```
MA-Password-Manager/
├── main.py                 # Haupteinstiegspunkt
├── requirements.txt        # Python-Abhängigkeiten
├── README.md              # Dieses Dokument
├── docs/                  # Dokumentation
│   ├── ARCHITECTURE.md    # Technische Architektur
│   ├── API.md            # API-Dokumentation
│   └── USER_GUIDE.md     # Benutzerhandbuch
└── password_manager/      # Hauptpaket
    ├── __init__.py
    ├── manager.py         # Hauptlogik des Managers
    ├── crypto.py          # Verschlüsselungsfunktionen
    ├── generator.py       # Passwortgenerator
    ├── storage.py         # Datenspeicherung
    └── ui.py              # Benutzeroberfläche
```

## Sicherheitshinweise

⚠️ **Wichtig**: 
- Dieses Tool verschlüsselt Passwörter mit AES-256
- Der Master-Key wird lokal in einer verschlüsselten Datei gespeichert
- Nutzen Sie starke Master-Passwörter
- Sichern Sie regelmäßig Ihre Daten

## Lizenz

Masterarbeitsprojekt - 2026

## Dokumentation

- [Technische Architektur](docs/ARCHITECTURE.md)
- [API-Dokumentation](docs/API.md)
- [Benutzerhandbuch](docs/USER_GUIDE.md)
