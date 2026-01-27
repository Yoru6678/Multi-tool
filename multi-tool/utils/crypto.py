"""
Module de cryptographie - Chiffrement et déchiffrement sécurisé
"""

import os
import base64
import hashlib
import secrets
from pathlib import Path
from typing import Optional, Tuple


class CryptoManager:
    """Gestionnaire de cryptographie sécurisé"""
    
    def __init__(self, key: Optional[bytes] = None):
        """
        Initialise le gestionnaire de cryptographie
        
        Args:
            key: Clé de chiffrement (générée automatiquement si non fournie)
        """
        self.key = key or self._generate_key()
    
    @staticmethod
    def _generate_key(length: int = 32) -> bytes:
        """Génère une clé cryptographique sécurisée"""
        return secrets.token_bytes(length)
    
    @staticmethod
    def generate_password(
        length: int = 16,
        include_uppercase: bool = True,
        include_lowercase: bool = True,
        include_digits: bool = True,
        include_special: bool = True
    ) -> str:
        """
        Génère un mot de passe sécurisé
        
        Args:
            length: Longueur du mot de passe
            include_uppercase: Inclure les majuscules
            include_lowercase: Inclure les minuscules
            include_digits: Inclure les chiffres
            include_special: Inclure les caractères spéciaux
            
        Returns:
            Mot de passe généré
        """
        charset = ""
        
        if include_lowercase:
            charset += "abcdefghijklmnopqrstuvwxyz"
        if include_uppercase:
            charset += "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if include_digits:
            charset += "0123456789"
        if include_special:
            charset += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if not charset:
            charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        
        return ''.join(secrets.choice(charset) for _ in range(length))
    
    @staticmethod
    def hash_file(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Calcule le hash d'un fichier
        
        Args:
            file_path: Chemin du fichier
            algorithm: Algorithme de hachage
            
        Returns:
            Hash hexadécimal ou None si erreur
        """
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                return None
            
            hasher = hashlib.new(algorithm)
            
            with open(path, 'rb') as f:
                while chunk := f.read(8192):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def hash_text(text: str, algorithm: str = 'sha256') -> str:
        """
        Calcule le hash d'un texte
        
        Args:
            text: Texte à hacher
            algorithm: Algorithme de hachage
            
        Returns:
            Hash hexadécimal
        """
        hasher = hashlib.new(algorithm)
        hasher.update(text.encode('utf-8'))
        return hasher.hexdigest()
    
    @staticmethod
    def encode_base64(data: str) -> str:
        """Encode une chaîne en Base64"""
        return base64.b64encode(data.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_base64(encoded: str) -> Optional[str]:
        """Décode une chaîne Base64"""
        try:
            return base64.b64decode(encoded.encode('utf-8')).decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def encode_base32(data: str) -> str:
        """Encode une chaîne en Base32"""
        return base64.b32encode(data.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_base32(encoded: str) -> Optional[str]:
        """Décode une chaîne Base32"""
        try:
            return base64.b32decode(encoded.encode('utf-8')).decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def xor_cipher(data: str, key: str) -> str:
        """
        Chiffrement XOR simple (pour démonstration uniquement)
        
        Args:
            data: Données à chiffrer
            key: Clé de chiffrement
            
        Returns:
            Données chiffrées en hexadécimal
        """
        result = []
        for i, char in enumerate(data):
            xored = ord(char) ^ ord(key[i % len(key)])
            result.append(format(xored, '02x'))
        return ''.join(result)
    
    @staticmethod
    def check_password_strength(password: str) -> Tuple[str, int, list]:
        """
        Évalue la force d'un mot de passe
        
        Args:
            password: Mot de passe à évaluer
            
        Returns:
            Tuple (niveau, score, suggestions)
        """
        score = 0
        suggestions = []
        
        if len(password) >= 8:
            score += 1
        else:
            suggestions.append("Utilisez au moins 8 caractères")
        
        if len(password) >= 12:
            score += 1
        
        if len(password) >= 16:
            score += 1
        
        if any(c.islower() for c in password):
            score += 1
        else:
            suggestions.append("Ajoutez des minuscules")
        
        if any(c.isupper() for c in password):
            score += 1
        else:
            suggestions.append("Ajoutez des majuscules")
        
        if any(c.isdigit() for c in password):
            score += 1
        else:
            suggestions.append("Ajoutez des chiffres")
        
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if any(c in special_chars for c in password):
            score += 1
        else:
            suggestions.append("Ajoutez des caractères spéciaux")
        
        if len(set(password)) / len(password) > 0.7:
            score += 1
        else:
            suggestions.append("Évitez les caractères répétitifs")
        
        if score <= 3:
            level = "Faible"
        elif score <= 5:
            level = "Moyen"
        elif score <= 7:
            level = "Fort"
        else:
            level = "Très fort"
        
        return level, score, suggestions
