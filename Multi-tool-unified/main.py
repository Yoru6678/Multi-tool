#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Tool Unifié - Point d'entrée principal
Auteur: Fusion de plusieurs outils (3TH1C4L, Butcher, Cyb3rtech, Discord-All-Tools-In-One, Multi-tools, fsociety)
Version: 1.0.0
Compatible: Windows 10/11, Python 3.8+
"""

import os
import sys
import time
import logging
from pathlib import Path

# Ajout du répertoire racine au path Python
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

from utils.security import SecurityManager
from utils.logger import setup_logger
from utils.ui import UI
from config.settings import Settings

# Configuration du logger sécurisé
logger = setup_logger()

class MultiToolUnified:
    """Classe principale du multi-tool unifié"""
    
    def __init__(self):
        """Initialisation du multi-tool"""
        self.settings = Settings()
        self.security = SecurityManager()
        self.ui = UI()
        self.running = True
        
        # Vérification de la compatibilité Windows
        if os.name != 'nt':
            logger.warning("Ce multi-tool est optimisé pour Windows. Certaines fonctionnalités peuvent ne pas fonctionner correctement.")
        
        # Vérification de la version Python
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 ou supérieur est requis.")
            sys.exit(1)
    
    def display_banner(self):
        """Affiche la bannière du multi-tool"""
        self.ui.clear_screen()
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ███╗   ███╗██╗   ██╗██╗  ████████╗██╗      ████████╗ ██████╗  ██████╗ ██╗ ║
║   ████╗ ████║██║   ██║██║  ╚══██╔══╝██║      ╚══██╔══╝██╔═══██╗██╔═══██╗██║ ║
║   ██╔████╔██║██║   ██║██║     ██║   ██║  █████╗██║   ██║   ██║██║   ██║██║ ║
║   ██║╚██╔╝██║██║   ██║██║     ██║   ██║  ╚════╝██║   ██║   ██║██║   ██║██║ ║
║   ██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║         ██║   ╚██████╔╝╚██████╔╝███████╗║
║   ╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝         ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝║
║                                                                              ║
║                        MULTI-TOOL UNIFIÉ ET SÉCURISÉ                         ║
║                              Version 1.0.0                                   ║
║                         Compatible Windows 10/11                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        self.ui.print_colored(banner, "cyan")
        print()
    
    def display_main_menu(self):
        """Affiche le menu principal"""
        menu = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                              MENU PRINCIPAL                                  ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  [01] Outils Réseau              [06] Outils Discord                        ║
║  [02] Outils OSINT               [07] Outils Webhook                        ║
║  [03] Outils Sécurité            [08] Générateurs                           ║
║  [04] Outils Système             [09] Utilitaires                           ║
║  [05] Outils Web                 [10] Configuration                         ║
║                                                                              ║
║  [00] Quitter                    [99] À propos                              ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        self.ui.print_colored(menu, "green")
    
    def handle_network_tools(self):
        """Gère les outils réseau"""
        from modules.network import NetworkTools
        network = NetworkTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS RÉSEAU")
            print("""
[01] Afficher mon IP publique
[02] Scanner IP
[03] Ping IP
[04] Scanner de ports
[05] Informations sur un site web
[06] Lookup DNS
[07] Traceroute
[08] Whois
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                network.show_my_ip()
            elif choice == "02":
                network.ip_scanner()
            elif choice == "03":
                network.ip_pinger()
            elif choice == "04":
                network.port_scanner()
            elif choice == "05":
                network.website_info()
            elif choice == "06":
                network.dns_lookup()
            elif choice == "07":
                network.traceroute()
            elif choice == "08":
                network.whois_lookup()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_osint_tools(self):
        """Gère les outils OSINT"""
        from modules.osint import OSINTTools
        osint = OSINTTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS OSINT")
            print("""
[01] Tracker de nom d'utilisateur
[02] Recherche d'email
[03] Recherche de numéro de téléphone
[04] Recherche d'adresse IP (GeoIP)
[05] Recherche sur les réseaux sociaux
[06] Recherche de domaine
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                osint.username_tracker()
            elif choice == "02":
                osint.email_lookup()
            elif choice == "03":
                osint.phone_lookup()
            elif choice == "04":
                osint.geoip_lookup()
            elif choice == "05":
                osint.social_media_search()
            elif choice == "06":
                osint.domain_search()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_security_tools(self):
        """Gère les outils de sécurité"""
        from modules.security_tools import SecurityTools
        sec_tools = SecurityTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS SÉCURITÉ")
            print("""
[01] Générateur de mots de passe
[02] Vérificateur de force de mot de passe
[03] Chiffrement de fichiers
[04] Déchiffrement de fichiers
[05] Hash de fichiers (MD5, SHA256, etc.)
[06] Générateur de clés
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                sec_tools.password_generator()
            elif choice == "02":
                sec_tools.password_strength_checker()
            elif choice == "03":
                sec_tools.encrypt_file()
            elif choice == "04":
                sec_tools.decrypt_file()
            elif choice == "05":
                sec_tools.file_hasher()
            elif choice == "06":
                sec_tools.key_generator()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_system_tools(self):
        """Gère les outils système"""
        from modules.system import SystemTools
        system = SystemTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS SYSTÈME")
            print("""
[01] Informations système
[02] Processus en cours
[03] Utilisation du disque
[04] Utilisation du réseau
[05] Nettoyage de fichiers temporaires
[06] Variables d'environnement
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                system.system_info()
            elif choice == "02":
                system.list_processes()
            elif choice == "03":
                system.disk_usage()
            elif choice == "04":
                system.network_usage()
            elif choice == "05":
                system.clean_temp_files()
            elif choice == "06":
                system.env_variables()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_web_tools(self):
        """Gère les outils web"""
        from modules.web import WebTools
        web = WebTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS WEB")
            print("""
[01] Scanner de vulnérabilités SQL
[02] Vérificateur de headers HTTP
[03] Extracteur de liens
[04] Vérificateur de certificat SSL
[05] Analyseur de robots.txt
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                web.sql_vulnerability_scanner()
            elif choice == "02":
                web.http_headers_checker()
            elif choice == "03":
                web.link_extractor()
            elif choice == "04":
                web.ssl_checker()
            elif choice == "05":
                web.robots_analyzer()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_discord_tools(self):
        """Gère les outils Discord"""
        from modules.discord_tools import DiscordTools
        discord = DiscordTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS DISCORD")
            self.ui.print_warning("⚠️  AVERTISSEMENT: Utilisez ces outils de manière responsable et légale uniquement!")
            print("""
[01] Informations sur un token
[02] Vérificateur de tokens
[03] Informations sur un serveur
[04] Informations sur un utilisateur (ID)
[05] Convertir ID en première partie du token
[06] Générer un lien d'invitation de bot
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                discord.token_info()
            elif choice == "02":
                discord.token_checker()
            elif choice == "03":
                discord.server_info()
            elif choice == "04":
                discord.user_info()
            elif choice == "05":
                discord.id_to_token_part()
            elif choice == "06":
                discord.bot_invite_generator()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_webhook_tools(self):
        """Gère les outils webhook"""
        from modules.webhook import WebhookTools
        webhook = WebhookTools()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS WEBHOOK")
            print("""
[01] Informations sur un webhook
[02] Envoyer un message via webhook
[03] Supprimer un webhook
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                webhook.webhook_info()
            elif choice == "02":
                webhook.webhook_sender()
            elif choice == "03":
                webhook.webhook_deleter()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_generators(self):
        """Gère les générateurs"""
        from modules.generators import Generators
        gen = Generators()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("GÉNÉRATEURS")
            print("""
[01] Générateur de mots de passe
[02] Générateur de codes Nitro Discord
[03] Générateur de noms d'utilisateur
[04] Générateur de QR codes
[05] Générateur de UUID
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                gen.password_generator()
            elif choice == "02":
                gen.nitro_generator()
            elif choice == "03":
                gen.username_generator()
            elif choice == "04":
                gen.qr_code_generator()
            elif choice == "05":
                gen.uuid_generator()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_utilities(self):
        """Gère les utilitaires"""
        from modules.utilities import Utilities
        utils = Utilities()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("UTILITAIRES")
            print("""
[01] Encodeur/Décodeur Base64
[02] Convertisseur de formats
[03] Calculatrice de hash
[04] Générateur de Lorem Ipsum
[05] Convertisseur d'unités
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                utils.base64_tool()
            elif choice == "02":
                utils.format_converter()
            elif choice == "03":
                utils.hash_calculator()
            elif choice == "04":
                utils.lorem_ipsum()
            elif choice == "05":
                utils.unit_converter()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_configuration(self):
        """Gère la configuration"""
        while True:
            self.ui.clear_screen()
            self.ui.print_header("CONFIGURATION")
            print("""
[01] Afficher la configuration actuelle
[02] Modifier les paramètres
[03] Réinitialiser la configuration
[04] Exporter la configuration
[05] Importer une configuration
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                self.settings.display_settings()
            elif choice == "02":
                self.settings.modify_settings()
            elif choice == "03":
                self.settings.reset_settings()
            elif choice == "04":
                self.settings.export_settings()
            elif choice == "05":
                self.settings.import_settings()
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def show_about(self):
        """Affiche les informations à propos"""
        self.ui.clear_screen()
        self.ui.print_header("À PROPOS")
        about_text = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                         MULTI-TOOL UNIFIÉ v1.0.0                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Ce multi-tool est une fusion sécurisée de plusieurs outils:                ║
║    • 3TH1C4L-MultiTool                                                       ║
║    • Butcher-Tools                                                           ║
║    • Cyb3rtech-Tool                                                          ║
║    • Discord-All-Tools-In-One                                                ║
║    • Multi-tools                                                             ║
║    • fsociety                                                                ║
║                                                                              ║
║  Développé avec un focus sur:                                                ║
║    ✓ Sécurité renforcée                                                      ║
║    ✓ Compatibilité Windows 10/11                                             ║
║    ✓ Validation des entrées                                                  ║
║    ✓ Chiffrement des données sensibles                                       ║
║    ✓ Logs sécurisés                                                          ║
║    ✓ Architecture modulaire                                                  ║
║                                                                              ║
║  ⚠️  AVERTISSEMENT LÉGAL:                                                     ║
║  Cet outil est fourni à des fins éducatives uniquement.                     ║
║  L'utilisateur est seul responsable de l'utilisation qu'il en fait.         ║
║  Toute utilisation malveillante est strictement interdite.                  ║
║                                                                              ║
║  Python Version: 3.8+                                                        ║
║  Plateforme: Windows 10/11                                                   ║
║  Licence: MIT                                                                ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        print(about_text)
        self.ui.pause()
    
    def run(self):
        """Boucle principale du programme"""
        try:
            # Affichage de l'avertissement légal au démarrage
            self.ui.show_legal_warning()
            
            while self.running:
                self.display_banner()
                self.display_main_menu()
                
                choice = self.ui.get_input("Votre choix")
                
                if choice == "00":
                    self.ui.print_info("Merci d'avoir utilisé Multi-Tool Unifié!")
                    self.running = False
                elif choice == "01":
                    self.handle_network_tools()
                elif choice == "02":
                    self.handle_osint_tools()
                elif choice == "03":
                    self.handle_security_tools()
                elif choice == "04":
                    self.handle_system_tools()
                elif choice == "05":
                    self.handle_web_tools()
                elif choice == "06":
                    self.handle_discord_tools()
                elif choice == "07":
                    self.handle_webhook_tools()
                elif choice == "08":
                    self.handle_generators()
                elif choice == "09":
                    self.handle_utilities()
                elif choice == "10":
                    self.handle_configuration()
                elif choice == "99":
                    self.show_about()
                else:
                    self.ui.print_error("Choix invalide. Veuillez réessayer.")
                    time.sleep(1)
        
        except KeyboardInterrupt:
            self.ui.print_warning("\n\nInterruption par l'utilisateur.")
            logger.info("Programme interrompu par l'utilisateur")
        except Exception as e:
            self.ui.print_error(f"Erreur critique: {str(e)}")
            logger.error(f"Erreur critique: {str(e)}", exc_info=True)
        finally:
            logger.info("Fermeture du Multi-Tool Unifié")


def main():
    """Point d'entrée principal"""
    try:
        # Configuration du titre de la console Windows
        if os.name == 'nt':
            os.system('title Multi-Tool Unifié v1.0.0')
        
        # Lancement du multi-tool
        app = MultiToolUnified()
        app.run()
    
    except Exception as e:
        print(f"[ERREUR FATALE] {str(e)}")
        logger.critical(f"Erreur fatale au démarrage: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
