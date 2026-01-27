"""
Module de configuration - Gestion sécurisée des paramètres
"""

import os
import configparser
from pathlib import Path
from typing import Any, Optional, Dict


class ConfigManager:
    """Gestionnaire de configuration sécurisé"""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialise le gestionnaire de configuration
        
        Args:
            config_file: Chemin vers le fichier de configuration
        """
        self.config = configparser.ConfigParser()
        self.config_file = config_file
        
        if config_file:
            self.load(config_file)
    
    def load(self, config_file: str) -> bool:
        """
        Charge un fichier de configuration
        
        Args:
            config_file: Chemin du fichier
            
        Returns:
            True si chargé avec succès
        """
        try:
            path = Path(config_file)
            if path.exists():
                self.config.read(path, encoding='utf-8')
                self.config_file = config_file
                return True
            return False
        except Exception:
            return False
    
    def save(self, config_file: Optional[str] = None) -> bool:
        """
        Sauvegarde la configuration
        
        Args:
            config_file: Chemin du fichier (utilise le fichier actuel si non spécifié)
            
        Returns:
            True si sauvegardé avec succès
        """
        try:
            file_path = config_file or self.config_file
            if not file_path:
                return False
            
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            return True
        except Exception:
            return False
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """
        Récupère une valeur de configuration
        
        Args:
            section: Section de la configuration
            key: Clé de la valeur
            fallback: Valeur par défaut
            
        Returns:
            Valeur de configuration ou fallback
        """
        try:
            return self.config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Récupère une valeur entière"""
        try:
            return self.config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Récupère une valeur booléenne"""
        try:
            return self.config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError):
            return fallback
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Définit une valeur de configuration
        
        Args:
            section: Section de la configuration
            key: Clé de la valeur
            value: Valeur à définir
        """
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))
    
    def get_section(self, section: str) -> Dict[str, str]:
        """Récupère toutes les valeurs d'une section"""
        try:
            return dict(self.config.items(section))
        except configparser.NoSectionError:
            return {}
    
    @staticmethod
    def get_env(key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Récupère une variable d'environnement
        
        Args:
            key: Nom de la variable
            default: Valeur par défaut
            
        Returns:
            Valeur de la variable ou default
        """
        return os.environ.get(key, default)
    
    @staticmethod
    def get_windows_path(path_type: str) -> Optional[str]:
        """
        Récupère un chemin Windows spécial
        
        Args:
            path_type: Type de chemin (APPDATA, TEMP, USERPROFILE, etc.)
            
        Returns:
            Chemin ou None
        """
        path_map = {
            'APPDATA': os.environ.get('APPDATA'),
            'LOCALAPPDATA': os.environ.get('LOCALAPPDATA'),
            'TEMP': os.environ.get('TEMP') or os.environ.get('TMP'),
            'USERPROFILE': os.environ.get('USERPROFILE'),
            'PROGRAMFILES': os.environ.get('ProgramFiles'),
            'PROGRAMFILES86': os.environ.get('ProgramFiles(x86)'),
            'SYSTEMROOT': os.environ.get('SystemRoot'),
            'HOME': os.environ.get('HOME') or os.environ.get('USERPROFILE')
        }
        return path_map.get(path_type.upper())
