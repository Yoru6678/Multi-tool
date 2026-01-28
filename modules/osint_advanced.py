#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module OSINT Avancé - Intelligence Open Source
Intégration de: Butcher-Tools, Sherlock, ReconXplorer
"""

import logging
import requests
import json
from typing import Dict, List, Optional
import socket
import re

logger = logging.getLogger(__name__)


class OSINTAdvanced:
    """Outils OSINT avancés et sécurisés"""
    
    TIMEOUT = 10
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    # Dictionnaire des sites OSINT (inspiré de Sherlock)
    OSINT_SITES = {
        "GitHub": {
            "url": "https://api.github.com/users/{}",
            "method": "json",
            "key": "login"
        },
        "Twitter": {
            "url": "https://api.twitter.com/1.1/users/show.json?screen_name={}",
            "method": "json"
        },
        "Instagram": {
            "url": "https://www.instagram.com/{}/",
            "method": "regex",
            "regex": r'"user":"[^"]*"'
        },
        "YouTube": {
            "url": "https://www.youtube.com/@{}/",
            "method": "status"
        },
        "TikTok": {
            "url": "https://www.tiktok.com/@{}/",
            "method": "status"
        },
        "Reddit": {
            "url": "https://www.reddit.com/user/{}/",
            "method": "status"
        },
        "LinkedIn": {
            "url": "https://www.linkedin.com/in/{}/",
            "method": "status"
        },
        "Twitch": {
            "url": "https://www.twitch.tv/{}",
            "method": "status"
        },
    }
    
    def __init__(self):
        """Initialisation"""
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.USER_AGENT})
    
    def search_username(self, username: str) -> Dict[str, List]:
        """
        Recherche un nom d'utilisateur sur plusieurs plateformes
        
        Args:
            username: Nom d'utilisateur à rechercher
        
        Returns:
            Dict: Résultats trouvés/non trouvés
        """
        results = {
            "found": [],
            "not_found": [],
            "error": []
        }
        
        for site_name, site_info in self.OSINT_SITES.items():
            try:
                url = site_info["url"].format(username)
                method = site_info.get("method", "status")
                
                response = self.session.get(url, timeout=self.TIMEOUT)
                
                if method == "status":
                    if response.status_code == 200:
                        results["found"].append({
                            "site": site_name,
                            "url": url,
                            "status": "✓ Trouvé"
                        })
                    elif response.status_code == 404:
                        results["not_found"].append(site_name)
                    else:
                        results["error"].append(f"{site_name}: {response.status_code}")
                
                elif method == "json":
                    if response.status_code == 200:
                        data = response.json()
                        results["found"].append({
                            "site": site_name,
                            "url": url,
                            "data": data
                        })
                    else:
                        results["not_found"].append(site_name)
                
                elif method == "regex" and "regex" in site_info:
                    if re.search(site_info["regex"], response.text):
                        results["found"].append({
                            "site": site_name,
                            "url": url,
                            "status": "✓ Trouvé"
                        })
                    else:
                        results["not_found"].append(site_name)
            
            except requests.Timeout:
                results["error"].append(f"{site_name}: Timeout")
            except Exception as e:
                results["error"].append(f"{site_name}: {str(e)}")
        
        logger.info(f"Username search: {len(results['found'])} trouvés pour '{username}'")
        return results
    
    def search_email(self, email: str) -> Dict:
        """
        Recherche des informations sur un email
        
        Args:
            email: Email à rechercher
        
        Returns:
            Dict: Informations trouvées
        """
        try:
            # Validation basique
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return {"error": "Email invalide"}
            
            results = {
                "email": email,
                "valid": None,
                "services": [],
                "breaches": []
            }
            
            # Vérification domaine
            domain = email.split("@")[1]
            try:
                socket.gethostbyname(domain)
                results["valid"] = True
            except socket.gaierror:
                results["valid"] = False
            
            # Services utilisant cet email
            services_api = f"https://www.google.com/search?q=%22{email}%22"
            try:
                response = self.session.get(services_api, timeout=self.TIMEOUT)
                results["services"].append(f"Résultats Google: {response.status_code}")
            except:
                pass
            
            logger.info(f"Email search: {email}")
            return results
        
        except Exception as e:
            logger.error(f"Erreur search_email: {str(e)}")
            return {"error": str(e)}
    
    def search_phone(self, phone_number: str) -> Dict:
        """
        Recherche des informations sur un numéro de téléphone
        
        Args:
            phone_number: Numéro à rechercher
        
        Returns:
            Dict: Informations trouvées
        """
        try:
            # Nettoyage du numéro
            clean_phone = re.sub(r'[^\d+]', '', phone_number)
            
            results = {
                "phone": phone_number,
                "country": None,
                "operator": None,
                "type": None
            }
            
            # Détection pays/opérateur simple
            if clean_phone.startswith("+33"):
                results["country"] = "France"
                if clean_phone.startswith("+33 6") or clean_phone.startswith("+33 7"):
                    results["type"] = "Mobile"
                else:
                    results["type"] = "Fixe"
            elif clean_phone.startswith("+1"):
                results["country"] = "USA/Canada"
                results["type"] = "Mobile/Fixe"
            
            logger.info(f"Phone search: {phone_number}")
            return results
        
        except Exception as e:
            logger.error(f"Erreur search_phone: {str(e)}")
            return {"error": str(e)}
    
    def geoip_lookup(self, ip_address: str) -> Dict:
        """
        Recherche géolocalisation d'une IP
        
        Args:
            ip_address: Adresse IP
        
        Returns:
            Dict: Informations géolocalisation
        """
        try:
            # Validation IP
            if not re.match(r'^(\d{1,3}\.){3}\d{1,3}$', ip_address):
                return {"error": "IP invalide"}
            
            # Utilisation de services gratuits
            services = [
                f"http://ip-api.com/json/{ip_address}",
                f"http://geoip.nekudo.com/api/{ip_address}",
            ]
            
            for service in services:
                try:
                    response = self.session.get(service, timeout=self.TIMEOUT)
                    if response.status_code == 200:
                        data = response.json()
                        logger.info(f"GeoIP lookup: {ip_address}")
                        return {
                            "ip": ip_address,
                            "data": data,
                            "source": service
                        }
                except:
                    continue
            
            return {"error": "Impossible de localiser cette IP"}
        
        except Exception as e:
            logger.error(f"Erreur geoip_lookup: {str(e)}")
            return {"error": str(e)}
    
    def search_domain(self, domain: str) -> Dict:
        """
        Recherche des informations sur un domaine
        
        Args:
            domain: Domaine à rechercher
        
        Returns:
            Dict: Informations WHOIS/DNS
        """
        try:
            results = {
                "domain": domain,
                "dns": {},
                "whois": {}
            }
            
            # Résolution DNS
            try:
                ip = socket.gethostbyname(domain)
                results["dns"]["ip"] = ip
            except:
                results["dns"]["ip"] = "Non trouvée"
            
            # Autres infos DNS
            try:
                import socket
                mx = socket.getmxrrdata(domain) if hasattr(socket, 'getmxrrdata') else None
                if mx:
                    results["dns"]["mx"] = str(mx)
            except:
                pass
            
            logger.info(f"Domain search: {domain}")
            return results
        
        except Exception as e:
            logger.error(f"Erreur search_domain: {str(e)}")
            return {"error": str(e)}

    def check_pwned_email(self, email: str) -> Dict:
        """
        Vérifie si un email a été compromis via l'API HaveIBeenPwned
        
        Args:
            email: Email à vérifier
            
        Returns:
            Dict: Résultats de la recherche
        """
        import time
        try:
            # Validation de l'email
            if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                return {"error": "Email invalide"}
            
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {
                "User-Agent": self.USER_AGENT
            }

            # Respect de la politique de rate limit de l'API HIBP
            time.sleep(1.6)
            
            response = self.session.get(url, headers=headers, timeout=self.TIMEOUT)
            
            if response.status_code == 200:
                logger.info(f"HIBP: {email} a été trouvé dans des fuites de données.")
                return {"email": email, "breaches": response.json()}
            elif response.status_code == 404:
                logger.info(f"HIBP: {email} n'a été trouvé dans aucune fuite de données.")
                return {"email": email, "breaches": []}
            else:
                logger.error(f"Erreur HIBP: {response.status_code} pour {email}")
                return {"error": f"Erreur de l'API: {response.status_code}"}
        
        except requests.Timeout:
            logger.warning(f"Timeout lors de la recherche HIBP pour {email}")
            return {"error": "Timeout lors de la connexion à l'API HaveIBeenPwned"}
        except Exception as e:
            logger.error(f"Erreur inattendue dans check_pwned_email: {str(e)}")
            return {"error": f"Erreur inattendue: {str(e)}"}
