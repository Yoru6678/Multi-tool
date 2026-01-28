#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'Encryptage AES - Intégré depuis Grabbers-Deobfuscator
Fournit le chiffrement AES-256 pour sécuriser les tokens et données sensibles
"""

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
import base64
import os

class AESEncryption:
    """Gère le chiffrement AES-256 des données sensibles"""
    
    @staticmethod
    def generate_key(password: str, salt: bytes = None) -> tuple:
        """Génère une clé de chiffrement basée sur un mot de passe"""
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
    
    @staticmethod
    def encrypt_data(data: str, password: str) -> str:
        """Chiffre les données avec AES-256"""
        try:
            key, salt = AESEncryption.generate_key(password)
            cipher = Fernet(key)
            encrypted = cipher.encrypt(data.encode())
            # Ajouter le salt au début du message chiffré
            return base64.b64encode(salt + encrypted).decode()
        except Exception as e:
            raise ValueError(f"Erreur de chiffrement: {str(e)}")
    
    @staticmethod
    def decrypt_data(encrypted_data: str, password: str) -> str:
        """Déchiffre les données chiffrées avec AES-256"""
        try:
            data = base64.b64decode(encrypted_data.encode())
            salt = data[:16]
            encrypted = data[16:]
            
            key, _ = AESEncryption.generate_key(password, salt)
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted)
            return decrypted.decode()
        except Exception as e:
            raise ValueError(f"Erreur de déchiffrement: {str(e)}")
    
    @staticmethod
    def hash_data(data: str) -> str:
        """Hache les données avec SHA-256"""
        from hashlib import sha256
        return sha256(data.encode()).hexdigest()
    
    @staticmethod
    def verify_hash(data: str, hash_value: str) -> bool:
        """Vérifie si le hash correspond aux données"""
        return AESEncryption.hash_data(data) == hash_value


class TokenEncryptor:
    """Gestionnaire spécialisé pour l'encryption des tokens Discord"""
    
    def __init__(self, master_password: str = None):
        self.master_password = master_password or "default_secure_key"
    
    def encrypt_token(self, token: str) -> str:
        """Chiffre un token Discord"""
        return AESEncryption.encrypt_data(token, self.master_password)
    
    def decrypt_token(self, encrypted_token: str) -> str:
        """Déchiffre un token Discord"""
        return AESEncryption.decrypt_data(encrypted_token, self.master_password)
    
    def bulk_encrypt(self, tokens: list) -> list:
        """Chiffre plusieurs tokens en une seule opération"""
        return [self.encrypt_token(token) for token in tokens]
    
    def bulk_decrypt(self, encrypted_tokens: list) -> list:
        """Déchiffre plusieurs tokens en une seule opération"""
        return [self.decrypt_token(token) for token in encrypted_tokens]


if __name__ == "__main__":
    # Test
    test_data = "mon_donnee_sensitive"
    password = "mon_mot_de_passe_fort"
    
    encrypted = AESEncryption.encrypt_data(test_data, password)
    print(f"Chiffré: {encrypted[:50]}...")
    
    decrypted = AESEncryption.decrypt_data(encrypted, password)
    print(f"Déchiffré: {decrypted}")
    print(f"Match: {decrypted == test_data}")
