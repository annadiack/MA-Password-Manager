"""
Benutzeroberfläche des Passwortmanagers.

Dieses Modul bietet die interaktive Konsolenschnittstelle für den Passwortmanager.
"""

from colorama import Fore, Back, Style, init
from .manager import PasswordManager
from .generator import PasswordGenerator

# Colorama initialisieren
init(autoreset=True)


class PasswordManagerUI:
    """Benutzeroberfläche des Passwortmanagers."""
    
    def __init__(self):
        """Initialisiert die Benutzeroberfläche."""
        self.manager = None
        self.running = True
    
    def print_header(self, text: str) -> None:
        """Gibt einen formatierten Header aus."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{text.center(60)}")
        print(f"{'='*60}{Style.RESET_ALL}\n")
    
    def print_success(self, text: str) -> None:
        """Gibt eine Erfolgsmeldung aus."""
        print(f"{Fore.GREEN}✓ {text}{Style.RESET_ALL}")
    
    def print_error(self, text: str) -> None:
        """Gibt eine Fehlermeldung aus."""
        print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")
    
    def print_info(self, text: str) -> None:
        """Gibt eine Informationsmeldung aus."""
        print(f"{Fore.YELLOW}ℹ {text}{Style.RESET_ALL}")
    
    def setup_master_password(self) -> None:
        """Dialog zur Einrichtung des Master-Passworts."""
        self.print_header("Erste Einrichtung des Passwortmanagers")
        
        print("Ein Master-Passwort ist erforderlich, um Ihre Passwörter zu schützen.")
        print("Bitte wählen Sie ein starkes Passwort (mindestens 12 Zeichen).\n")
        
        while True:
            password = input(f"{Fore.CYAN}Master-Passwort eingeben: {Style.RESET_ALL}")
            
            if len(password) < 8:
                self.print_error("Passwort muss mindestens 8 Zeichen lang sein")
                continue
            
            # Passwort-Stärke prüfen
            strength = PasswordGenerator.validate_strength(password)
            print(f"Passwort-Stärke: {Fore.MAGENTA}{strength['strength']}{Style.RESET_ALL}")
            
            if strength['feedback']:
                for feedback in strength['feedback']:
                    print(f"  → {feedback}")
            
            confirm = input(f"\n{Fore.CYAN}Passwort bestätigen: {Style.RESET_ALL}")
            
            if password == confirm:
                PasswordManager.setup_master_password(password)
                self.manager = PasswordManager(password)
                self.print_success("Master-Passwort erfolgreich gespeichert!")
                break
            else:
                self.print_error("Passwörter stimmen nicht überein")
    
    def authenticate(self) -> None:
        """Dialog zur Authentifizierung mit dem Master-Passwort."""
        self.print_header("Authentifizierung erforderlich")
        
        attempts = 3
        while attempts > 0:
            password = input(f"{Fore.CYAN}Master-Passwort eingeben: {Style.RESET_ALL}")
            
            if PasswordManager.verify_master_password(password):
                self.manager = PasswordManager(password)
                self.print_success("Authentifizierung erfolgreich!")
                break
            else:
                attempts -= 1
                if attempts > 0:
                    self.print_error(f"Falsches Passwort. {attempts} Versuche verbleibend")
                else:
                    self.print_error("Zu viele fehlgeschlagene Versuche. Programmbeendung.")
                    self.running = False
    
    def display_menu(self) -> None:
        """Zeigt das Hauptmenü an."""
        print(f"\n{Fore.CYAN}Hauptmenü:{Style.RESET_ALL}")
        print("  1. Passwort speichern")
        print("  2. Passwort abrufen")
        print("  3. Passwort generieren")
        print("  4. Alle Einträge anzeigen")
        print("  5. Eintrag löschen")
        print("  6. Passwortmanager beenden")
        print()
    
    def save_password_dialog(self) -> None:
        """Dialog zum Speichern eines neuen Passworts."""
        print(f"\n{Fore.CYAN}--- Passwort speichern ---{Style.RESET_ALL}")
        
        service = input("Service-Name (z.B. Gmail, GitHub): ").strip()
        if not service:
            self.print_error("Service-Name darf nicht leer sein")
            return
        
        username = input("Benutzername/E-Mail: ").strip()
        if not username:
            self.print_error("Benutzername darf nicht leer sein")
            return
        
        password = input("Passwort: ").strip()
        if not password:
            self.print_error("Passwort darf nicht leer sein")
            return
        
        notes = input("Notizen (optional): ").strip()
        
        try:
            self.manager.save_password(service, username, password, notes)
            self.print_success(f"Passwort für '{service}' erfolgreich gespeichert")
        except Exception as e:
            self.print_error(f"Fehler beim Speichern: {str(e)}")
    
    def get_password_dialog(self) -> None:
        """Dialog zum Abrufen eines Passworts."""
        print(f"\n{Fore.CYAN}--- Passwort abrufen ---{Style.RESET_ALL}")
        
        services = self.manager.list_all_services()
        if not services:
            self.print_info("Keine Einträge vorhanden")
            return
        
        service = input("Service-Name eingeben: ").strip()
        
        result = self.manager.get_password(service)
        if result:
            print(f"\n{Fore.CYAN}Passwortinformationen:{Style.RESET_ALL}")
            print(f"  Service:    {result['service']}")
            print(f"  Benutzer:   {result['username']}")
            print(f"  Passwort:   {Fore.MAGENTA}{result['password']}{Style.RESET_ALL}")
            if result['notes']:
                print(f"  Notizen:    {result['notes']}")
            print(f"  Erstellt:   {result['created_at']}")
            print(f"  Geändert:   {result['updated_at']}")
        else:
            self.print_error(f"Service '{service}' nicht gefunden")
    
    def generate_password_dialog(self) -> None:
        """Dialog zum Generieren eines neuen Passworts."""
        print(f"\n{Fore.CYAN}--- Passwort generieren ---{Style.RESET_ALL}")
        
        print("Standardeinstellungen: 16 Zeichen mit allen Zeichensätzen")
        custom = input("Benutzerdefinierte Länge? (Standard=16, oder Zahl eingeben): ").strip()
        
        try:
            length = int(custom) if custom else 16
            if length < 8:
                self.print_error("Länge muss mindestens 8 sein")
                return
        except ValueError:
            length = 16
        
        password = self.manager.generate_password(length=length)
        strength = PasswordGenerator.validate_strength(password)
        
        print(f"\n{Fore.CYAN}Generiertes Passwort:{Style.RESET_ALL}")
        print(f"  {Fore.MAGENTA}{password}{Style.RESET_ALL}")
        print(f"  Länge: {length}")
        print(f"  Stärke: {strength['strength']}")
        
        save = input("\nIn Eintrag speichern? (j/n): ").strip().lower()
        if save == 'j':
            self.save_password_dialog()
    
    def list_entries_dialog(self) -> None:
        """Zeigt alle Einträge an."""
        print(f"\n{Fore.CYAN}--- Alle Einträge ---{Style.RESET_ALL}")
        
        services = self.manager.list_all_services()
        if not services:
            self.print_info("Keine Einträge vorhanden")
            return
        
        for i, service in enumerate(services, 1):
            print(f"  {i}. {service}")
    
    def delete_entry_dialog(self) -> None:
        """Dialog zum Löschen eines Eintrags."""
        print(f"\n{Fore.CYAN}--- Eintrag löschen ---{Style.RESET_ALL}")
        
        services = self.manager.list_all_services()
        if not services:
            self.print_info("Keine Einträge vorhanden")
            return
        
        service = input("Service-Name eingeben: ").strip()
        
        confirm = input(f"Eintrag '{service}' wirklich löschen? (j/n): ").strip().lower()
        if confirm == 'j':
            if self.manager.delete_password(service):
                self.print_success(f"Eintrag '{service}' gelöscht")
            else:
                self.print_error(f"Service '{service}' nicht gefunden")
    
    def run(self) -> None:
        """Hauptprogrammschleife."""
        self.print_header("Passwortmanager")
        
        # Authentifizierung
        if PasswordManager.is_first_launch():
            self.setup_master_password()
        else:
            self.authenticate()
        
        if not self.running:
            return
        
        # Hauptschleife
        while self.running:
            self.display_menu()
            choice = input(f"{Fore.CYAN}Wähle eine Option (1-6): {Style.RESET_ALL}").strip()
            
            if choice == '1':
                self.save_password_dialog()
            elif choice == '2':
                self.get_password_dialog()
            elif choice == '3':
                self.generate_password_dialog()
            elif choice == '4':
                self.list_entries_dialog()
            elif choice == '5':
                self.delete_entry_dialog()
            elif choice == '6':
                print(f"\n{Fore.CYAN}Auf Wiedersehen!{Style.RESET_ALL}\n")
                self.running = False
            else:
                self.print_error("Ungültige Auswahl. Bitte wähle 1-6")


def main() -> None:
    """Einstiegspunkt der Anwendung."""
    try:
        ui = PasswordManagerUI()
        ui.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programm unterbrochen.{Style.RESET_ALL}\n")
    except Exception as e:
        print(f"\n{Fore.RED}Kritischer Fehler: {str(e)}{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
