#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration avancée - Multi-Tool Unifié
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    """Gestionnaire de configuration"""
    
    def __init__(self):
        """Initialise le gestionnaire de configuration"""
        self.config_dir = Path(__file__).parent / "config"
        self.config_file = self.config_dir / "config.json"
        self.load_config()
    
    def load_config(self):
        """Charge la configuration depuis le fichier"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config = json.load(f)
            except Exception as e:
                print(f"⚠️  Erreur lors du chargement de la config: {str(e)}")
                self.config = self.get_default_config()
        else:
            self.config = self.get_default_config()
    
    @staticmethod
    def get_default_config() -> Dict[str, Any]:
        """Retourne la configuration par défaut"""
        return {
            "version": "1.0.0",
            "appearance": {
                "theme": "dark",
                "color_output": True,
                "banner_enabled": True,
                "clear_screen_enabled": True
            },
            "network": {
                "timeout": 10,
                "retry_count": 3,
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            },
            "security": {
                "encrypt_tokens": True,
                "mask_sensitive_data": True,
                "pbkdf2_iterations": 100000,
                "log_level": "INFO"
            },
            "features": {
                "network_tools": True,
                "osint_tools": True,
                "discord_tools": True,
                "security_tools": True,
                "system_tools": True,
                "web_tools": True,
                "generators": True,
                "utilities": True,
                "webhook_tools": True,
                "configuration": True
            },
            "paths": {
                "input_dir": "input",
                "output_dir": "output",
                "logs_dir": "logs",
                "data_dir": "data"
            },
            "limits": {
                "max_workers_threads": 10,
                "max_port_scan_ports": 1000,
                "max_ip_scan_range": 256,
                "max_batch_size": 100
            }
        }
    
    def save_config(self):
        """Sauvegarde la configuration dans le fichier"""
        try:
            self.config_dir.mkdir(exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"❌ Erreur lors de la sauvegarde de la config: {str(e)}")
    
    def get(self, key: str, default=None) -> Any:
        """Récupère une clé de configuration"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k, default)
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """Définit une clé de configuration"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def create_directories(self):
        """Crée les répertoires nécessaires"""
        paths = self.get("paths", {})
        for path_key, path_value in paths.items():
            path = Path(__file__).parent / path_value
            path.mkdir(exist_ok=True)

# Instance globale
config = ConfigManager()

def initialize_config():
    """Initialise la configuration et les répertoires"""
    global config
    config = ConfigManager()
    config.create_directories()
    config.save_config()
    return config
