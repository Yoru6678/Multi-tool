#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Générateurs Avancés - Générateurs de données
"""

import logging
import secrets
import string
import uuid
import random
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)


class GeneratorsAdvanced:
    """Générateurs avancés de données"""
    
    def __init__(self):
        """Initialisation"""
        self.special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate_password(self, length: int = 16, include_special: bool = True, 
                         include_numbers: bool = True) -> str:
        """Génère un mot de passe aléatoire"""
        try:
            chars = string.ascii_letters
            
            if include_numbers:
                chars += string.digits
            
            if include_special:
                chars += self.special_chars
            
            password = ''.join(secrets.choice(chars) for _ in range(length))
            logger.info(f"Mot de passe généré: {length} caractères")
            return password
        except Exception as e:
            logger.error(f"Erreur generate_password: {str(e)}")
            return ""
    
    def generate_username(self, prefix: str = "", length: int = 8) -> str:
        """Génère un nom d'utilisateur aléatoire"""
        try:
            adjectives = ["cool", "fast", "smart", "swift", "cyber", "digital", "tech", "pro"]
            nouns = ["ninja", "tiger", "dragon", "falcon", "phoenix", "shadow", "storm", "wolf"]
            
            username = f"{prefix}" if prefix else ""
            username += f"{random.choice(adjectives)}{random.choice(nouns)}"
            username += f"{secrets.randbelow(10000)}"
            
            logger.info(f"Nom d'utilisateur généré: {username}")
            return username
        except Exception as e:
            logger.error(f"Erreur generate_username: {str(e)}")
            return ""
    
    def generate_uuid(self, version: int = 4) -> str:
        """Génère un UUID"""
        try:
            if version == 1:
                new_uuid = uuid.uuid1()
            elif version == 4:
                new_uuid = uuid.uuid4()
            else:
                new_uuid = uuid.uuid4()
            
            logger.info(f"UUID v{version} généré")
            return str(new_uuid)
        except Exception as e:
            logger.error(f"Erreur generate_uuid: {str(e)}")
            return ""
    
    def generate_token(self, length: int = 32) -> str:
        """Génère un token aléatoire sécurisé"""
        try:
            token = secrets.token_hex(length // 2)
            logger.info(f"Token généré: {length} caractères")
            return token
        except Exception as e:
            logger.error(f"Erreur generate_token: {str(e)}")
            return ""
    
    def generate_nitro_codes(self, count: int = 10) -> list:
        """Génère des codes Discord Nitro factices (à titre éducatif)"""
        try:
            codes = []
            for _ in range(count):
                code = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
                codes.append(code)
            
            logger.warning(f"Codes Nitro factices générés: {count}")
            return codes
        except Exception as e:
            logger.error(f"Erreur generate_nitro_codes: {str(e)}")
            return []
    
    def generate_email(self, username: Optional[str] = None, domains: Optional[list] = None) -> str:
        """Génère une adresse email"""
        try:
            if not username:
                username = self.generate_username()
            
            if not domains:
                domains = ["gmail.com", "outlook.com", "yahoo.com", "test.com", "example.com"]
            
            email = f"{username}@{random.choice(domains)}"
            logger.info(f"Email généré: {email}")
            return email
        except Exception as e:
            logger.error(f"Erreur generate_email: {str(e)}")
            return ""
    
    def generate_phone(self, country_code: str = "+1", digits: int = 10) -> str:
        """Génère un numéro de téléphone"""
        try:
            phone_number = ''.join(str(secrets.randbelow(10)) for _ in range(digits))
            phone = f"{country_code} {phone_number[:3]} {phone_number[3:6]} {phone_number[6:]}"
            logger.info(f"Numéro de téléphone généré: {phone}")
            return phone
        except Exception as e:
            logger.error(f"Erreur generate_phone: {str(e)}")
            return ""
    
    def generate_credit_card(self) -> str:
        """Génère un numéro de carte de crédit factice (à titre éducatif)"""
        try:
            # Algorithme de Luhn pour créer des numéros valides
            def luhn_checksum(card_number):
                def digits_of(n):
                    return [int(d) for d in str(n)]
                
                digits = digits_of(card_number)
                odd_digits = digits[-1::-2]
                even_digits = digits[-2::-2]
                
                checksum = sum(odd_digits)
                for d in even_digits:
                    checksum += sum(digits_of(d*2))
                
                return checksum % 10
            
            # Générer les 15 premiers chiffres
            card_number = int(''.join(str(secrets.randbelow(10)) for _ in range(15)))
            
            # Ajouter le checksum
            check_digit = (10 - luhn_checksum(card_number * 10)) % 10
            card = str(card_number) + str(check_digit)
            
            logger.warning(f"Numéro de carte de crédit factice généré")
            return card
        except Exception as e:
            logger.error(f"Erreur generate_credit_card: {str(e)}")
            return ""
    
    def generate_timestamp(self) -> dict:
        """Génère des timestamps"""
        try:
            now = datetime.now()
            return {
                "iso_format": now.isoformat(),
                "timestamp": now.timestamp(),
                "date_time": now.strftime("%Y-%m-%d %H:%M:%S"),
                "unix_timestamp": int(now.timestamp())
            }
        except Exception as e:
            logger.error(f"Erreur generate_timestamp: {str(e)}")
            return {}
    
    def generate_batch_passwords(self, count: int = 10, length: int = 16) -> list:
        """Génère un lot de mots de passe"""
        try:
            passwords = [self.generate_password(length) for _ in range(count)]
            logger.info(f"Lot de {count} mots de passe généré")
            return passwords
        except Exception as e:
            logger.error(f"Erreur generate_batch_passwords: {str(e)}")
            return []
