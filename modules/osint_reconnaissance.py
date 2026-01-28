#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module OSINT Reconnaissance - Intégré depuis SIGIT
Regroupe les outils OSINT avancés: DNS, GitHub, Data Breach, etc.
"""

import requests
import dns.resolver
from typing import Dict, List
import json

class OSINTReconnaissance:
    """Effectue une reconnaissance OSINT complète"""
    
    def __init__(self):
        self.results = {}
    
    @staticmethod
    def dns_recon(domain: str) -> Dict:
        """Effectue une reconnaissance DNS"""
        print(f"  DNS Recon pour {domain}...")
        dns_records = {
            "A": [], "MX": [], "NS": [], "TXT": [], "CNAME": []
        }
        
        try:
            for record_type in dns_records.keys():
                try:
                    answers = dns.resolver.resolve(domain, record_type)
                    dns_records[record_type] = [str(rdata) for rdata in answers]
                except Exception:
                    pass
        except Exception as e:
            return {"error": str(e)}
        
        return dns_records
    
    @staticmethod
    def github_recon(username: str) -> Dict:
        """Effectue une reconnaissance GitHub"""
        print(f"  GitHub Recon pour {username}...")
        try:
            url = f"https://api.github.com/users/{username}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    "username": data.get("login"),
                    "name": data.get("name"),
                    "bio": data.get("bio"),
                    "location": data.get("location"),
                    "email": data.get("email"),
                    "blog": data.get("blog"),
                    "twitter": data.get("twitter_username"),
                    "followers": data.get("followers"),
                    "following": data.get("following"),
                    "public_repos": data.get("public_repos"),
                    "created_at": data.get("created_at")
                }
            return {"error": "Utilisateur non trouvé"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def data_breach_check(email: str) -> Dict:
        """Vérifie si un email a été compromis"""
        print(f"  Data Breach Check pour {email}...")
        try:
            # Utilise l'API Have I Been Pwned
            url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                breaches = response.json()
                return {
                    "compromised": True,
                    "breaches": [breach["Name"] for breach in breaches],
                    "count": len(breaches)
                }
            elif response.status_code == 404:
                return {"compromised": False}
            else:
                return {"error": f"Status code: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def reverse_email_lookup(email: str) -> Dict:
        """Recherche inverse sur un email"""
        print(f"  Email Lookup pour {email}...")
        try:
            # Recherche sur plusieurs sources
            # Note: Cette fonction nécessiterait des APIs payantes pour être complète
            return {
                "email": email,
                "status": "Basic lookup (API payante requise pour résultats complets)"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def full_reconnaissance(self, target: str, target_type: str = "auto") -> Dict:
        """Effectue une reconnaissance complète"""
        print(f"\n🔍 OSINT Reconnaissance pour {target}...")
        
        if target_type == "auto":
            if "@" in target:
                target_type = "email"
            elif "." in target:
                target_type = "domain"
            else:
                target_type = "username"
        
        results = {
            "target": target,
            "type": target_type,
            "data": {}
        }
        
        if target_type == "domain":
            results["data"]["dns"] = self.dns_recon(target)
        elif target_type == "username":
            results["data"]["github"] = self.github_recon(target)
        elif target_type == "email":
            results["data"]["breach_check"] = self.data_breach_check(target)
            results["data"]["email_lookup"] = self.reverse_email_lookup(target)
        
        return results


if __name__ == "__main__":
    osint = OSINTReconnaissance()
    # Example: osint.full_reconnaissance("example.com")
