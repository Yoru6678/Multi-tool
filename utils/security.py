#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de sécurité - Gestion de la validation des entrées et du chiffrement
Compatible Windows 10/11
"""

import re
import os
import hashlib
import secrets
import string
from pathlib import Path
from typing import Optional, Union
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import logging

# Compatibility wrapper for PBKDF2
PBKDF2 = PBKDF2HMAC

logger = logging.getLogger(__name__)


class SecurityManager:
    """Gestionnaire de sécurité pour le multi-tool"""
    
    # Patterns de validation
    PATTERNS = {
        'ip': r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
        'domain': r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$',
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'url': r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&/=]*)$',
        'discord_token': r'^[MN][A-Za-z\d]{23,25}\.[A-Za-z\d]{6}\.[A-Za-z\d_\-]{27,}$',
        'discord_webhook': r'^https://(?:canary\.|ptb\.)?discord(?:app)?\.com/api/webhooks/\d+/[\w-]+$',
        'discord_id': r'^\d{17,19}$',
        'port': r'^([1-9][0-9]{0,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])$',
        'username': r'^[a-zA-Z0-9_-]{3,32}$',
        'hex_color': r'^#?([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
    }
    
    # Caractères dangereux à filtrer
    DANGEROUS_CHARS = ['<', '>', '&', '"', "'", '`', '|', ';', '$', '(', ')', '{', '}', '[', ']', '\\', '\n', '\r']
    
    def __init__(self):
        """Initialisation du gestionnaire de sécurité"""
        self.encryption_key = None
    
    def validate_input(self, user_input: str, input_type: str = 'text', max_length: int = 1000) -> tuple[bool, str]:
        """
        Valide une entrée utilisateur selon son type
        
        Args:
            user_input: L'entrée à valider
            input_type: Le type d'entrée (ip, domain, email, url, etc.)
            max_length: Longueur maximale autorisée
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Vérification de la longueur
            if len(user_input) > max_length:
                return False, f"L'entrée dépasse la longueur maximale autorisée ({max_length} caractères)"
            
            # Vérification des caractères nuls
            if '\x00' in user_input:
                return False, "Caractères nuls détectés dans l'entrée"
            
            # Validation selon le type
            if input_type in self.PATTERNS:
                if not re.match(self.PATTERNS[input_type], user_input):
                    return False, f"Format {input_type} invalide"
            
            # Vérification des caractères dangereux pour les entrées texte
            if input_type == 'text':
                for char in self.DANGEROUS_CHARS:
                    if char in user_input:
                        return False, f"Caractère dangereux détecté: {char}"
            
            return True, ""
        
        except Exception as e:
            logger.error(f"Erreur lors de la validation: {str(e)}")
            return False, "Erreur lors de la validation"
    
    def sanitize_input(self, user_input: str) -> str:
        """
        Nettoie une entrée utilisateur en supprimant les caractères dangereux
        
        Args:
            user_input: L'entrée à nettoyer
        
        Returns:
            str: L'entrée nettoyée
        """
        try:
            # Suppression des caractères nuls
            sanitized = user_input.replace('\x00', '')
            
            # Suppression des caractères de contrôle
            sanitized = ''.join(char for char in sanitized if ord(char) >= 32 or char in ['\n', '\r', '\t'])
            
            # Limitation de la longueur
            sanitized = sanitized[:1000]
            
            return sanitized.strip()
        
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage: {str(e)}")
            return ""
    
    def validate_file_path(self, file_path: str, must_exist: bool = False) -> tuple[bool, str]:
        """
        Valide un chemin de fichier pour éviter les path traversal attacks
        
        Args:
            file_path: Le chemin à valider
            must_exist: Si True, vérifie que le fichier existe
        
        Returns:
            tuple: (is_valid, error_message)
        """
        try:
            # Conversion en Path pour normalisation
            path = Path(file_path).resolve()
            
            # Vérification que le chemin ne sort pas du répertoire de travail
            try:
                path.relative_to(Path.cwd())
            except ValueError:
                # Le chemin est en dehors du répertoire de travail
                # On vérifie s'il est dans un répertoire système sensible
                sensitive_dirs = ['C:\\Windows', 'C:\\Program Files', 'C:\\Program Files (x86)']
                for sensitive_dir in sensitive_dirs:
                    try:
                        path.relative_to(Path(sensitive_dir))
                        return False, "Accès à un répertoire système interdit"
                    except ValueError:
                        continue
            
            # Vérification de l'existence si requis
            if must_exist and not path.exists():
                return False, "Le fichier n'existe pas"
            
            # Vérification des caractères interdits dans les noms de fichiers Windows
            invalid_chars = ['<', '>', ':', '"', '|', '?', '*']
            for char in invalid_chars:
                if char in str(path):
                    return False, f"Caractère invalide dans le chemin: {char}"
            
            return True, ""
        
        except Exception as e:
            logger.error(f"Erreur lors de la validation du chemin: {str(e)}")
            return False, "Erreur lors de la validation du chemin"
    
    def generate_secure_password(self, length: int = 16, use_special: bool = True) -> str:
        """
        Génère un mot de passe sécurisé
        
        Args:
            length: Longueur du mot de passe
            use_special: Inclure des caractères spéciaux
        
        Returns:
            str: Le mot de passe généré
        """
        try:
            if length < 8:
                length = 8
            if length > 128:
                length = 128
            
            # Définition des caractères à utiliser
            chars = string.ascii_letters + string.digits
            if use_special:
                chars += "!@#$%^&*()-_=+[]{}|;:,.<>?"
            
            # Génération sécurisée
            password = ''.join(secrets.choice(chars) for _ in range(length))
            
            # Vérification que le mot de passe contient au moins un de chaque type
            has_upper = any(c.isupper() for c in password)
            has_lower = any(c.islower() for c in password)
            has_digit = any(c.isdigit() for c in password)
            
            # Régénération si nécessaire
            if not (has_upper and has_lower and has_digit):
                return self.generate_secure_password(length, use_special)
            
            return password
        
        except Exception as e:
            logger.error(f"Erreur lors de la génération du mot de passe: {str(e)}")
            return ""
    
    def hash_data(self, data: str, algorithm: str = 'sha256') -> str:
        """
        Hash des données avec l'algorithme spécifié
        
        Args:
            data: Les données à hasher
            algorithm: L'algorithme à utiliser (md5, sha1, sha256, sha512)
        
        Returns:
            str: Le hash en hexadécimal
        """
        try:
            data_bytes = data.encode('utf-8')
            
            if algorithm == 'md5':
                return hashlib.md5(data_bytes).hexdigest()
            elif algorithm == 'sha1':
                return hashlib.sha1(data_bytes).hexdigest()
            elif algorithm == 'sha256':
                return hashlib.sha256(data_bytes).hexdigest()
            elif algorithm == 'sha512':
                return hashlib.sha512(data_bytes).hexdigest()
            else:
                logger.warning(f"Algorithme inconnu: {algorithm}, utilisation de SHA256")
                return hashlib.sha256(data_bytes).hexdigest()
        
        except Exception as e:
            logger.error(f"Erreur lors du hashing: {str(e)}")
            return ""
    
    def generate_encryption_key(self, password: str, salt: Optional[bytes] = None) -> tuple[bytes, bytes]:
        """
        Génère une clé de chiffrement à partir d'un mot de passe
        
        Args:
            password: Le mot de passe
            salt: Le sel (généré si None)
        
        Returns:
            tuple: (key, salt)
        """
        try:
            if salt is None:
                salt = os.urandom(16)
            
            kdf = PBKDF2(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            
            return key, salt
        
        except Exception as e:
            logger.error(f"Erreur lors de la génération de la clé: {str(e)}")
            return b"", b""
    
    def encrypt_data(self, data: str, password: str) -> tuple[str, str]:
        """
        Chiffre des données avec un mot de passe
        
        Args:
            data: Les données à chiffrer
            password: Le mot de passe
        
        Returns:
            tuple: (encrypted_data, salt) en base64
        """
        try:
            # Génération de la clé
            key, salt = self.generate_encryption_key(password)
            
            # Chiffrement
            fernet = Fernet(key)
            encrypted = fernet.encrypt(data.encode())
            
            return base64.b64encode(encrypted).decode(), base64.b64encode(salt).decode()
        
        except Exception as e:
            logger.error(f"Erreur lors du chiffrement: {str(e)}")
            return "", ""
    
    def decrypt_data(self, encrypted_data: str, password: str, salt: str) -> str:
        """
        Déchiffre des données
        
        Args:
            encrypted_data: Les données chiffrées (base64)
            password: Le mot de passe
            salt: Le sel (base64)
        
        Returns:
            str: Les données déchiffrées
        """
        try:
            # Décodage
            encrypted_bytes = base64.b64decode(encrypted_data)
            salt_bytes = base64.b64decode(salt)
            
            # Génération de la clé
            key, _ = self.generate_encryption_key(password, salt_bytes)
            
            # Déchiffrement
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted_bytes)
            
            return decrypted.decode()
        
        except Exception as e:
            logger.error(f"Erreur lors du déchiffrement: {str(e)}")
            return ""
    
    def check_password_strength(self, password: str) -> tuple[int, list]:
        """
        Vérifie la force d'un mot de passe
        
        Args:
            password: Le mot de passe à vérifier
        
        Returns:
            tuple: (score (0-100), list of recommendations)
        """
        score = 0
        recommendations = []
        
        # Longueur
        length = len(password)
        if length < 8:
            recommendations.append("Le mot de passe doit contenir au moins 8 caractères")
        elif length < 12:
            score += 20
            recommendations.append("Augmentez la longueur à au moins 12 caractères")
        elif length < 16:
            score += 30
        else:
            score += 40
        
        # Majuscules
        if any(c.isupper() for c in password):
            score += 15
        else:
            recommendations.append("Ajoutez des lettres majuscules")
        
        # Minuscules
        if any(c.islower() for c in password):
            score += 15
        else:
            recommendations.append("Ajoutez des lettres minuscules")
        
        # Chiffres
        if any(c.isdigit() for c in password):
            score += 15
        else:
            recommendations.append("Ajoutez des chiffres")
        
        # Caractères spéciaux
        if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
            score += 15
        else:
            recommendations.append("Ajoutez des caractères spéciaux")
        
        # Patterns communs
        common_patterns = ['123', 'abc', 'password', 'qwerty', '111', '000']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 20
            recommendations.append("Évitez les patterns communs")
        
        # Score final
        score = max(0, min(100, score))
        
        return score, recommendations
    
    def generate_secure_token(self, length: int = 32) -> str:
        """
        Génère un token sécurisé
        
        Args:
            length: Longueur du token
        
        Returns:
            str: Le token généré
        """
        try:
            return secrets.token_urlsafe(length)
        except Exception as e:
            logger.error(f"Erreur lors de la génération du token: {str(e)}")
            return ""
    
    def rate_limit_check(self, identifier: str, max_attempts: int = 5, window_seconds: int = 60) -> bool:
        """
        Vérifie si un identifiant a dépassé la limite de tentatives
        
        Args:
            identifier: L'identifiant à vérifier
            max_attempts: Nombre maximum de tentatives
            window_seconds: Fenêtre de temps en secondes
        
        Returns:
            bool: True si la limite n'est pas dépassée
        """
        # Cette fonction nécessiterait un système de cache/stockage
        # Pour l'instant, on retourne toujours True
        # À implémenter avec Redis ou un fichier de cache
        return True
