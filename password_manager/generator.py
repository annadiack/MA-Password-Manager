"""
Passwortgenerator-Modul.

Dieses Modul bietet Funktionen zur Generierung von starken,
zufälligen Passwörtern mit konfigurierbaren Anforderungen.
"""

import random
import string


class PasswordGenerator:
    """Generiert sichere, zufällige Passwörter."""
    
    # Zeichensätze
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    @staticmethod
    def generate(
        length: int = 16,
        use_lowercase: bool = True,
        use_uppercase: bool = True,
        use_digits: bool = True,
        use_special: bool = True
    ) -> str:
        """
        Generiert ein sicheres Passwort mit den angegebenen Anforderungen.
        
        Args:
            length: Passwortlänge (mindestens 8)
            use_lowercase: Kleinbuchstaben einbeziehen
            use_uppercase: Großbuchstaben einbeziehen
            use_digits: Zahlen einbeziehen
            use_special: Sonderzeichen einbeziehen
            
        Returns:
            Generiertes Passwort
            
        Raises:
            ValueError: Wenn Länge < 8 oder keine Zeichensätze gewählt
        """
        if length < 8:
            raise ValueError("Passwortlänge muss mindestens 8 Zeichen sein")
        
        # Verfügbare Zeichen zusammenstellen
        available_chars = ""
        if use_lowercase:
            available_chars += PasswordGenerator.LOWERCASE
        if use_uppercase:
            available_chars += PasswordGenerator.UPPERCASE
        if use_digits:
            available_chars += PasswordGenerator.DIGITS
        if use_special:
            available_chars += PasswordGenerator.SPECIAL
        
        if not available_chars:
            raise ValueError("Mindestens ein Zeichensatz muss gewählt sein")
        
        # Passwort generieren
        password = "".join(
            random.choice(available_chars) for _ in range(length)
        )
        
        return password
    
    @staticmethod
    def generate_strong(length: int = 16) -> str:
        """
        Generiert ein starkes Passwort mit allen Zeichensatztypen.
        
        Args:
            length: Passwortlänge
            
        Returns:
            Starkes Passwort
        """
        return PasswordGenerator.generate(
            length=length,
            use_lowercase=True,
            use_uppercase=True,
            use_digits=True,
            use_special=True
        )
    
    @staticmethod
    def validate_strength(password: str) -> dict:
        """
        Bewertet die Stärke eines Passworts.
        
        Args:
            password: Zu bewertendes Passwort
            
        Returns:
            Dict mit Bewertung und Feedback
        """
        score = 0
        feedback = []
        
        # Längenbewertung
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if len(password) >= 16:
            score += 1
        else:
            feedback.append("Länge sollte mindestens 16 Zeichen sein")
        
        # Zeichensätze prüfen
        has_lower = any(c in PasswordGenerator.LOWERCASE for c in password)
        has_upper = any(c in PasswordGenerator.UPPERCASE for c in password)
        has_digit = any(c in PasswordGenerator.DIGITS for c in password)
        has_special = any(c in PasswordGenerator.SPECIAL for c in password)
        
        if has_lower:
            score += 1
        else:
            feedback.append("Kleinbuchstaben hinzufügen")
        
        if has_upper:
            score += 1
        else:
            feedback.append("Großbuchstaben hinzufügen")
        
        if has_digit:
            score += 1
        else:
            feedback.append("Zahlen hinzufügen")
        
        if has_special:
            score += 1
        else:
            feedback.append("Sonderzeichen hinzufügen")
        
        # Bewertung als String
        strength_map = {
            0: "Sehr schwach",
            1: "Schwach",
            2: "Schwach",
            3: "Mittel",
            4: "Mittel",
            5: "Stark",
            6: "Stark",
            7: "Sehr stark",
            8: "Sehr stark"
        }
        
        return {
            "score": score,
            "strength": strength_map.get(score, "Unbekannt"),
            "feedback": feedback
        }
