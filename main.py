#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Tool Unifié - Point d'entrée principal
Auteur: Fusion de plusieurs outils (3TH1C4L, Butcher, Cyb3rtech, Discord-All-Tools-In-One, Multi-tools, fsociety)
Intégration & Consolidation: by Gsx
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
║                                 by Gsx                                       ║
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
        from modules.network_advanced import NetworkAdvanced
        network = NetworkAdvanced()
        
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
                ip = network.get_public_ip()
                if ip:
                    self.ui.print_success(f"Votre IP publique: {ip}")
                else:
                    self.ui.print_error("Impossible de récupérer votre IP")
            elif choice == "02":
                ip_range = self.ui.get_input("Plage IP (ex: 192.168.1.1-192.168.1.254)")
                results = network.ip_scanner(ip_range)
                if "error" in results:
                    self.ui.print_error(results["error"])
                else:
                    self.ui.print_success(f"IPs actives trouvées: {len(results['active'])}")
                    for ip in results["active"][:10]:
                        print(f"  ✓ {ip}")
            elif choice == "03":
                ip = self.ui.get_input("Adresse IP")
                import subprocess, platform
                try:
                    if platform.system().lower() == 'windows':
                        result = subprocess.run(['ping', '-n', '4', ip], capture_output=True)
                    else:
                        result = subprocess.run(['ping', '-c', '4', ip], capture_output=True)
                    self.ui.print_success("Ping effectué")
                except Exception as e:
                    self.ui.print_error(str(e))
            elif choice == "04":
                target = self.ui.get_input("Cible (IP ou domaine)")
                ports = self.ui.get_input("Ports (ex: 1-1024 ou 22,80,443)", "1-65535")
                results = network.port_scanner(target, ports)
                if "error" in results:
                    self.ui.print_error(results["error"])
                else:
                    self.ui.print_success(f"Ports ouverts: {len(results['open'])}")
                    for port in results["open"][:10]:
                        print(f"  ✓ Port {port}")
            elif choice == "05":
                domain = self.ui.get_input("Domaine")
                try:
                    response = __import__('requests').get(f"http://{domain}", timeout=5)
                    self.ui.print_success(f"Site accessible (HTTP {response.status_code})")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "06":
                domain = self.ui.get_input("Domaine")
                results = network.dns_lookup(domain)
                if "error" not in results:
                    self.ui.print_success(f"Résolutions trouvées:")
                    if results.get("a"):
                        print(f"  A: {results['a']}")
                else:
                    self.ui.print_error(results["error"])
            elif choice == "07":
                target = self.ui.get_input("Cible")
                hops = network.traceroute(target)
                self.ui.print_success(f"Hops trouvés: {len(hops)}")
            elif choice == "08":
                domain = self.ui.get_input("Domaine")
                results = network.whois_lookup(domain)
                self.ui.print_success(f"WHOIS lookup: {domain}")
                if "raw_response" in results:
                    print(results["raw_response"])
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_osint_tools(self):
        """Gère les outils OSINT"""
        from modules.osint_advanced import OSINTAdvanced
        osint = OSINTAdvanced()
        
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
                username = self.ui.get_input("Nom d'utilisateur")
                results = osint.search_username(username)
                self.ui.print_success(f"Résultats trouvés: {len(results['found'])}")
                for item in results['found'][:5]:
                    print(f"  ✓ {item['site']}: {item.get('url', 'Trouvé')}")
            elif choice == "02":
                email = self.ui.get_input("Email")
                results = osint.search_email(email)
                if "error" not in results:
                    self.ui.print_success(f"Email: {results.get('email')}")
                    print(f"  Valide: {results.get('valid')}")
            elif choice == "03":
                phone = self.ui.get_input("Numéro de téléphone")
                results = osint.search_phone(phone)
                if "error" not in results:
                    self.ui.print_success(f"Téléphone: {results.get('phone')}")
                    print(f"  Pays: {results.get('country')}")
                    print(f"  Type: {results.get('type')}")
            elif choice == "04":
                ip = self.ui.get_input("Adresse IP")
                results = osint.geoip_lookup(ip)
                if "error" not in results:
                    self.ui.print_success(f"GeoIP: {ip}")
                    import json
                    print(json.dumps(results.get('data', {}), indent=2)[:500])
            elif choice == "05":
                username = self.ui.get_input("Nom d'utilisateur")
                results = osint.search_username(username)
                self.ui.print_success(f"Profils trouvés: {len(results['found'])}")
            elif choice == "06":
                domain = self.ui.get_input("Domaine")
                results = osint.search_domain(domain)
                if "error" not in results:
                    self.ui.print_success(f"Domaine: {domain}")
                    print(f"  IP: {results['dns'].get('ip')}")
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_security_tools(self):
        """Gère les outils de sécurité"""
        from modules.security_advanced import SecurityAdvanced
        sec = SecurityAdvanced()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS SÉCURITÉ")
            print("""
[01] Générateur de mots de passe
[02] Vérificateur de force de mot de passe
[03] Chiffrement de fichiers
[04] Déchiffrement de fichiers
[05] Hash de fichiers
[06] Hash de texte
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                try:
                    length = self.ui.get_input("Longueur (défaut: 16)", default="16")
                    password = sec.generate_password(int(length))
                    self.ui.print_success("Mot de passe généré")
                    print(f"  {password}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "02":
                try:
                    password = self.ui.get_input("Mot de passe")
                    strength = sec.check_password_strength(password)
                    self.ui.print_success("Force du mot de passe")
                    print(f"  Niveau: {strength['strength']}")
                    print(f"  Score: {strength['score']}/5")
                    for feedback in strength['feedback'][:3]:
                        print(f"  • {feedback}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "03":
                try:
                    file_path = self.ui.get_input("Chemin du fichier")
                    password = self.ui.get_input("Mot de passe de chiffrement")
                    result = sec.encrypt_file(file_path, password)
                    if "error" not in result:
                        self.ui.print_success("Fichier chiffré")
                        print(f"  Fichier: {result.get('encrypted_file')}")
                    else:
                        self.ui.print_error(f"Erreur: {result.get('error')}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "04":
                try:
                    file_path = self.ui.get_input("Chemin du fichier")
                    password = self.ui.get_input("Mot de passe de déchiffrement")
                    result = sec.decrypt_file(file_path, password)
                    if "error" not in result:
                        self.ui.print_success("Fichier déchiffré")
                        print(f"  Fichier: {result.get('decrypted_file')}")
                    else:
                        self.ui.print_error(f"Erreur: {result.get('error')}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "05":
                try:
                    file_path = self.ui.get_input("Chemin du fichier")
                    algorithm = self.ui.get_input("Algorithme [sha256|md5|sha1|sha512]", default="sha256")
                    hash_result = sec.hash_file(file_path, algorithm)
                    self.ui.print_success(f"Hash de fichier ({algorithm})")
                    print(f"  {hash_result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "06":
                try:
                    text = self.ui.get_input("Texte")
                    algorithm = self.ui.get_input("Algorithme [sha256|md5|sha1|sha512]", default="sha256")
                    hash_result = sec.hash_text(text, algorithm)
                    self.ui.print_success(f"Hash de texte ({algorithm})")
                    print(f"  {hash_result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_system_tools(self):
        """Gère les outils système"""
        from modules.system_advanced import SystemAdvanced
        system = SystemAdvanced()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS SYSTÈME")
            print("""
[01] Informations système
[02] Informations CPU
[03] Utilisation de la mémoire
[04] Utilisation du disque
[05] Informations réseau
[06] Processus en cours
[07] Boot time
[08] Variables d'environnement
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                try:
                    info = system.get_system_info()
                    self.ui.print_success("Informations système")
                    for key, value in info.items():
                        print(f"  {key}: {value}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "02":
                try:
                    cpu_info = system.get_cpu_info()
                    self.ui.print_success("Informations CPU")
                    for key, value in cpu_info.items():
                        print(f"  {key}: {value}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "03":
                try:
                    mem_info = system.get_memory_info()
                    self.ui.print_success("Utilisation mémoire")
                    for key, value in mem_info.items():
                        print(f"  {key}: {value}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "04":
                try:
                    disk_info = system.get_disk_info()
                    self.ui.print_success("Utilisation disque")
                    for partition, stats in disk_info.items():
                        print(f"\n  {partition}:")
                        for key, value in stats.items():
                            print(f"    {key}: {value}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "05":
                try:
                    net_info = system.get_network_info()
                    self.ui.print_success("Informations réseau")
                    for key, value in net_info.items():
                        if isinstance(value, dict):
                            print(f"  {key}:")
                            for k, v in value.items():
                                print(f"    {k}: {v}")
                        else:
                            print(f"  {key}: {value}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "06":
                try:
                    processes = system.list_processes()
                    self.ui.print_success("Top 20 processus (par mémoire)")
                    for proc in processes[:10]:
                        print(f"  {proc}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "07":
                try:
                    boot_time = system.get_boot_time()
                    self.ui.print_success(f"Heure du dernier démarrage: {boot_time}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "08":
                try:
                    env = system.get_environment_variables()
                    self.ui.print_success("Variables d'environnement")
                    for key, value in list(env.items())[:10]:
                        print(f"  {key}: {value}")
                    print(f"  ... et {len(env) - 10} autres")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_web_tools(self):
        """Gère les outils web"""
        from modules.web_advanced import WebAdvanced
        web = WebAdvanced()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("OUTILS WEB")
            print("""
[01] Scanner de vulnérabilités SQL
[02] Vérificateur de headers HTTP
[03] Extracteur de liens
[04] Vérificateur de certificat SSL
[05] Analyseur de robots.txt
[06] Test de disponibilité
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                try:
                    url = self.ui.get_input("URL cible (ex: http://example.com)")
                    if not url.startswith('http'):
                        url = 'http://' + url
                    results = web.sql_injection_scanner(url)
                    self.ui.print_success("Scanner SQL Injection")
                    print(f"  Payloads testés: {results.get('payloads_tested', 0)}")
                    if results.get('vulnerable_params'):
                        self.ui.print_warning(f"  ⚠️  Vulnérabilités détectées: {len(results['vulnerable_params'])}")
                    else:
                        self.ui.print_success("  ✓ Aucune vulnérabilité évidente détectée")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "02":
                try:
                    url = self.ui.get_input("URL (ex: http://example.com)")
                    if not url.startswith('http'):
                        url = 'http://' + url
                    results = web.check_http_headers(url)
                    self.ui.print_success("Vérification des headers HTTP")
                    print(f"  Status code: {results.get('status_code')}")
                    print(f"  Headers de sécurité présents: {len(results.get('present', {}))}")
                    if results.get('missing'):
                        self.ui.print_warning(f"  ⚠️  Headers manquants: {len(results['missing'])}")
                        for h in results['missing'][:3]:
                            print(f"    - {h}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "03":
                try:
                    url = self.ui.get_input("URL (ex: http://example.com)")
                    if not url.startswith('http'):
                        url = 'http://' + url
                    links = web.extract_links(url)
                    self.ui.print_success(f"Liens extraits: {len(links)}")
                    for link in links[:5]:
                        print(f"  • {link}")
                    if len(links) > 5:
                        print(f"  ... et {len(links) - 5} autres liens")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "04":
                try:
                    domain = self.ui.get_input("Domaine (ex: example.com)")
                    results = web.check_ssl_certificate(domain)
                    self.ui.print_success("Certificat SSL")
                    if results.get('valid'):
                        print(f"  ✓ Certificat valide")
                        print(f"  Émetteur: {results.get('issuer', {}).get('commonName', 'Unknown')}")
                        print(f"  Expire: {results.get('not_after', 'Unknown')}")
                    else:
                        self.ui.print_warning(f"  ⚠️  Certificat invalide: {results.get('error', 'Unknown error')}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "05":
                try:
                    url = self.ui.get_input("URL (ex: http://example.com)")
                    if not url.startswith('http'):
                        url = 'http://' + url
                    disallowed = web.check_robots_txt(url)
                    if disallowed:
                        self.ui.print_success(f"robots.txt trouvé - {len(disallowed)} règles")
                        for rule in disallowed[:5]:
                            print(f"  {rule}")
                    else:
                        print("  Aucun robots.txt trouvé")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "06":
                try:
                    url = self.ui.get_input("URL (ex: http://example.com)")
                    if not url.startswith('http'):
                        url = 'http://' + url
                    results = web.test_website_availability(url)
                    if results.get('available'):
                        self.ui.print_success("Site disponible")
                        print(f"  Status: {results.get('status_code')}")
                        print(f"  Temps réponse: {results.get('response_time_ms', 0):.2f}ms")
                        print(f"  Serveur: {results.get('server', 'Unknown')}")
                    else:
                        self.ui.print_error(f"  Site indisponible: {results.get('error', 'Unknown error')}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_discord_tools(self):
        """Gère les outils Discord"""
        from modules.discord_advanced import DiscordAdvanced
        discord = DiscordAdvanced()
        
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
                token = self.ui.get_input("Token Discord", secure=True)
                valid, data = discord.validate_token(token)
                if valid:
                    self.ui.print_success("Token valide!")
                    print(f"  Utilisateur: {data.get('username')}")
                    print(f"  Email: {data.get('email')}")
                    print(f"  Nitro: {'✓ Oui' if data.get('nitro') else '✗ Non'}")
                else:
                    self.ui.print_error("Token invalide")
            elif choice == "02":
                token_list = self.ui.get_input("Tokens (séparés par virgule)")
                tokens = [t.strip() for t in token_list.split(',')]
                results = discord.check_tokens_batch(tokens)
                self.ui.print_success(f"Valides: {len(results['valid'])}")
                for item in results['valid'][:5]:
                    print(f"  ✓ {item['token']}")
            elif choice == "03":
                server_id = self.ui.get_input("ID serveur Discord")
                token = self.ui.get_input("Token Discord (optionnel)", secure=True)
                if token:
                    info = discord.get_server_info(server_id, token)
                    if info:
                        self.ui.print_success(f"Serveur: {info.get('name')}")
                        print(f"  Membres: {info.get('members')}")
            elif choice == "04":
                user_id = self.ui.get_input("ID utilisateur Discord")
                token = self.ui.get_input("Token Discord", secure=True)
                info = discord.get_user_info(user_id, token)
                if info:
                    self.ui.print_success(f"Utilisateur: {info.get('username')}")
            elif choice == "05":
                user_id = self.ui.get_input("ID utilisateur Discord")
                import base64
                try:
                    encoded = base64.b64encode(user_id.encode()).decode()
                    self.ui.print_info(f"Première partie (approx): {encoded[:20]}...")
                except:
                    pass
            elif choice == "06":
                bot_id = self.ui.get_input("ID du bot Discord")
                permissions = "8"
                invite = f"https://discord.com/api/oauth2/authorize?client_id={bot_id}&permissions={permissions}&scope=bot"
                self.ui.print_success(f"Lien généré")
                print(f"  {invite}")
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
        from modules.generators_advanced import GeneratorsAdvanced
        gen = GeneratorsAdvanced()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("GÉNÉRATEURS")
            print("""
[01] Générateur de mots de passe
[02] Générateur de codes Nitro Discord
[03] Générateur de noms d'utilisateur
[04] Générateur de UUID
[05] Générateur de tokens
[06] Générateur d'emails
[07] Générateur de numéros de téléphone
[08] Batch de mots de passe
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                try:
                    length = self.ui.get_input("Longueur (défaut: 16)", default="16")
                    password = gen.generate_password(int(length))
                    self.ui.print_success("Mot de passe généré")
                    print(f"  {password}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "02":
                try:
                    count = self.ui.get_input("Nombre de codes (défaut: 5)", default="5")
                    codes = gen.generate_nitro_codes(int(count))
                    self.ui.print_success(f"Codes Nitro générés: {len(codes)}")
                    for code in codes[:5]:
                        print(f"  {code}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "03":
                try:
                    username = gen.generate_username()
                    self.ui.print_success("Nom d'utilisateur généré")
                    print(f"  {username}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "04":
                try:
                    uuid_str = gen.generate_uuid()
                    self.ui.print_success("UUID généré")
                    print(f"  {uuid_str}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "05":
                try:
                    token = gen.generate_token()
                    self.ui.print_success("Token généré")
                    print(f"  {token}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "06":
                try:
                    email = gen.generate_email()
                    self.ui.print_success("Email généré")
                    print(f"  {email}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "07":
                try:
                    phone = gen.generate_phone()
                    self.ui.print_success("Numéro de téléphone généré")
                    print(f"  {phone}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "08":
                try:
                    count = self.ui.get_input("Nombre de mots de passe (défaut: 10)", default="10")
                    passwords = gen.generate_batch_passwords(int(count))
                    self.ui.print_success(f"Batch de {len(passwords)} mots de passe")
                    for pwd in passwords[:5]:
                        print(f"  {pwd}")
                    if len(passwords) > 5:
                        print(f"  ... et {len(passwords) - 5} autres")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            else:
                self.ui.print_error("Choix invalide")
            
            if choice != "00":
                self.ui.pause()
    
    def handle_utilities(self):
        """Gère les utilitaires"""
        from modules.utilities_advanced import UtilitiesAdvanced
        utils = UtilitiesAdvanced()
        
        while True:
            self.ui.clear_screen()
            self.ui.print_header("UTILITAIRES")
            print("""
[01] Encodeur/Décodeur Base64
[02] Encodeur/Décodeur Hex
[03] Encodeur/Décodeur URL
[04] ROT13 Encoder
[05] Calculatrice de hash
[06] Formatage JSON
[07] Extraction de données (emails, URLs, IPs)
[08] Compteurs (lignes, mots, caractères)
[09] Convertisseur de casse
[10] Inverse une chaîne
[00] Retour au menu principal
""")
            
            choice = self.ui.get_input("Votre choix")
            
            if choice == "00":
                break
            elif choice == "01":
                try:
                    self.ui.print_info("Base64 Encoder/Decoder")
                    mode = self.ui.get_input("[1] Encoder  [2] Decoder")
                    text = self.ui.get_input("Texte")
                    if mode == "1":
                        result = utils.base64_encode(text)
                    else:
                        result = utils.base64_decode(text)
                    self.ui.print_success("Résultat")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "02":
                try:
                    self.ui.print_info("Hex Encoder/Decoder")
                    mode = self.ui.get_input("[1] Encoder  [2] Decoder")
                    text = self.ui.get_input("Texte")
                    if mode == "1":
                        result = utils.hex_encode(text)
                    else:
                        result = utils.hex_decode(text)
                    self.ui.print_success("Résultat")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "03":
                try:
                    self.ui.print_info("URL Encoder/Decoder")
                    mode = self.ui.get_input("[1] Encoder  [2] Decoder")
                    text = self.ui.get_input("Texte")
                    if mode == "1":
                        result = utils.url_encode(text)
                    else:
                        result = utils.url_decode(text)
                    self.ui.print_success("Résultat")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "04":
                try:
                    text = self.ui.get_input("Texte")
                    result = utils.rot13_encode(text)
                    self.ui.print_success("ROT13 Encodé")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "05":
                try:
                    self.ui.print_info("Calculatrice de Hash")
                    algo = self.ui.get_input("Algorithme [md5|sha1|sha256|sha512]", default="sha256")
                    text = self.ui.get_input("Texte")
                    result = utils.calculate_hash(text, algo)
                    self.ui.print_success(f"Hash ({algo})")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "06":
                try:
                    self.ui.print_info("Formatage JSON")
                    mode = self.ui.get_input("[1] Format  [2] Minify")
                    json_str = self.ui.get_input("JSON")
                    if mode == "1":
                        result = utils.json_format(json_str)
                    else:
                        result = utils.json_minify(json_str)
                    self.ui.print_success("JSON résultat")
                    print(f"  {result[:500]}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "07":
                try:
                    text = self.ui.get_input("Texte")
                    self.ui.print_success("Extraction de données")
                    emails = utils.extract_emails(text)
                    urls = utils.extract_urls(text)
                    ips = utils.extract_ips(text)
                    print(f"  Emails: {len(emails)}")
                    for email in emails[:3]:
                        print(f"    • {email}")
                    print(f"  URLs: {len(urls)}")
                    for url in urls[:3]:
                        print(f"    • {url}")
                    print(f"  IPs: {len(ips)}")
                    for ip in ips[:3]:
                        print(f"    • {ip}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "08":
                try:
                    text = self.ui.get_input("Texte")
                    lines = utils.line_counter(text)
                    words = utils.word_counter(text)
                    chars = utils.char_counter(text)
                    self.ui.print_success("Compteurs")
                    print(f"  Lignes: {lines}")
                    print(f"  Mots: {words}")
                    print(f"  Caractères: {chars}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "09":
                try:
                    text = self.ui.get_input("Texte")
                    case_type = self.ui.get_input("[upper|lower|title]", default="upper")
                    result = utils.convert_case(text, case_type)
                    self.ui.print_success(f"Convertis en {case_type}")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
            elif choice == "10":
                try:
                    text = self.ui.get_input("Texte")
                    result = utils.reverse_string(text)
                    self.ui.print_success("Chaîne inversée")
                    print(f"  {result}")
                except Exception as e:
                    self.ui.print_error(f"Erreur: {str(e)}")
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
║                    MULTI-TOOL UNIFIÉ v1.0.0 - by Gsx                         ║
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
║  Intégration & Consolidation: by Gsx                                         ║
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
