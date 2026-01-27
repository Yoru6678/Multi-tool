"""
Module de validation - Validation des entrées utilisateur
"""

import re
from typing import Optional, Tuple, Any


class InputValidator:
    """Classe pour valider les entrées utilisateur"""
    
    @staticmethod
    def validate_port(port: Any) -> Tuple[bool, Optional[int]]:
        """
        Valide un numéro de port
        
        Args:
            port: Port à valider (int ou str)
            
        Returns:
            Tuple (valide, port_int)
        """
        try:
            port_int = int(port)
            if 1 <= port_int <= 65535:
                return True, port_int
            return False, None
        except (ValueError, TypeError):
            return False, None
    
    @staticmethod
    def validate_port_range(start: Any, end: Any) -> Tuple[bool, Optional[Tuple[int, int]]]:
        """
        Valide une plage de ports
        
        Args:
            start: Port de début
            end: Port de fin
            
        Returns:
            Tuple (valide, (start_int, end_int))
        """
        valid_start, start_int = InputValidator.validate_port(start)
        valid_end, end_int = InputValidator.validate_port(end)
        
        if valid_start and valid_end and start_int <= end_int:
            return True, (start_int, end_int)
        return False, None
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Valide un nom d'utilisateur
        
        Args:
            username: Nom d'utilisateur à valider
            
        Returns:
            True si valide
        """
        if not username or len(username) > 50:
            return False
        
        pattern = r'^[a-zA-Z0-9_.-]+$'
        return bool(re.match(pattern, username))
    
    @staticmethod
    def validate_positive_int(value: Any, max_value: int = 1000000) -> Tuple[bool, Optional[int]]:
        """
        Valide un entier positif
        
        Args:
            value: Valeur à valider
            max_value: Valeur maximale autorisée
            
        Returns:
            Tuple (valide, valeur_int)
        """
        try:
            int_val = int(value)
            if 0 < int_val <= max_value:
                return True, int_val
            return False, None
        except (ValueError, TypeError):
            return False, None
    
    @staticmethod
    def validate_choice(choice: str, valid_choices: list) -> bool:
        """
        Valide un choix parmi une liste
        
        Args:
            choice: Choix de l'utilisateur
            valid_choices: Liste des choix valides
            
        Returns:
            True si le choix est valide
        """
        return choice.strip().lower() in [str(c).lower() for c in valid_choices]
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """
        Valide un numéro de téléphone international
        
        Args:
            phone: Numéro de téléphone à valider
            
        Returns:
            True si valide
        """
        cleaned = re.sub(r'[\s\-\(\)]', '', phone)
        pattern = r'^\+?[0-9]{8,15}$'
        return bool(re.match(pattern, cleaned))
    
    @staticmethod
    def validate_hash(hash_string: str, hash_type: str = 'md5') -> bool:
        """
        Valide un hash selon son type
        
        Args:
            hash_string: Hash à valider
            hash_type: Type de hash (md5, sha1, sha256, sha512)
            
        Returns:
            True si le format est valide
        """
        lengths = {
            'md5': 32,
            'sha1': 40,
            'sha256': 64,
            'sha512': 128
        }
        
        expected_length = lengths.get(hash_type.lower())
        if not expected_length:
            return False
        
        pattern = f'^[a-fA-F0-9]{{{expected_length}}}$'
        return bool(re.match(pattern, hash_string))
