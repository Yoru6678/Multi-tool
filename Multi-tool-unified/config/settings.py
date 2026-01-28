#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module de configuration et paramètres
Compatible Windows 10/11
"""

import os
import json
import configparser
from pathlib import Path
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


class Settings:
    """Gestionnaire de configuration"""
    
    DEFAULT_SETTINGS = {
        'general': {
            'language': 'fr',
            'theme': 'default',
            'log_level': 'INFO',
            'auto_update': 'false',
        },
        'security': {
            'mask_sensitive_data': 'true',
            'require_confirmation': 'true',
            'max_retries': '3',
            'timeout': '30',
        },
        'network': {
            'default_timeout': '10',
            'max_threads': '10',
            'use_proxy': 'false',
            'proxy_url': '',
        },
        'paths': {
            'output_dir': 'output',
            'temp_dir': 'temp',
            'log_dir': 'logs',
        }
    }
    
    def __init__(self, config_file: str = 'config/config.ini'):
        """
        Initialisation des paramètres
        
        Args:
            config_file: Chemin du fichier de configuration
        """
        self.config_file = Path(config_file)
        self.config = configparser.ConfigParser()
        
        # Création du répertoire de configuration si nécessaire
        self.config_file.parent.mkdir(exist_ok=True)
        
        # Chargement ou création de la configuration
        if self.config_file.exists():
            self.load_settings()
        else:
            self.create_default_config()
    
    def create_default_config(self):
        """Crée un fichier de configuration par défaut"""
        try:
            for section, options in self.DEFAULT_SETTINGS.items():
                self.config[section] = options
            
            self.save_settings()
            logger.info(f"Configuration par défaut créée: {self.config_file}")
        
        except Exception as e:
            logger.error(f"Erreur lors de la création de la configuration: {str(e)}")
    
    def load_settings(self):
        """Charge les paramètres depuis le fichier"""
        try:
            self.config.read(self.config_file, encoding='utf-8')
            logger.info(f"Configuration chargée depuis: {self.config_file}")
        
        except Exception as e:
            logger.error(f"Erreur lors du chargement de la configuration: {str(e)}")
            self.create_default_config()
    
    def save_settings(self):
        """Sauvegarde les paramètres dans le fichier"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            logger.info(f"Configuration sauvegardée dans: {self.config_file}")
        
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
    
    def get(self, section: str, option: str, fallback: Any = None) -> str:
        """
        Récupère une valeur de configuration
        
        Args:
            section: Section de la configuration
            option: Option à récupérer
            fallback: Valeur par défaut si non trouvée
        
        Returns:
            str: La valeur de configuration
        """
        try:
            return self.config.get(section, option, fallback=fallback)
        except Exception as e:
            logger.warning(f"Erreur lors de la récupération de {section}.{option}: {str(e)}")
            return fallback
    
    def set(self, section: str, option: str, value: str):
        """
        Définit une valeur de configuration
        
        Args:
            section: Section de la configuration
            option: Option à définir
            value: Valeur à définir
        """
        try:
            if section not in self.config:
                self.config[section] = {}
            
            self.config[section][option] = str(value)
            self.save_settings()
        
        except Exception as e:
            logger.error(f"Erreur lors de la définition de {section}.{option}: {str(e)}")
    
    def get_bool(self, section: str, option: str, fallback: bool = False) -> bool:
        """
        Récupère une valeur booléenne
        
        Args:
            section: Section de la configuration
            option: Option à récupérer
            fallback: Valeur par défaut
        
        Returns:
            bool: La valeur booléenne
        """
        try:
            return self.config.getboolean(section, option, fallback=fallback)
        except Exception as e:
            logger.warning(f"Erreur lors de la récupération de {section}.{option}: {str(e)}")
            return fallback
    
    def get_int(self, section: str, option: str, fallback: int = 0) -> int:
        """
        Récupère une valeur entière
        
        Args:
            section: Section de la configuration
            option: Option à récupérer
            fallback: Valeur par défaut
        
        Returns:
            int: La valeur entière
        """
        try:
            return self.config.getint(section, option, fallback=fallback)
        except Exception as e:
            logger.warning(f"Erreur lors de la récupération de {section}.{option}: {str(e)}")
            return fallback
    
    def display_settings(self):
        """Affiche tous les paramètres"""
        from utils.ui import UI
        ui = UI()
        
        ui.print_header("CONFIGURATION ACTUELLE")
        
        for section in self.config.sections():
            print(f"\n{ui.COLORS['cyan']}[{section.upper()}]{ui.COLORS['reset']}")
            for option, value in self.config[section].items():
                print(f"  {ui.COLORS['green']}{option}{ui.COLORS['reset']}: {value}")
    
    def modify_settings(self):
        """Interface pour modifier les paramètres"""
        from utils.ui import UI
        ui = UI()
        
        ui.print_header("MODIFICATION DES PARAMÈTRES")
        
        # Affichage des sections
        sections = list(self.config.sections())
        for i, section in enumerate(sections, 1):
            print(f"[{i}] {section}")
        
        section_choice = ui.get_input("Choisissez une section (numéro)")
        
        try:
            section_index = int(section_choice) - 1
            if 0 <= section_index < len(sections):
                section = sections[section_index]
                
                # Affichage des options
                options = list(self.config[section].items())
                for i, (option, value) in enumerate(options, 1):
                    print(f"[{i}] {option} = {value}")
                
                option_choice = ui.get_input("Choisissez une option (numéro)")
                option_index = int(option_choice) - 1
                
                if 0 <= option_index < len(options):
                    option_name = options[option_index][0]
                    current_value = options[option_index][1]
                    
                    new_value = ui.get_input(f"Nouvelle valeur pour {option_name} (actuel: {current_value})")
                    
                    if new_value:
                        self.set(section, option_name, new_value)
                        ui.print_success(f"Paramètre {section}.{option_name} modifié avec succès")
                    else:
                        ui.print_warning("Modification annulée")
                else:
                    ui.print_error("Option invalide")
            else:
                ui.print_error("Section invalide")
        
        except ValueError:
            ui.print_error("Entrée invalide")
        except Exception as e:
            ui.print_error(f"Erreur: {str(e)}")
    
    def reset_settings(self):
        """Réinitialise les paramètres par défaut"""
        from utils.ui import UI
        ui = UI()
        
        if ui.confirm("Êtes-vous sûr de vouloir réinitialiser tous les paramètres"):
            self.config.clear()
            self.create_default_config()
            ui.print_success("Paramètres réinitialisés avec succès")
        else:
            ui.print_info("Réinitialisation annulée")
    
    def export_settings(self):
        """Exporte les paramètres vers un fichier JSON"""
        from utils.ui import UI
        ui = UI()
        
        try:
            export_file = ui.get_input("Nom du fichier d'export (sans extension)")
            if not export_file:
                export_file = "config_export"
            
            export_path = Path(f"{export_file}.json")
            
            # Conversion en dictionnaire
            config_dict = {section: dict(self.config[section]) for section in self.config.sections()}
            
            # Sauvegarde en JSON
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=4, ensure_ascii=False)
            
            ui.print_success(f"Configuration exportée vers: {export_path}")
        
        except Exception as e:
            ui.print_error(f"Erreur lors de l'export: {str(e)}")
    
    def import_settings(self):
        """Importe les paramètres depuis un fichier JSON"""
        from utils.ui import UI
        ui = UI()
        
        try:
            import_file = ui.get_input("Chemin du fichier à importer")
            import_path = Path(import_file)
            
            if not import_path.exists():
                ui.print_error("Le fichier n'existe pas")
                return
            
            # Chargement du JSON
            with open(import_path, 'r', encoding='utf-8') as f:
                config_dict = json.load(f)
            
            # Application de la configuration
            self.config.clear()
            for section, options in config_dict.items():
                self.config[section] = options
            
            self.save_settings()
            ui.print_success("Configuration importée avec succès")
        
        except json.JSONDecodeError:
            ui.print_error("Fichier JSON invalide")
        except Exception as e:
            ui.print_error(f"Erreur lors de l'import: {str(e)}")
    
    def ensure_directories(self):
        """Crée les répertoires nécessaires s'ils n'existent pas"""
        try:
            output_dir = Path(self.get('paths', 'output_dir', 'output'))
            temp_dir = Path(self.get('paths', 'temp_dir', 'temp'))
            log_dir = Path(self.get('paths', 'log_dir', 'logs'))
            
            output_dir.mkdir(exist_ok=True)
            temp_dir.mkdir(exist_ok=True)
            log_dir.mkdir(exist_ok=True)
            
            logger.info("Répertoires créés/vérifiés")
        
        except Exception as e:
            logger.error(f"Erreur lors de la création des répertoires: {str(e)}")
