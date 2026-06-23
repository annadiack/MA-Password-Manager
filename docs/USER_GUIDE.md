# Benutzerhandbuch

## Inhaltsverzeichnis

1. [Installation](#installation)
2. [Erste Schritte](#erste-schritte)
3. [Hauptfunktionen](#hauptfunktionen)
4. [Häufig gestellte Fragen](#häufig-gestellte-fragen)
5. [Sicherheitstipps](#sicherheitstipps)

---

## Installation

### Systemvoraussetzungen

- **Python 3.8+** (überprüfen mit `python --version`)
- **pip** (normalerweise mit Python installiert)
- **Speicherplatz:** ~10 MB für Installation

### Schritt-für-Schritt Installation

#### 1. Repository klonen

```bash
git clone https://github.com/annadiack/MA-Password-Manager.git
cd MA-Password-Manager
```

#### 2. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

Dies installiert:
- **cryptography** - Kryptographische Funktionen
- **colorama** - Farbige Konsolenausgabe
- **pydantic** - Datenvalidierung

#### 3. Programm starten

```bash
python main.py
```

---

## Erste Schritte

### Master-Passwort einrichten

Bei der ersten Ausführung werden Sie aufgefordert, ein Master-Passwort zu erstellen:

```
============================================================
     Erste Einrichtung des Passwortmanagers
============================================================

Master-Passwort eingeben: ••••••••••••
Master-Passwort bestätigen: ••••••••••••

✓ Master-Passwort erfolgreich gespeichert!
```

**Wichtige Punkte:**
- ✅ Wählen Sie ein **starkes Passwort** (mindestens 12 Zeichen)
- ✅ Kombinieren Sie **Groß-, Kleinbuchstaben, Zahlen und Sonderzeichen**
- ✅ **Merken Sie sich das Passwort** - es kann nicht zurückgesetzt werden
- ❌ Nutzen Sie **keine einfachen Passwörter** wie "password123"

### Authentifizierung

Bei jeder nachfolgenden Ausführung geben Sie Ihr Master-Passwort ein:

```
============================================================
        Authentifizierung erforderlich
============================================================

Master-Passwort eingeben: ••••••••••••
✓ Authentifizierung erfolgreich!
```

Sie haben **3 Versuche**, bevor das Programm beendet wird.

---

## Hauptfunktionen

### 1. Passwort speichern

```
Hauptmenü:
  1. Passwort speichern

Wähle eine Option: 1

--- Passwort speichern ---
Service-Name (z.B. Gmail, GitHub): Gmail
Benutzername/E-Mail: user@gmail.com
Passwort: MySecurePassword123
Notizen (optional): Persönliches Konto

✓ Passwort für 'Gmail' erfolgreich gespeichert
```

**Was wird gespeichert?**
- Service-Name
- Benutzername/E-Mail
- Passwort (verschlüsselt mit AES-256)
- Notizen (optional)
- Zeitstempel (erstellt/geändert)

**Tipps:**
- Service-Namen eindeutig halten (z.B. "Gmail-Work", "Gmail-Private")
- Notizen für mehrere Konten nutzen (z.B. "2. Faktor aktiviert")
- Bestehende Einträge werden überschrieben wenn gleicher Name

---

### 2. Passwort abrufen

```
Hauptmenü:
  2. Passwort abrufen

Wähle eine Option: 2

--- Passwort abrufen ---
Service-Name eingeben: Gmail

Passwortinformationen:
  Service:    Gmail
  Benutzer:   user@gmail.com
  Passwort:   MySecurePassword123
  Notizen:    Persönliches Konto
  Erstellt:   2026-06-23T15:30:00
  Geändert:   2026-06-23T15:30:00
```

**Funktionsweise:**
1. Service-Name eingeben
2. Passwort wird entschlüsselt und angezeigt
3. Vollständige Informationen werden angezeigt

**Hinweise:**
- Service-Namen sind **case-insensitive** ("Gmail", "gmail", "GMAIL" funktionieren alle)
- Passwort wird **im Klartext** angezeigt
- Keine Limitierung wie oft Sie abrufen können

---

### 3. Passwort generieren

```
Hauptmenü:
  3. Passwort generieren

Wähle eine Option: 3

--- Passwort generieren ---
Benutzerdefinierte Länge? (Standard=16, oder Zahl eingeben): 20

Generiertes Passwort:
  k7@mP#xL$qR9vN2wE5tY
  Länge: 20
  Stärke: Sehr stark

In Eintrag speichern? (j/n): j
```

**Generator-Optionen:**
- **Standardlänge:** 16 Zeichen
- **Mindestlänge:** 8 Zeichen
- **Zeichensätze:** Großbuchstaben, Kleinbuchstaben, Zahlen, Sonderzeichen

**Passwort-Stärkebewertung:**
- 🔴 **Sehr schwach:** 0-1 Punkte
- 🟠 **Schwach:** 2 Punkte
- 🟡 **Mittel:** 3-4 Punkte
- 🟢 **Stark:** 5-6 Punkte
- 💚 **Sehr stark:** 7-8 Punkte

**Empfehlungen:**
- Nutzen Sie mindestens **16 Zeichen**
- Ziel: **"Sehr stark"** Bewertung
- Optional: Direkt in Passwort-Manager speichern

---

### 4. Alle Einträge anzeigen

```
Hauptmenü:
  4. Alle Einträge anzeigen

Wähle eine Option: 4

--- Alle Einträge ---
  1. Gmail
  2. GitHub
  3. AWS-Console
  4. Jira
```

**Funktionsweise:**
- Listet alle gespeicherten Services auf
- Nur Service-Namen sichtbar (keine Passwörter)
- Verwendet Sie zum Überblick über gespeicherte Konten

---

### 5. Eintrag löschen

```
Hauptmenü:
  5. Eintrag löschen

Wähle eine Option: 5

--- Eintrag löschen ---
Service-Name eingeben: Gmail
Eintrag 'Gmail' wirklich löschen? (j/n): j

✓ Eintrag 'Gmail' gelöscht
```

**Wichtige Hinweise:**
- ⚠️ **Löschen ist permanent** - kann nicht rückgängig gemacht werden
- Bestätigung erforderlich vor Löschung
- Service-Namen sind case-insensitive

---

### 6. Programm beenden

```
Hauptmenü:
  6. Passwortmanager beenden

Wähle eine Option: 6

Auf Wiedersehen!
```

Sicher beendet das Programm.

---

## Häufig gestellte Fragen

### F: Was passiert wenn ich mein Master-Passwort vergesse?
**A:** Das Master-Passwort kann **nicht zurückgesetzt werden**. Die Passwörter sind dann nicht mehr abrufbar. Bewahren Sie das Master-Passwort an sicherer Stelle auf.

### F: Wo werden meine Passwörter gespeichert?
**A:** 
Linux/macOS:
```
~/.password_manager/passwords.json
```

Windows:
```
C:\Users\<YourUsername>\.password_manager\passwords.json
```

Die Passwörter sind **verschlüsselt**.

### F: Kann ich meine Passwörter exportieren?
**A:** Aktuell nicht über die UI. Sie können die Datei direkt in `~/.password_manager/passwords.json` bearbeiten (Passwörter sind Base64-kodiert, aber verschlüsselt).

### F: Ist das sicher genug?
**A:** Ja, der Manager nutzt:
- AES-256-GCM Verschlüsselung (Military-grade)
- PBKDF2 mit 480,000 Iterationen
- Dateiberechtigungen 0o600 (nur Besitzer)

Zusätzlich empfehlen wir:
- Starkes Master-Passwort
- Regelmäßige Backups
- Sicherer Computer

### F: Kann ich den Manager auf mehreren Computern nutzen?
**A:** Aktuell wird jeder Computer getrennt verwaltet. Sie können die `passwords.json` Datei manuell synchronisieren.

### F: Wie viele Passwörter kann ich speichern?
**A:** Theoretisch unbegrenzt, praktisch limitiert durch Speicherplatz. Die JSON-Datei bleibt klein (1 Eintrag ≈ 500 Bytes).

---

## Sicherheitstipps

### 1. Master-Passwort
✅ **DO:**
- Verwenden Sie **mindestens 12 Zeichen**
- Kombinieren Sie **Groß-, Kleinbuchstaben, Zahlen, Sonderzeichen**
- Nutzen Sie **unikale** Passwörter
- Speichern Sie es **sicher** (z.B. Passwort-Manager, Papier)

❌ **DON'T:**
- Keine **einfachen Wörter** (password, qwerty, 123456)
- Keine **persönlichen Daten** (Namen, Geburtsdaten)
- Nicht **weitergeben** oder **aufschreiben**
- Nicht in **Browser speichern**

### 2. Passwortmanager Sicherheit
✅ **DO:**
- Führen Sie regelmäßig **Backups** durch
- Nutzen Sie den Manager auf **sicheren Computern**
- Sperren Sie Ihren Computer wenn **nicht in Benutzung**
- Verwenden Sie **Firewall** und **Antivirus**

❌ **DON'T:**
- Laden Sie nicht vom **unsicheren Quellen** herunter
- Teilen Sie Ihr Master-Passwort **nicht**
- Speichern Sie Passwörter **nicht in Klartext**
- Nutzen Sie nicht auf **öffentlichen Computern**

### 3. Passwortmanagement
✅ **DO:**
- Generieren Sie **starke Passwörter** (16+ Zeichen)
- Nutzen Sie **unique Passwörter** pro Service
- Aktualisieren Sie Passwörter **regelmäßig**
- Speichern Sie **sensible Notizen**

❌ **DON'T:**
- Wiederverwenden Sie Passwörter nicht
- Speichern Sie "Test-Passwörter"
- Nutzen Sie zu kurze Passwörter
- Vergessen Sie Updates

### 4. Datenschutz
✅ **DO:**
- Nutzen Sie diesen Manager **nur privat**
- Beachten Sie **lokale Datenschutzgesetze**
- Löschen Sie Passwörter wenn **nicht mehr nötig**
- Sichern Sie Ihr Backup **verschlüsselt**

---

## Support

Bei Fragen oder Problemen:
1. Überprüfen Sie die [Technische Architektur](ARCHITECTURE.md)
2. Konsultieren Sie die [API-Dokumentation](API.md)
3. Erstellen Sie ein [GitHub Issue](https://github.com/annadiack/MA-Password-Manager/issues)

---

**Viel Erfolg mit dem Password Manager!** 🔐
