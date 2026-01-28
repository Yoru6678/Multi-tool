#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de User-Agents pour Multi-Tool Unifié
Rotation automatique pour éviter la détection
Compatible Windows 10/11
"""

import os
import random
import logging
from pathlib import Path
from typing import List, Optional

logger = logging.getLogger(__name__)


class UserAgentManager:
    """Gestionnaire de User-Agents avec rotation automatique"""
    
    # User-Agents par défaut (navigateurs récents)
    DEFAULT_USER_AGENTS = [
        # Chrome Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        
        # Firefox Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
        
        # Edge Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
        
        # Opera Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
        
        # Chrome macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        
        # Safari macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        
        # Chrome Linux
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        
        # Mobile Chrome Android
        "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
        
        # Mobile Safari iOS
        "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    ]
    
    def __init__(self, useragent_file: str = "input/user-agents.txt"):
        """
        Initialisation du gestionnaire de User-Agents
        
        Args:
            useragent_file: Chemin du fichier contenant les User-Agents
        """
        self.useragent_file = Path(useragent_file)
        self.user_agents: List[str] = []
        self.current_index = 0
        
        # Création du fichier si inexistant
        if not self.useragent_file.exists():
            self.useragent_file.parent.mkdir(exist_ok=True)
            self._create_default_file()
        
        self.load_user_agents()
    
    def _create_default_file(self):
        """Crée un fichier de User-Agents par défaut"""
        try:
            with open(self.useragent_file, 'w', encoding='utf-8') as f:
                f.write("# Liste de User-Agents pour Multi-Tool Unifié\n")
                f.write("# Un User-Agent par ligne\n")
                f.write("# Les lignes commençant par # sont ignorées\n\n")
                
                for ua in self.DEFAULT_USER_AGENTS:
                    f.write(f"{ua}\n")
            
            logger.info(f"Fichier de User-Agents créé: {self.useragent_file}")
        
        except Exception as e:
            logger.error(f"Erreur lors de la création du fichier de User-Agents: {str(e)}")
    
    def load_user_agents(self):
        """Charge les User-Agents depuis le fichier"""
        try:
            if not self.useragent_file.exists():
                logger.warning(f"Fichier de User-Agents introuvable: {self.useragent_file}")
                self.user_agents = self.DEFAULT_USER_AGENTS.copy()
                return
            
            with open(self.useragent_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.user_agents = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    self.user_agents.append(line)
            
            # Si aucun User-Agent valide, utiliser les défauts
            if not self.user_agents:
                logger.warning("Aucun User-Agent valide trouvé, utilisation des User-Agents par défaut")
                self.user_agents = self.DEFAULT_USER_AGENTS.copy()
            
            logger.info(f"{len(self.user_agents)} User-Agents chargés")
        
        except Exception as e:
            logger.error(f"Erreur lors du chargement des User-Agents: {str(e)}")
            self.user_agents = self.DEFAULT_USER_AGENTS.copy()
    
    def get_random_user_agent(self) -> str:
        """
        Retourne un User-Agent aléatoire
        
        Returns:
            str: User-Agent aléatoire
        """
        if not self.user_agents:
            return self.DEFAULT_USER_AGENTS[0]
        
        return random.choice(self.user_agents)
    
    def get_next_user_agent(self) -> str:
        """
        Retourne le prochain User-Agent (rotation)
        
        Returns:
            str: User-Agent suivant
        """
        if not self.user_agents:
            return self.DEFAULT_USER_AGENTS[0]
        
        user_agent = self.user_agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.user_agents)
        
        return user_agent
    
    def get_chrome_user_agent(self) -> str:
        """
        Retourne un User-Agent Chrome aléatoire
        
        Returns:
            str: User-Agent Chrome
        """
        chrome_uas = [ua for ua in self.user_agents if 'Chrome' in ua and 'Edg' not in ua and 'OPR' not in ua]
        
        if not chrome_uas:
            return self.DEFAULT_USER_AGENTS[0]
        
        return random.choice(chrome_uas)
    
    def get_firefox_user_agent(self) -> str:
        """
        Retourne un User-Agent Firefox aléatoire
        
        Returns:
            str: User-Agent Firefox
        """
        firefox_uas = [ua for ua in self.user_agents if 'Firefox' in ua]
        
        if not firefox_uas:
            return "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0"
        
        return random.choice(firefox_uas)
    
    def get_mobile_user_agent(self) -> str:
        """
        Retourne un User-Agent mobile aléatoire
        
        Returns:
            str: User-Agent mobile
        """
        mobile_uas = [ua for ua in self.user_agents if 'Mobile' in ua or 'Android' in ua or 'iPhone' in ua]
        
        if not mobile_uas:
            return "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36"
        
        return random.choice(mobile_uas)
    
    def add_user_agent(self, user_agent: str):
        """
        Ajoute un User-Agent à la liste et au fichier
        
        Args:
            user_agent: User-Agent à ajouter
        """
        if user_agent and user_agent not in self.user_agents:
            self.user_agents.append(user_agent)
            
            # Ajouter au fichier
            try:
                with open(self.useragent_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{user_agent}")
                logger.info(f"User-Agent ajouté: {user_agent[:50]}...")
            except Exception as e:
                logger.error(f"Erreur lors de l'ajout du User-Agent au fichier: {str(e)}")
    
    def get_headers(self, additional_headers: dict = None) -> dict:
        """
        Retourne des headers HTTP avec un User-Agent aléatoire
        
        Args:
            additional_headers: Headers additionnels à inclure
        
        Returns:
            dict: Headers HTTP complets
        """
        headers = {
            'User-Agent': self.get_random_user_agent(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
        }
        
        if additional_headers:
            headers.update(additional_headers)
        
        return headers
    
    def display_stats(self):
        """Affiche les statistiques des User-Agents"""
        print(f"\n{'='*60}")
        print(f"STATISTIQUES DES USER-AGENTS")
        print(f"{'='*60}")
        print(f"Total de User-Agents: {len(self.user_agents)}")
        
        # Compter par type
        chrome_count = len([ua for ua in self.user_agents if 'Chrome' in ua and 'Edg' not in ua and 'OPR' not in ua])
        firefox_count = len([ua for ua in self.user_agents if 'Firefox' in ua])
        edge_count = len([ua for ua in self.user_agents if 'Edg' in ua])
        safari_count = len([ua for ua in self.user_agents if 'Safari' in ua and 'Chrome' not in ua])
        mobile_count = len([ua for ua in self.user_agents if 'Mobile' in ua or 'Android' in ua or 'iPhone' in ua])
        
        print(f"Chrome: {chrome_count}")
        print(f"Firefox: {firefox_count}")
        print(f"Edge: {edge_count}")
        print(f"Safari: {safari_count}")
        print(f"Mobile: {mobile_count}")
        print(f"{'='*60}\n")


# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Créer le gestionnaire
    ua_mgr = UserAgentManager()
    
    # Afficher les stats
    ua_mgr.display_stats()
    
    # Obtenir des User-Agents
    print(f"User-Agent aléatoire: {ua_mgr.get_random_user_agent()}\n")
    print(f"User-Agent Chrome: {ua_mgr.get_chrome_user_agent()}\n")
    print(f"User-Agent mobile: {ua_mgr.get_mobile_user_agent()}\n")
    
    # Obtenir des headers complets
    headers = ua_mgr.get_headers()
    print("Headers HTTP complets:")
    for key, value in headers.items():
        print(f"  {key}: {value}")
