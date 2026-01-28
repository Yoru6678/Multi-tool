#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module d'interface utilisateur
Compatible Windows 10/11
"""

import os
import sys
import time
from colorama import init, Fore, Back, Style
if os.name == 'nt':
    import msvcrt

# Initialisation de colorama pour Windows
init(autoreset=True)


class UI:
    """Gestionnaire d'interface utilisateur"""
    
    # Couleurs
    COLORS = {
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.BLUE,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
        'reset': Style.RESET_ALL
    }
    
    # Symboles
    SYMBOLS = {
        'success': '✓',
        'error': '✗',
        'warning': '⚠',
        'info': 'ℹ',
        'arrow': '→',
        'bullet': '•'
    }
    
    def __init__(self):
        """Initialisation de l'UI"""
        self.width = self.get_terminal_width()
    
    @staticmethod
    def get_terminal_width() -> int:
        """Retourne la largeur du terminal"""
        try:
            return os.get_terminal_size().columns
        except:
            return 80
    
    @staticmethod
    def clear_screen():
        """Efface l'écran"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_colored(self, text: str, color: str = 'white'):
        """
        Affiche du texte coloré
        
        Args:
            text: Le texte à afficher
            color: La couleur (red, green, yellow, blue, magenta, cyan, white)
        """
        color_code = self.COLORS.get(color, self.COLORS['white'])
        print(f"{color_code}{text}{Style.RESET_ALL}")
    
    def print_success(self, message: str):
        """Affiche un message de succès"""
        print(f"{Fore.GREEN}[{self.SYMBOLS['success']}] {message}{Style.RESET_ALL}")
    
    def print_error(self, message: str):
        """Affiche un message d'erreur"""
        print(f"{Fore.RED}[{self.SYMBOLS['error']}] {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str):
        """Affiche un avertissement"""
        print(f"{Fore.YELLOW}[{self.SYMBOLS['warning']}] {message}{Style.RESET_ALL}")
    
    def print_info(self, message: str):
        """Affiche une information"""
        print(f"{Fore.CYAN}[{self.SYMBOLS['info']}] {message}{Style.RESET_ALL}")
    
    def print_header(self, title: str):
        """
        Affiche un en-tête
        
        Args:
            title: Le titre de l'en-tête
        """
        width = self.width
        print()
        print(f"{Fore.CYAN}{'═' * width}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{title.center(width)}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'═' * width}{Style.RESET_ALL}")
        print()
    
    def print_separator(self, char: str = '─'):
        """Affiche un séparateur"""
        print(f"{Fore.CYAN}{char * self.width}{Style.RESET_ALL}")
    
    def get_input(self, prompt: str, secure: bool = False) -> str:
        """
        Demande une entrée utilisateur
        
        Args:
            prompt: Le message de prompt
            secure: Si True, masque l'entrée (pour les mots de passe)
        
        Returns:
            str: L'entrée utilisateur
        """
        if secure:
            import getpass
            return getpass.getpass(f"{Fore.YELLOW}[?] {prompt}: {Style.RESET_ALL}")
        else:
            return input(f"{Fore.YELLOW}[?] {prompt}: {Style.RESET_ALL}").strip()
    
    def get_choice(self, prompt: str, choices: list) -> str:
        """
        Demande un choix parmi une liste
        
        Args:
            prompt: Le message de prompt
            choices: Liste des choix possibles
        
        Returns:
            str: Le choix sélectionné
        """
        while True:
            choice = self.get_input(prompt)
            if choice in choices:
                return choice
            else:
                self.print_error(f"Choix invalide. Choisissez parmi: {', '.join(choices)}")
    
    def confirm(self, message: str) -> bool:
        """
        Demande une confirmation (Oui/Non)
        
        Args:
            message: Le message de confirmation
        
        Returns:
            bool: True si oui, False si non
        """
        response = self.get_input(f"{message} (O/N)").upper()
        return response in ['O', 'OUI', 'Y', 'YES']
    
    def pause(self, message: str = "Appuyez sur Entrée pour continuer..."):
        """
        Met en pause et attend une entrée
        
        Args:
            message: Le message à afficher
        """
        input(f"\n{Fore.YELLOW}{message}{Style.RESET_ALL}")
    
    def show_progress(self, current: int, total: int, prefix: str = '', suffix: str = ''):
        """
        Affiche une barre de progression
        
        Args:
            current: Valeur actuelle
            total: Valeur totale
            prefix: Texte avant la barre
            suffix: Texte après la barre
        """
        bar_length = 50
        filled_length = int(bar_length * current // total)
        bar = '█' * filled_length + '░' * (bar_length - filled_length)
        percent = f"{100 * current / total:.1f}"
        
        print(f'\r{Fore.CYAN}{prefix} |{bar}| {percent}% {suffix}{Style.RESET_ALL}', end='')
        
        if current == total:
            print()
    
    def animate_text(self, text: str, delay: float = 0.03):
        """
        Affiche du texte avec animation
        
        Args:
            text: Le texte à afficher
            delay: Délai entre chaque caractère
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()
    
    def show_loading(self, message: str = "Chargement", duration: float = 2.0):
        """
        Affiche une animation de chargement
        
        Args:
            message: Le message à afficher
            duration: Durée de l'animation
        """
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        
        while time.time() < end_time:
            for frame in frames:
                print(f'\r{Fore.CYAN}{frame} {message}...{Style.RESET_ALL}', end='')
                time.sleep(0.1)
                if time.time() >= end_time:
                    break
        
        print(f'\r{" " * (len(message) + 10)}\r', end='')
    
    def display_table(self, headers: list, rows: list):
        """
        Affiche un tableau
        
        Args:
            headers: Liste des en-têtes
            rows: Liste des lignes (chaque ligne est une liste)
        """
        # Calcul des largeurs de colonnes
        col_widths = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))
        
        # Affichage de l'en-tête
        header_line = ' | '.join(str(h).ljust(w) for h, w in zip(headers, col_widths))
        print(f"{Fore.CYAN}{header_line}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * len(header_line)}{Style.RESET_ALL}")
        
        # Affichage des lignes
        for row in rows:
            row_line = ' | '.join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
            print(row_line)
    
    def display_box(self, title: str, content: list, color: str = 'cyan'):
        """
        Affiche un contenu dans une boîte
        
        Args:
            title: Titre de la boîte
            content: Liste de lignes de contenu
            color: Couleur de la boîte
        """
        color_code = self.COLORS.get(color, self.COLORS['cyan'])
        
        # Calcul de la largeur
        max_width = max(len(title), max(len(line) for line in content)) + 4
        
        # Bordure supérieure
        print(f"{color_code}╔{'═' * (max_width - 2)}╗{Style.RESET_ALL}")
        
        # Titre
        print(f"{color_code}║ {title.center(max_width - 4)} ║{Style.RESET_ALL}")
        print(f"{color_code}╠{'═' * (max_width - 2)}╣{Style.RESET_ALL}")
        
        # Contenu
        for line in content:
            padding = max_width - len(line) - 4
            print(f"{color_code}║ {line}{' ' * padding} ║{Style.RESET_ALL}")
        
        # Bordure inférieure
        print(f"{color_code}╚{'═' * (max_width - 2)}╝{Style.RESET_ALL}")
    
    def show_legal_warning(self):
        """Affiche l'avertissement légal au démarrage"""
        self.clear_screen()
        
        warning = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                          ⚠️  AVERTISSEMENT LÉGAL ⚠️                           ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  Ce logiciel est fourni à des fins ÉDUCATIVES et de RECHERCHE uniquement.   ║
║                                                                              ║
║  L'utilisateur est SEUL RESPONSABLE de l'utilisation qu'il fait de cet      ║
║  outil. Les développeurs ne peuvent être tenus responsables de toute        ║
║  utilisation malveillante, illégale ou non autorisée.                       ║
║                                                                              ║
║  En utilisant ce logiciel, vous acceptez:                                   ║
║    • De respecter toutes les lois locales et internationales                ║
║    • De ne pas utiliser l'outil à des fins malveillantes                    ║
║    • D'obtenir les autorisations nécessaires avant tout test                ║
║    • D'assumer l'entière responsabilité de vos actions                      ║
║                                                                              ║
║  Toute utilisation abusive peut entraîner des poursuites judiciaires.       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
        
        self.print_colored(warning, 'yellow')
        
        if not self.confirm("\nAcceptez-vous ces conditions"):
            self.print_error("Vous devez accepter les conditions pour continuer.")
            sys.exit(0)
        
        self.print_success("Conditions acceptées. Démarrage du programme...")
        time.sleep(1)
    
    def display_menu_item(self, number: str, title: str, description: str = ""):
        """
        Affiche un élément de menu
        
        Args:
            number: Numéro de l'option
            title: Titre de l'option
            description: Description optionnelle
        """
        if description:
            print(f"{Fore.CYAN}[{Fore.WHITE}{number}{Fore.CYAN}] {Fore.GREEN}{title}{Style.RESET_ALL} - {Fore.YELLOW}{description}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}[{Fore.WHITE}{number}{Fore.CYAN}] {Fore.GREEN}{title}{Style.RESET_ALL}")
