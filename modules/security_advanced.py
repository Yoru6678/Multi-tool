#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Sécurité Avancée - Outils de sécurité et cryptographie
"""

import logging
import hashlib
import secrets
import string
import os
import re
from typing import Tuple
from cryptography.fernet import Fernet
import base64

logger = logging.getLogger(__name__)


class SecurityAdvanced:
    """Outils sécurité avancés"""
    
    def __init__(self):
        """Initialisation"""
        pass
    
    def generate_password(self, length: int = 16, include_special: bool = True, include_numbers: bool = True) -> str:
        """Génère un mot de passe sécurisé"""
        try:
            chars = string.ascii_letters
            if include_numbers:
                chars += string.digits
            if include_special:
                chars += string.punctuation
            
            password = ''.join(secrets.choice(chars) for _ in range(length))
            logger.info(f"Mot de passe généré ({length} caractères)")
            return password
        except Exception as e:
            logger.error(f"Erreur generate_password: {str(e)}")
            return ""
    
    def check_password_strength(self, password: str) -> dict:
        """Vérifie la force d'un mot de passe"""
        try:
            score = 0
            feedback = []
            
            if len(password) < 8:
                feedback.append("❌ Trop court (minimum 8 caractères)")
            else:
                score += 1
            
            if len(password) >= 12:
                score += 1
            
            if re.search(r'[a-z]', password):
                score += 1
            else:
                feedback.append("❌ Pas de minuscules")
            
            if re.search(r'[A-Z]', password):
                score += 1
            else:
                feedback.append("❌ Pas de majuscules")
            
            if re.search(r'[0-9]', password):
                score += 1
            else:
                feedback.append("❌ Pas de chiffres")
            
            if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                score += 1
            else:
                feedback.append("❌ Pas de caractères spéciaux")
            
            strength = "Faible" if score < 2 else "Moyen" if score < 4 else "Fort" if score < 6 else "Très fort"
            
            return {
                "password_length": len(password),
                "score": score,
                "strength": strength,
                "feedback": feedback if feedback else ["✓ Bon mot de passe"]
            }
        except Exception as e:
            logger.error(f"Erreur check_password_strength: {str(e)}")
            return {}
    
    def hash_file(self, file_path: str, algorithm: str = "sha256") -> str:
        """Calcule le hash d'un fichier"""
        try:
            hash_obj = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    hash_obj.update(chunk)
            
            result = hash_obj.hexdigest()
            logger.info(f"Hash {algorithm} calculé pour {file_path}")
            return result
        except Exception as e:
            logger.error(f"Erreur hash_file: {str(e)}")
            return ""
    
    def hash_text(self, text: str, algorithm: str = "sha256") -> str:
        """Calcule le hash d'un texte"""
        try:
            hash_obj = hashlib.new(algorithm)
            hash_obj.update(text.encode())
            return hash_obj.hexdigest()
        except Exception as e:
            logger.error(f"Erreur hash_text: {str(e)}")
            return ""
    
    def encrypt_file(self, file_path: str, password: str) -> bool:
        """Chiffre un fichier"""
        try:
            # Génération d'une clé à partir du mot de passe
            key = base64.urlsafe_b64encode(
                hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)[:32]
            )
            
            cipher = Fernet(key)
            
            with open(file_path, 'rb') as f:
                data = f.read()
            
            encrypted = cipher.encrypt(data)
            
            with open(file_path + '.enc', 'wb') as f:
                f.write(encrypted)
            
            logger.info(f"Fichier chiffré: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Erreur encrypt_file: {str(e)}")
            return False
    
    def decrypt_file(self, file_path: str, password: str) -> bool:
        """Déchiffre un fichier"""
        try:
            key = base64.urlsafe_b64encode(
                hashlib.pbkdf2_hmac('sha256', password.encode(), b'salt', 100000)[:32]
            )
            
            cipher = Fernet(key)
            
            with open(file_path, 'rb') as f:
                encrypted = f.read()
            
            decrypted = cipher.decrypt(encrypted)
            
            output_path = file_path.replace('.enc', '.dec')
            with open(output_path, 'wb') as f:
                f.write(decrypted)
            
            logger.info(f"Fichier déchiffré: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Erreur decrypt_file: {str(e)}")
            return False
