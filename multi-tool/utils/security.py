"""
Module de sécurité - Fonctions de protection et validation
"""

import re
import html
import secrets
import hashlib
from pathlib import Path
from typing import Optional, Union
from urllib.parse import urlparse


class SecurityUtils:
    """Classe utilitaire pour les fonctions de sécurité"""
    
    DANGEROUS_CHARS = ['..', '~', '$', '`', '|', ';', '&', '>', '<', '\\x00']
    ALLOWED_SCHEMES = ['http', 'https']
    
    @staticmethod
    def sanitize_input(user_input: str, max_length: int = 1000) -> str:
        """
        Nettoie une entrée utilisateur contre les injections
        
        Args:
            user_input: Chaîne à nettoyer
            max_length: Longueur maximale autorisée
            
        Returns:
            Chaîne nettoyée et sécurisée
        """
        if not isinstance(user_input, str):
            return ""
        
        cleaned = user_input.strip()[:max_length]
        cleaned = html.escape(cleaned)
        
        for char in SecurityUtils.DANGEROUS_CHARS:
            cleaned = cleaned.replace(char, '')
        
        return cleaned
    
    @staticmethod
    def sanitize_path(file_path: str) -> Optional[Path]:
        """
        Valide et nettoie un chemin de fichier contre les path traversal
        
        Args:
            file_path: Chemin à valider
            
        Returns:
            Path sécurisé ou None si invalide
        """
        if not file_path:
            return None
            
        try:
            path = Path(file_path).resolve()
            
            if '..' in str(path) or str(path).startswith('/etc'):
                return None
                
            return path
        except Exception:
            return None
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """
        Valide qu'une URL est sécurisée
        
        Args:
            url: URL à valider
            
        Returns:
            True si l'URL est valide et sécurisée
        """
        try:
            parsed = urlparse(url)
            return (
                parsed.scheme in SecurityUtils.ALLOWED_SCHEMES and
                bool(parsed.netloc) and
                '..' not in url
            )
        except Exception:
            return False
    
    @staticmethod
    def validate_ip(ip: str) -> bool:
        """
        Valide une adresse IP (IPv4 ou IPv6)
        
        Args:
            ip: Adresse IP à valider
            
        Returns:
            True si l'IP est valide
        """
        ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
        ipv6_pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
        
        if re.match(ipv4_pattern, ip):
            octets = ip.split('.')
            return all(0 <= int(octet) <= 255 for octet in octets)
        
        return bool(re.match(ipv6_pattern, ip))
    
    @staticmethod
    def validate_domain(domain: str) -> bool:
        """
        Valide un nom de domaine
        
        Args:
            domain: Domaine à valider
            
        Returns:
            True si le domaine est valide
        """
        pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
        return bool(re.match(pattern, domain))
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Valide une adresse email
        
        Args:
            email: Email à valider
            
        Returns:
            True si l'email est valide
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    @staticmethod
    def generate_secure_token(length: int = 32) -> str:
        """
        Génère un token sécurisé
        
        Args:
            length: Longueur du token en bytes
            
        Returns:
            Token hexadécimal sécurisé
        """
        return secrets.token_hex(length)
    
    @staticmethod
    def hash_data(data: str, algorithm: str = 'sha256') -> str:
        """
        Hache des données de manière sécurisée
        
        Args:
            data: Données à hacher
            algorithm: Algorithme de hachage
            
        Returns:
            Hash hexadécimal
        """
        hasher = hashlib.new(algorithm)
        hasher.update(data.encode('utf-8'))
        return hasher.hexdigest()
    
    @staticmethod
    def is_safe_command(command: str) -> bool:
        """
        Vérifie si une commande est sûre à exécuter
        
        Args:
            command: Commande à vérifier
            
        Returns:
            True si la commande est considérée sûre
        """
        dangerous_patterns = [
            'rm -rf', 'del /f', 'format', 'mkfs',
            'dd if=', ':(){:|:&};:', 'chmod 777',
            'wget', 'curl -o', 'eval', 'exec'
        ]
        
        command_lower = command.lower()
        return not any(pattern in command_lower for pattern in dangerous_patterns)
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Nettoie un nom de fichier
        
        Args:
            filename: Nom de fichier à nettoyer
            
        Returns:
            Nom de fichier sécurisé
        """
        invalid_chars = '<>:"/\\|?*\x00'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        filename = filename.strip('. ')
        
        return filename[:255] if filename else 'unnamed_file'
