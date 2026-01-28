#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de sécurité avancée - Anti-exploitation et validation
"""

import re
import logging
from typing import Optional, Tuple
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class SecurityValidator:
    """Validateur de sécurité"""
    
    @staticmethod
    def validate_url(url: str) -> Tuple[bool, str]:
        """Valide une URL"""
        try:
            result = urlparse(url)
            
            # Vérifications basiques
            if not result.scheme in ['http', 'https']:
                return False, "Protocole invalide. Utilisez http:// ou https://"
            
            if not result.netloc:
                return False, "Domaine manquant"
            
            # Vérifier les caractères suspects
            if any(char in url for char in ['<', '>', '"', "'", '`']):
                return False, "Caractères suspects détectés"
            
            return True, ""
        except Exception as e:
            logger.error(f"Erreur validation URL: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def validate_domain(domain: str) -> Tuple[bool, str]:
        """Valide un nom de domaine"""
        try:
            # Regex pour domaine valide
            pattern = r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$'
            
            if not re.match(pattern, domain.lower()):
                return False, "Domaine invalide"
            
            if len(domain) > 255:
                return False, "Domaine trop long"
            
            return True, ""
        except Exception as e:
            logger.error(f"Erreur validation domaine: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def validate_ip(ip: str) -> Tuple[bool, str]:
        """Valide une adresse IP"""
        try:
            # Regex pour IPv4
            pattern = r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
            
            if not re.match(pattern, ip):
                return False, "IP invalide"
            
            return True, ""
        except Exception as e:
            logger.error(f"Erreur validation IP: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """Valide une adresse email"""
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            
            if not re.match(pattern, email):
                return False, "Email invalide"
            
            if len(email) > 254:
                return False, "Email trop long"
            
            return True, ""
        except Exception as e:
            logger.error(f"Erreur validation email: {str(e)}")
            return False, str(e)
    
    @staticmethod
    def detect_sql_injection_attempt(text: str) -> bool:
        """Détecte une tentative de SQL injection basique"""
        try:
            sql_keywords = [
                'union', 'select', 'insert', 'update', 'delete', 'drop',
                'create', 'alter', 'exec', 'execute', 'script', 'javascript',
                'eval', 'function'
            ]
            
            text_lower = text.lower()
            
            # Vérifier la présence de guillemets/apostrophes suspectes
            if text.count("'") > 3 or text.count('"') > 3:
                return True
            
            # Vérifier les mots-clés SQL
            for keyword in sql_keywords:
                if f" {keyword} " in f" {text_lower} ":
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Erreur détection SQL injection: {str(e)}")
            return False
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """Nettoie l'entrée utilisateur"""
        try:
            # Limiter la longueur
            if len(text) > max_length:
                text = text[:max_length]
            
            # Supprimer les caractères de contrôle
            text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\t')
            
            return text
        except Exception as e:
            logger.error(f"Erreur sanitisation: {str(e)}")
            return ""
    
    @staticmethod
    def mask_token(token: str) -> str:
        """Masque un token pour l'affichage"""
        try:
            if len(token) <= 8:
                return "***"
            
            visible = token[:4] + token[-4:]
            return f"{visible}...{len(token)} chars"
        except Exception as e:
            logger.error(f"Erreur masquage token: {str(e)}")
            return "***"

class RateLimiter:
    """Limiteur de débit"""
    
    def __init__(self, max_requests: int = 100, time_window: int = 60):
        """Initialise le limiteur"""
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = {}
    
    def is_allowed(self, key: str) -> bool:
        """Vérifie si une action est autorisée"""
        try:
            import time
            now = time.time()
            
            # Nettoyer les anciennes entrées
            self.requests = {
                k: v for k, v in self.requests.items()
                if now - v < self.time_window
            }
            
            if key not in self.requests:
                self.requests[key] = []
            
            self.requests[key].append(now)
            
            # Vérifier le nombre de requêtes
            if len(self.requests[key]) > self.max_requests:
                logger.warning(f"Rate limit dépassé pour: {key}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Erreur rate limiter: {str(e)}")
            return True
