"""
Module de logging sécurisé - Journalisation sans données sensibles
"""

import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


class SecureLogger:
    """Logger sécurisé qui masque les données sensibles"""
    
    SENSITIVE_PATTERNS = [
        (r'(?i)(password|passwd|pwd)\s*[=:]\s*\S+', r'\1=***MASQUÉ***'),
        (r'(?i)(token|api_key|apikey|secret)\s*[=:]\s*\S+', r'\1=***MASQUÉ***'),
        (r'(?i)(authorization|auth)\s*[=:]\s*\S+', r'\1=***MASQUÉ***'),
        (r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '***EMAIL***'),
        (r'\b(?:\d{4}[-\s]?){3}\d{4}\b', '***CARTE***'),
    ]
    
    def __init__(
        self,
        name: str = "multi-tool",
        log_file: Optional[str] = None,
        level: int = logging.INFO
    ):
        """
        Initialise le logger sécurisé
        
        Args:
            name: Nom du logger
            log_file: Fichier de log (optionnel)
            level: Niveau de logging
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
            
            if log_file:
                log_path = Path(log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(
                    log_path,
                    encoding='utf-8'
                )
                file_handler.setLevel(level)
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
    
    def _sanitize_message(self, message: str) -> str:
        """Masque les données sensibles dans un message"""
        sanitized = message
        for pattern, replacement in self.SENSITIVE_PATTERNS:
            sanitized = re.sub(pattern, replacement, sanitized)
        return sanitized
    
    def info(self, message: str):
        """Log un message d'information"""
        self.logger.info(self._sanitize_message(message))
    
    def warning(self, message: str):
        """Log un avertissement"""
        self.logger.warning(self._sanitize_message(message))
    
    def error(self, message: str):
        """Log une erreur"""
        self.logger.error(self._sanitize_message(message))
    
    def debug(self, message: str):
        """Log un message de debug"""
        self.logger.debug(self._sanitize_message(message))
    
    def critical(self, message: str):
        """Log une erreur critique"""
        self.logger.critical(self._sanitize_message(message))
    
    def log_action(self, action: str, details: str = ""):
        """Log une action utilisateur"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        message = f"[ACTION] {action}"
        if details:
            message += f" - {self._sanitize_message(details)}"
        self.info(message)
