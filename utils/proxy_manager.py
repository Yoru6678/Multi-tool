#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gestionnaire de proxies pour Multi-Tool Unifié
Supporte HTTP, HTTPS, SOCKS4, SOCKS5
Compatible Windows 10/11
"""

import os
import random
import requests
import logging
from pathlib import Path
from typing import List, Dict, Optional
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class ProxyManager:
    """Gestionnaire de proxies avec rotation automatique"""
    
    def __init__(self, proxy_file: str = "input/proxies.txt"):
        """
        Initialisation du gestionnaire de proxies
        
        Args:
            proxy_file: Chemin du fichier contenant les proxies
        """
        self.proxy_file = Path(proxy_file)
        self.proxies: List[Dict[str, str]] = []
        self.current_index = 0
        self.working_proxies: List[Dict[str, str]] = []
        self.failed_proxies: List[str] = []
        
        # Création du fichier si inexistant
        if not self.proxy_file.exists():
            self.proxy_file.parent.mkdir(exist_ok=True)
            self.proxy_file.touch()
            logger.info(f"Fichier de proxies créé: {self.proxy_file}")
        
        self.load_proxies()
    
    def load_proxies(self):
        """Charge les proxies depuis le fichier"""
        try:
            if not self.proxy_file.exists():
                logger.warning(f"Fichier de proxies introuvable: {self.proxy_file}")
                return
            
            with open(self.proxy_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            self.proxies = []
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxy_dict = self._parse_proxy(line)
                    if proxy_dict:
                        self.proxies.append(proxy_dict)
            
            logger.info(f"{len(self.proxies)} proxies chargés depuis {self.proxy_file}")
        
        except Exception as e:
            logger.error(f"Erreur lors du chargement des proxies: {str(e)}")
    
    def _parse_proxy(self, proxy_string: str) -> Optional[Dict[str, str]]:
        """
        Parse une chaîne de proxy en dictionnaire
        
        Formats supportés:
        - ip:port
        - protocol://ip:port
        - protocol://user:pass@ip:port
        - user:pass@ip:port
        
        Args:
            proxy_string: Chaîne représentant le proxy
        
        Returns:
            Dict avec les clés 'http' et 'https', ou None si invalide
        """
        try:
            proxy_string = proxy_string.strip()
            
            # Si pas de protocole, ajouter http://
            if '://' not in proxy_string:
                # Vérifier si format user:pass@ip:port
                if '@' in proxy_string:
                    proxy_string = f"http://{proxy_string}"
                else:
                    # Format simple ip:port
                    proxy_string = f"http://{proxy_string}"
            
            # Parser l'URL
            parsed = urlparse(proxy_string)
            
            # Vérifier que le port est présent
            if not parsed.port:
                logger.warning(f"Proxy sans port ignoré: {proxy_string}")
                return None
            
            # Construire l'URL du proxy
            if parsed.username and parsed.password:
                proxy_url = f"{parsed.scheme}://{parsed.username}:{parsed.password}@{parsed.hostname}:{parsed.port}"
            else:
                proxy_url = f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"
            
            # Retourner le dictionnaire de proxy
            return {
                'http': proxy_url,
                'https': proxy_url
            }
        
        except Exception as e:
            logger.warning(f"Erreur lors du parsing du proxy '{proxy_string}': {str(e)}")
            return None
    
    def get_random_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retourne un proxy aléatoire
        
        Returns:
            Dict avec les clés 'http' et 'https', ou None si aucun proxy
        """
        if not self.proxies:
            return None
        
        return random.choice(self.proxies)
    
    def get_next_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retourne le prochain proxy (rotation)
        
        Returns:
            Dict avec les clés 'http' et 'https', ou None si aucun proxy
        """
        if not self.proxies:
            return None
        
        proxy = self.proxies[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.proxies)
        
        return proxy
    
    def test_proxy(self, proxy: Dict[str, str], test_url: str = "https://api.ipify.org?format=json", timeout: int = 10) -> bool:
        """
        Teste si un proxy fonctionne
        
        Args:
            proxy: Dictionnaire du proxy à tester
            test_url: URL de test
            timeout: Timeout en secondes
        
        Returns:
            True si le proxy fonctionne, False sinon
        """
        try:
            response = requests.get(test_url, proxies=proxy, timeout=timeout)
            if response.status_code == 200:
                logger.info(f"Proxy fonctionnel: {proxy['http']}")
                return True
            else:
                logger.warning(f"Proxy non fonctionnel (status {response.status_code}): {proxy['http']}")
                return False
        
        except Exception as e:
            logger.warning(f"Proxy en échec: {proxy['http']} - {str(e)}")
            return False
    
    def test_all_proxies(self, test_url: str = "https://api.ipify.org?format=json", timeout: int = 10):
        """
        Teste tous les proxies et met à jour la liste des proxies fonctionnels
        
        Args:
            test_url: URL de test
            timeout: Timeout en secondes
        """
        logger.info(f"Test de {len(self.proxies)} proxies...")
        
        self.working_proxies = []
        self.failed_proxies = []
        
        for proxy in self.proxies:
            if self.test_proxy(proxy, test_url, timeout):
                self.working_proxies.append(proxy)
            else:
                self.failed_proxies.append(proxy['http'])
        
        logger.info(f"Résultats: {len(self.working_proxies)} fonctionnels, {len(self.failed_proxies)} en échec")
    
    def get_working_proxy(self) -> Optional[Dict[str, str]]:
        """
        Retourne un proxy fonctionnel (testé)
        
        Returns:
            Dict avec les clés 'http' et 'https', ou None si aucun proxy fonctionnel
        """
        if not self.working_proxies:
            logger.warning("Aucun proxy fonctionnel disponible. Testez les proxies d'abord.")
            return self.get_random_proxy()  # Fallback sur un proxy non testé
        
        return random.choice(self.working_proxies)
    
    def add_proxy(self, proxy_string: str):
        """
        Ajoute un proxy à la liste et au fichier
        
        Args:
            proxy_string: Chaîne représentant le proxy
        """
        proxy_dict = self._parse_proxy(proxy_string)
        if proxy_dict:
            self.proxies.append(proxy_dict)
            
            # Ajouter au fichier
            try:
                with open(self.proxy_file, 'a', encoding='utf-8') as f:
                    f.write(f"\n{proxy_string}")
                logger.info(f"Proxy ajouté: {proxy_string}")
            except Exception as e:
                logger.error(f"Erreur lors de l'ajout du proxy au fichier: {str(e)}")
    
    def remove_failed_proxies(self):
        """Supprime les proxies en échec de la liste et du fichier"""
        if not self.failed_proxies:
            logger.info("Aucun proxy en échec à supprimer")
            return
        
        # Filtrer les proxies fonctionnels
        self.proxies = self.working_proxies.copy()
        
        # Réécrire le fichier
        try:
            with open(self.proxy_file, 'w', encoding='utf-8') as f:
                f.write("# Proxies fonctionnels\n")
                f.write("# Format: protocol://ip:port ou protocol://user:pass@ip:port\n")
                f.write("# Protocoles supportés: http, https, socks4, socks5\n\n")
                
                for proxy in self.proxies:
                    f.write(f"{proxy['http']}\n")
            
            logger.info(f"{len(self.failed_proxies)} proxies en échec supprimés")
        
        except Exception as e:
            logger.error(f"Erreur lors de la suppression des proxies en échec: {str(e)}")
    
    def get_proxy_for_requests(self, use_proxy: bool = True) -> Optional[Dict[str, str]]:
        """
        Retourne un proxy pour requests ou None
        
        Args:
            use_proxy: Si False, retourne None (pas de proxy)
        
        Returns:
            Dict de proxy ou None
        """
        if not use_proxy:
            return None
        
        return self.get_random_proxy()
    
    def display_stats(self):
        """Affiche les statistiques des proxies"""
        print(f"\n{'='*60}")
        print(f"STATISTIQUES DES PROXIES")
        print(f"{'='*60}")
        print(f"Total de proxies chargés: {len(self.proxies)}")
        print(f"Proxies fonctionnels: {len(self.working_proxies)}")
        print(f"Proxies en échec: {len(self.failed_proxies)}")
        print(f"{'='*60}\n")


# Exemple d'utilisation
if __name__ == "__main__":
    # Configuration du logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    # Créer le gestionnaire
    proxy_mgr = ProxyManager()
    
    # Afficher les stats
    proxy_mgr.display_stats()
    
    # Tester tous les proxies
    if proxy_mgr.proxies:
        print("Test des proxies en cours...")
        proxy_mgr.test_all_proxies()
        proxy_mgr.display_stats()
        
        # Obtenir un proxy fonctionnel
        proxy = proxy_mgr.get_working_proxy()
        if proxy:
            print(f"\nProxy sélectionné: {proxy['http']}")
