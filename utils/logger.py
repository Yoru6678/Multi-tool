#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de logging sécurisé
Compatible Windows 10/11
"""

import logging
import os
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler
import re


class SecureFormatter(logging.Formatter):
    """Formateur de logs sécurisé qui masque les données sensibles"""
    
    # Patterns de données sensibles à masquer
    SENSITIVE_PATTERNS = [
        (r'token["\s:=]+([A-Za-z0-9\._\-]{20,})', r'token=***MASKED***'),
        (r'password["\s:=]+([^\s,}]+)', r'password=***MASKED***'),
        (r'api[_\s]?key["\s:=]+([^\s,}]+)', r'api_key=***MASKED***'),
        (r'secret["\s:=]+([^\s,}]+)', r'secret=***MASKED***'),
        (r'authorization["\s:=]+([^\s,}]+)', r'authorization=***MASKED***'),
        (r'Bearer\s+[A-Za-z0-9\._\-]+', r'Bearer ***MASKED***'),
        (r'\d{13,19}', r'***ID_MASKED***'),  # Discord IDs
    ]
    
    def format(self, record):
        """Formate le message en masquant les données sensibles"""
        # Formatage standard
        message = super().format(record)
        
        # Masquage des données sensibles
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            message = re.sub(pattern, replacement, message, flags=re.IGNORECASE)
        
        return message


def setup_logger(name: str = 'multi_tool', log_dir: str = 'logs') -> logging.Logger:
    """
    Configure et retourne un logger sécurisé
    
    Args:
        name: Nom du logger
        log_dir: Répertoire des logs
    
    Returns:
        logging.Logger: Le logger configuré
    """
    # Création du répertoire de logs s'il n'existe pas
    log_path = Path(log_dir)
    log_path.mkdir(exist_ok=True)
    
    # Configuration du logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Éviter les doublons de handlers
    if logger.handlers:
        return logger
    
    # Format des logs
    log_format = SecureFormatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour fichier avec rotation
    log_file = log_path / f'multi_tool_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)
    
    # Handler pour console (seulement WARNING et plus)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)
    console_handler.setFormatter(log_format)
    
    # Ajout des handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Log de démarrage
    logger.info("="*80)
    logger.info("Multi-Tool Unifié - Démarrage du système de logging")
    logger.info(f"Fichier de log: {log_file}")
    logger.info("="*80)
    
    return logger


def log_action(logger: logging.Logger, action: str, details: dict = None, success: bool = True):
    """
    Log une action avec des détails
    
    Args:
        logger: Le logger à utiliser
        action: Description de l'action
        details: Détails supplémentaires (dict)
        success: Si l'action a réussi
    """
    status = "SUCCESS" if success else "FAILED"
    message = f"[{status}] {action}"
    
    if details:
        # Filtrage des données sensibles dans les détails
        safe_details = {}
        sensitive_keys = ['token', 'password', 'api_key', 'secret', 'authorization']
        
        for key, value in details.items():
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                safe_details[key] = "***MASKED***"
            else:
                safe_details[key] = value
        
        message += f" - Details: {safe_details}"
    
    if success:
        logger.info(message)
    else:
        logger.error(message)


def log_security_event(logger: logging.Logger, event_type: str, details: str):
    """
    Log un événement de sécurité
    
    Args:
        logger: Le logger à utiliser
        event_type: Type d'événement (VALIDATION_FAILED, SUSPICIOUS_INPUT, etc.)
        details: Détails de l'événement
    """
    logger.warning(f"[SECURITY] {event_type} - {details}")


def cleanup_old_logs(log_dir: str = 'logs', days_to_keep: int = 30):
    """
    Nettoie les anciens fichiers de logs
    
    Args:
        log_dir: Répertoire des logs
        days_to_keep: Nombre de jours à conserver
    """
    try:
        log_path = Path(log_dir)
        if not log_path.exists():
            return
        
        current_time = datetime.now()
        
        for log_file in log_path.glob('*.log*'):
            # Vérification de l'âge du fichier
            file_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            age_days = (current_time - file_time).days
            
            if age_days > days_to_keep:
                log_file.unlink()
                logging.info(f"Ancien fichier de log supprimé: {log_file}")
    
    except Exception as e:
        logging.error(f"Erreur lors du nettoyage des logs: {str(e)}")
