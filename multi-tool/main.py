#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Tool Unifié - Point d'entrée principal
Un outil de sécurité et OSINT éthique et légal

Auteur: Multi-Tool Project
Version: 1.0.0
License: MIT
"""

import os
import sys
import platform
from typing import Callable, Dict, Optional

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = CYAN = MAGENTA = WHITE = RESET = ''
    class Style:
        BRIGHT = RESET_ALL = ''

from modules.network import NetworkTools
from modules.osint import OSINTTools
from modules.crypto_tools import CryptoTools
from modules.utilities import UtilityTools
from utils.security import SecurityUtils
from utils.validators import InputValidator

VERSION = "1.0.0"
AUTHOR = "Multi-Tool Project"


def clear_screen():
    """Efface l'écran"""
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def print_banner():
    """Affiche la bannière du programme"""
    banner = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════╗
║                                                                          ║
║  {Fore.GREEN}███╗   ███╗██╗   ██╗██╗  ████████╗██╗    ████████╗ ██████╗  ██████╗ ██╗    {Fore.CYAN}║
║  {Fore.GREEN}████╗ ████║██║   ██║██║  ╚══██╔══╝██║    ╚══██╔══╝██╔═══██╗██╔═══██╗██║    {Fore.CYAN}║
║  {Fore.GREEN}██╔████╔██║██║   ██║██║     ██║   ██║       ██║   ██║   ██║██║   ██║██║    {Fore.CYAN}║
║  {Fore.GREEN}██║╚██╔╝██║██║   ██║██║     ██║   ██║       ██║   ██║   ██║██║   ██║██║    {Fore.CYAN}║
║  {Fore.GREEN}██║ ╚═╝ ██║╚██████╔╝███████╗██║   ██║       ██║   ╚██████╔╝╚██████╔╝███████╗{Fore.CYAN}║
║  {Fore.GREEN}╚═╝     ╚═╝ ╚═════╝ ╚══════╝╚═╝   ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝{Fore.CYAN}║
║                                                                          ║
║  {Fore.YELLOW}Version: {VERSION}  |  Outils de Sécurité et OSINT Éthiques{Fore.CYAN}              ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
    print(banner)


def print_menu(title: str, options: Dict[str, str]):
    """Affiche un menu formaté"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.GREEN}{Style.BRIGHT}  {title}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    for key, value in options.items():
        print(f"  {Fore.YELLOW}[{key}]{Style.RESET_ALL} {value}")
    
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")


def get_input(prompt: str, validator: Optional[Callable] = None) -> str:
    """Obtient une entrée utilisateur avec validation"""
    while True:
        try:
            user_input = input(f"\n{Fore.GREEN}> {prompt}: {Style.RESET_ALL}").strip()
            
            if validator and not validator(user_input):
                print(f"{Fore.RED}Entrée invalide. Veuillez réessayer.{Style.RESET_ALL}")
                continue
            
            return SecurityUtils.sanitize_input(user_input)
            
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Opération annulée.{Style.RESET_ALL}")
            return ""


def display_result(title: str, data: Dict):
    """Affiche les résultats de manière formatée"""
    print(f"\n{Fore.CYAN}{'─'*50}")
    print(f"{Fore.GREEN}{Style.BRIGHT}{title}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'─'*50}{Style.RESET_ALL}")
    
    for key, value in data.items():
        if value is not None and value != []:
            if isinstance(value, list):
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL}")
                for item in value:
                    print(f"    - {item}")
            elif isinstance(value, dict):
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL}")
                for k, v in value.items():
                    print(f"    {k}: {v}")
            else:
                print(f"  {Fore.YELLOW}{key}:{Style.RESET_ALL} {value}")


def pause():
    """Pause avant de continuer"""
    input(f"\n{Fore.CYAN}Appuyez sur Entrée pour continuer...{Style.RESET_ALL}")


def menu_network():
    """Menu des outils réseau"""
    while True:
        clear_screen()
        print_banner()
        print_menu("OUTILS RÉSEAU", {
            "1": "Afficher mon IP (locale et publique)",
            "2": "Ping un hôte",
            "3": "Scanner de ports",
            "4": "Recherche DNS",
            "5": "Recherche WHOIS",
            "6": "Informations IP (géolocalisation)",
            "7": "Vérifier le statut d'un site web",
            "8": "Traceroute",
            "0": "Retour au menu principal"
        })
        
        choice = get_input("Votre choix")
        
        if choice == "0":
            break
        elif choice == "1":
            result = NetworkTools.get_my_ip()
            display_result("VOS ADRESSES IP", result)
        elif choice == "2":
            host = get_input("Hôte à ping")
            if host:
                print(f"\n{Fore.YELLOW}Ping en cours...{Style.RESET_ALL}")
                result = NetworkTools.ping_host(host)
                display_result(f"RÉSULTAT PING - {host}", result)
        elif choice == "3":
            host = get_input("Hôte cible")
            if host:
                start = get_input("Port de début (défaut: 1)")
                end = get_input("Port de fin (défaut: 1024)")
                
                start_port = int(start) if start.isdigit() else 1
                end_port = int(end) if end.isdigit() else 1024
                
                print(f"\n{Fore.YELLOW}Scan en cours (ports {start_port}-{end_port})...{Style.RESET_ALL}")
                results = NetworkTools.scan_ports(host, start_port, end_port)
                
                if results:
                    print(f"\n{Fore.GREEN}Ports ouverts trouvés: {len(results)}{Style.RESET_ALL}")
                    for port in results:
                        print(f"  Port {port['port']}: {port['service']}")
                else:
                    print(f"\n{Fore.YELLOW}Aucun port ouvert trouvé.{Style.RESET_ALL}")
        elif choice == "4":
            domain = get_input("Domaine à rechercher")
            if domain and SecurityUtils.validate_domain(domain):
                result = NetworkTools.dns_lookup(domain)
                display_result(f"DNS - {domain}", result)
            else:
                print(f"{Fore.RED}Domaine invalide.{Style.RESET_ALL}")
        elif choice == "5":
            domain = get_input("Domaine pour WHOIS")
            if domain:
                print(f"\n{Fore.YELLOW}Recherche WHOIS...{Style.RESET_ALL}")
                result = NetworkTools.whois_lookup(domain)
                display_result(f"WHOIS - {domain}", result)
        elif choice == "6":
            ip = get_input("Adresse IP")
            if ip and SecurityUtils.validate_ip(ip):
                result = NetworkTools.get_ip_info(ip)
                display_result(f"INFORMATIONS IP - {ip}", result)
            else:
                print(f"{Fore.RED}Adresse IP invalide.{Style.RESET_ALL}")
        elif choice == "7":
            url = get_input("URL du site")
            if url:
                result = NetworkTools.check_website_status(url)
                display_result(f"STATUT - {url}", result)
        elif choice == "8":
            host = get_input("Hôte pour traceroute")
            if host:
                print(f"\n{Fore.YELLOW}Traceroute en cours (peut prendre du temps)...{Style.RESET_ALL}")
                hops = NetworkTools.traceroute(host)
                print(f"\n{Fore.GREEN}Résultat du traceroute:{Style.RESET_ALL}")
                for hop in hops:
                    print(f"  {hop['raw']}")
        
        pause()


def menu_osint():
    """Menu des outils OSINT"""
    while True:
        clear_screen()
        print_banner()
        print_menu("OUTILS OSINT (Renseignement Open Source)", {
            "1": "Rechercher un nom d'utilisateur",
            "2": "Informations GitHub",
            "3": "Analyser une adresse email",
            "4": "Analyser un numéro de téléphone",
            "5": "Informations site web",
            "6": "URLs recherche image inversée",
            "0": "Retour au menu principal"
        })
        
        choice = get_input("Votre choix")
        
        if choice == "0":
            break
        elif choice == "1":
            username = get_input("Nom d'utilisateur à rechercher")
            if username and InputValidator.validate_username(username):
                print(f"\n{Fore.YELLOW}Recherche en cours sur plusieurs plateformes...{Style.RESET_ALL}")
                results = OSINTTools.search_username(username)
                
                found = [r for r in results if r.get('statut') == 'Trouvé']
                print(f"\n{Fore.GREEN}Profils trouvés: {len(found)}{Style.RESET_ALL}")
                for result in results:
                    status_color = Fore.GREEN if result.get('statut') == 'Trouvé' else Fore.YELLOW
                    print(f"  {status_color}{result.get('plateforme')}: {result.get('statut')}{Style.RESET_ALL}")
                    if result.get('statut') == 'Trouvé':
                        print(f"    {Fore.CYAN}{result.get('url')}{Style.RESET_ALL}")
            else:
                print(f"{Fore.RED}Nom d'utilisateur invalide.{Style.RESET_ALL}")
        elif choice == "2":
            username = get_input("Nom d'utilisateur GitHub")
            if username:
                result = OSINTTools.get_github_info(username)
                display_result(f"GITHUB - {username}", result)
        elif choice == "3":
            email = get_input("Adresse email")
            if email and SecurityUtils.validate_email(email):
                result = OSINTTools.analyze_email(email)
                display_result(f"ANALYSE EMAIL - {email}", result)
            else:
                print(f"{Fore.RED}Email invalide.{Style.RESET_ALL}")
        elif choice == "4":
            phone = get_input("Numéro de téléphone (format international +XX...)")
            if phone:
                result = OSINTTools.analyze_phone(phone)
                display_result(f"ANALYSE TÉLÉPHONE", result)
        elif choice == "5":
            url = get_input("URL du site web")
            if url:
                print(f"\n{Fore.YELLOW}Analyse en cours...{Style.RESET_ALL}")
                result = OSINTTools.get_website_info(url)
                display_result(f"INFORMATIONS SITE", result)
        elif choice == "6":
            image_url = get_input("URL de l'image")
            if image_url:
                result = OSINTTools.reverse_image_urls(image_url)
                display_result("URLS RECHERCHE IMAGE INVERSÉE", result)
        
        pause()


def menu_crypto():
    """Menu des outils cryptographiques"""
    while True:
        clear_screen()
        print_banner()
        print_menu("OUTILS CRYPTOGRAPHIQUES", {
            "1": "Générateur de mot de passe sécurisé",
            "2": "Générateur de phrase de passe",
            "3": "Calculer le hash d'un texte",
            "4": "Calculer le hash d'un fichier",
            "5": "Identifier un type de hash",
            "6": "Encoder/Décoder Base64",
            "7": "Encoder/Décoder Hexadécimal",
            "8": "Chiffrement César",
            "9": "Code Morse",
            "10": "Évaluer la force d'un mot de passe",
            "11": "Générer un UUID/Token",
            "0": "Retour au menu principal"
        })
        
        choice = get_input("Votre choix")
        
        if choice == "0":
            break
        elif choice == "1":
            length = get_input("Longueur (8-128, défaut: 16)")
            length = int(length) if length.isdigit() else 16
            
            password = CryptoTools.generate_password(length)
            print(f"\n{Fore.GREEN}Mot de passe généré:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}{password}{Style.RESET_ALL}")
            
            strength = CryptoTools.check_password_strength(password)
            print(f"\n  Force: {strength['niveau']} (Score: {strength['score']}/9)")
        elif choice == "2":
            count = get_input("Nombre de mots (3-10, défaut: 4)")
            count = int(count) if count.isdigit() else 4
            
            passphrase = CryptoTools.generate_passphrase(count)
            print(f"\n{Fore.GREEN}Phrase de passe générée:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}{passphrase}{Style.RESET_ALL}")
        elif choice == "3":
            text = get_input("Texte à hacher")
            if text:
                print(f"\n{Fore.GREEN}Hashs calculés:{Style.RESET_ALL}")
                hashes = CryptoTools.hash_all(text)
                for algo, hash_val in hashes.items():
                    print(f"  {Fore.YELLOW}{algo}:{Style.RESET_ALL} {hash_val}")
        elif choice == "4":
            file_path = get_input("Chemin du fichier")
            if file_path:
                print(f"\n{Fore.YELLOW}Calcul en cours...{Style.RESET_ALL}")
                for algo in ['md5', 'sha1', 'sha256']:
                    hash_val = CryptoTools.hash_file(file_path, algo)
                    if hash_val:
                        print(f"  {Fore.YELLOW}{algo.upper()}:{Style.RESET_ALL} {hash_val}")
                    else:
                        print(f"{Fore.RED}Erreur: fichier introuvable ou inaccessible.{Style.RESET_ALL}")
                        break
        elif choice == "5":
            hash_str = get_input("Hash à identifier")
            if hash_str:
                types = CryptoTools.identify_hash(hash_str)
                print(f"\n{Fore.GREEN}Types possibles:{Style.RESET_ALL}")
                for t in types:
                    print(f"  - {t}")
        elif choice == "6":
            print_menu("BASE64", {"1": "Encoder", "2": "Décoder"})
            sub_choice = get_input("Votre choix")
            text = get_input("Texte")
            if text:
                if sub_choice == "1":
                    result = CryptoTools.encode_base64(text)
                    print(f"\n{Fore.GREEN}Encodé:{Style.RESET_ALL} {result}")
                else:
                    result = CryptoTools.decode_base64(text)
                    if result:
                        print(f"\n{Fore.GREEN}Décodé:{Style.RESET_ALL} {result}")
                    else:
                        print(f"{Fore.RED}Erreur de décodage.{Style.RESET_ALL}")
        elif choice == "7":
            print_menu("HEXADÉCIMAL", {"1": "Encoder", "2": "Décoder"})
            sub_choice = get_input("Votre choix")
            text = get_input("Texte")
            if text:
                if sub_choice == "1":
                    result = CryptoTools.encode_hex(text)
                    print(f"\n{Fore.GREEN}Encodé:{Style.RESET_ALL} {result}")
                else:
                    result = CryptoTools.decode_hex(text)
                    if result:
                        print(f"\n{Fore.GREEN}Décodé:{Style.RESET_ALL} {result}")
                    else:
                        print(f"{Fore.RED}Erreur de décodage.{Style.RESET_ALL}")
        elif choice == "8":
            print_menu("CHIFFREMENT CÉSAR", {"1": "Chiffrer", "2": "Déchiffrer"})
            sub_choice = get_input("Votre choix")
            text = get_input("Texte")
            shift = get_input("Décalage (défaut: 3)")
            shift = int(shift) if shift.isdigit() else 3
            
            if text:
                result = CryptoTools.caesar_cipher(text, shift, decrypt=(sub_choice == "2"))
                print(f"\n{Fore.GREEN}Résultat:{Style.RESET_ALL} {result}")
        elif choice == "9":
            print_menu("CODE MORSE", {"1": "Encoder", "2": "Décoder"})
            sub_choice = get_input("Votre choix")
            text = get_input("Texte")
            if text:
                if sub_choice == "1":
                    result = CryptoTools.morse_encode(text)
                else:
                    result = CryptoTools.morse_decode(text)
                print(f"\n{Fore.GREEN}Résultat:{Style.RESET_ALL} {result}")
        elif choice == "10":
            password = get_input("Mot de passe à évaluer")
            if password:
                result = CryptoTools.check_password_strength(password)
                display_result("ANALYSE MOT DE PASSE", result)
        elif choice == "11":
            print_menu("GÉNÉRATION", {"1": "UUID", "2": "Token hexadécimal", "3": "Token URL-safe"})
            sub_choice = get_input("Votre choix")
            
            if sub_choice == "1":
                result = CryptoTools.generate_uuid()
            elif sub_choice == "2":
                result = CryptoTools.generate_token(32, 'hex')
            else:
                result = CryptoTools.generate_token(32, 'urlsafe')
            
            print(f"\n{Fore.GREEN}Généré:{Style.RESET_ALL} {result}")
        
        pause()


def menu_utilities():
    """Menu des utilitaires"""
    while True:
        clear_screen()
        print_banner()
        print_menu("UTILITAIRES", {
            "1": "Informations système",
            "2": "Lister un répertoire",
            "3": "Informations fichier",
            "4": "Statistiques texte",
            "5": "Convertisseur couleurs",
            "6": "Convertisseur d'unités",
            "7": "Formater/Minifier JSON",
            "8": "Chronomètre",
            "9": "Compte à rebours",
            "0": "Retour au menu principal"
        })
        
        choice = get_input("Votre choix")
        
        if choice == "0":
            break
        elif choice == "1":
            result = UtilityTools.get_system_info()
            display_result("INFORMATIONS SYSTÈME", result)
        elif choice == "2":
            path = get_input("Chemin du répertoire (défaut: .)")
            path = path if path else "."
            result = UtilityTools.list_directory(path, hidden=False)
            
            if result.get('erreur'):
                print(f"{Fore.RED}Erreur: {result['erreur']}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.GREEN}Dossiers ({len(result['dossiers'])}):{Style.RESET_ALL}")
                for d in result['dossiers']:
                    print(f"  📁 {d['nom']}")
                print(f"\n{Fore.GREEN}Fichiers ({len(result['fichiers'])}):{Style.RESET_ALL}")
                for f in result['fichiers']:
                    print(f"  📄 {f['nom']} ({f['taille']} octets)")
        elif choice == "3":
            file_path = get_input("Chemin du fichier")
            if file_path:
                result = UtilityTools.file_info(file_path)
                display_result("INFORMATIONS FICHIER", result)
        elif choice == "4":
            print("Entrez votre texte (terminez par une ligne vide):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            text = '\n'.join(lines)
            
            if text:
                result = UtilityTools.text_stats(text)
                display_result("STATISTIQUES TEXTE", result)
        elif choice == "5":
            color = get_input("Couleur (#RRGGBB ou R,G,B)")
            if color:
                result = UtilityTools.color_converter(color)
                display_result("CONVERSION COULEUR", result)
        elif choice == "6":
            value = get_input("Valeur")
            from_unit = get_input("Unité source (m, km, kg, gb, etc.)")
            to_unit = get_input("Unité cible")
            
            if value and from_unit and to_unit:
                try:
                    result = UtilityTools.unit_converter(float(value), from_unit, to_unit)
                    if result is not None:
                        print(f"\n{Fore.GREEN}Résultat:{Style.RESET_ALL} {value} {from_unit} = {result:.4f} {to_unit}")
                    else:
                        print(f"{Fore.RED}Conversion non supportée.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Valeur invalide.{Style.RESET_ALL}")
        elif choice == "7":
            print_menu("JSON", {"1": "Formater (prettify)", "2": "Minifier"})
            sub_choice = get_input("Votre choix")
            json_str = get_input("JSON")
            
            if json_str:
                if sub_choice == "1":
                    result = UtilityTools.json_prettify(json_str)
                else:
                    result = UtilityTools.json_minify(json_str)
                
                if result:
                    print(f"\n{Fore.GREEN}Résultat:{Style.RESET_ALL}")
                    print(result)
                else:
                    print(f"{Fore.RED}JSON invalide.{Style.RESET_ALL}")
        elif choice == "8":
            UtilityTools.stopwatch()
        elif choice == "9":
            seconds = get_input("Durée en secondes")
            if seconds.isdigit():
                UtilityTools.countdown(int(seconds))
        
        pause()


def main_menu():
    """Menu principal"""
    while True:
        clear_screen()
        print_banner()
        print_menu("MENU PRINCIPAL", {
            "1": "Outils Réseau",
            "2": "Outils OSINT (Renseignement)",
            "3": "Outils Cryptographiques",
            "4": "Utilitaires",
            "0": "Quitter"
        })
        
        choice = get_input("Votre choix")
        
        if choice == "0":
            print(f"\n{Fore.GREEN}Merci d'avoir utilisé Multi-Tool. À bientôt!{Style.RESET_ALL}\n")
            sys.exit(0)
        elif choice == "1":
            menu_network()
        elif choice == "2":
            menu_osint()
        elif choice == "3":
            menu_crypto()
        elif choice == "4":
            menu_utilities()


def main():
    """Point d'entrée principal"""
    try:
        if platform.system() == 'Windows':
            os.system('chcp 65001 >nul 2>&1')
        
        main_menu()
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Programme interrompu par l'utilisateur.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Erreur inattendue: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
