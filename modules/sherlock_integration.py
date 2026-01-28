#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Sherlock Integration - Recherche de noms d'utilisateur sur 300+ sites
Intégré depuis Sherlock Project
"""

import requests
from typing import Dict, List
import json
from pathlib import Path
import concurrent.futures

class SherlockSearch:
    """Effectue des recherches de noms d'utilisateur sur plusieurs plateformes"""
    
    def __init__(self):
        self.sites_info = {}
        self.results = {}
        self.session = requests.Session()
        self.load_sites_database()
    
    def load_sites_database(self):
        """Charge la base de données des sites"""
        # Sites les plus populaires pour commencer
        self.sites_info = {
            "Discord": {
                "url": "https://discord.com/api/v9/users/@{username}",
                "error_type": "status_code",
                "status_code": 404
            },
            "Twitter": {
                "url": "https://twitter.com/{username}",
                "error_type": "text",
                "error_text": "This page doesn\'t exist"
            },
            "Instagram": {
                "url": "https://www.instagram.com/{username}",
                "error_type": "status_code",
                "status_code": 404
            },
            "GitHub": {
                "url": "https://api.github.com/users/{username}",
                "error_type": "status_code",
                "status_code": 404
            },
            "Reddit": {
                "url": "https://www.reddit.com/user/{username}/about.json",
                "error_type": "status_code",
                "status_code": 404
            },
            "YouTube": {
                "url": "https://www.youtube.com/c/{username}/about",
                "error_type": "text",
                "error_text": "This page isn\'t available"
            },
            "TikTok": {
                "url": "https://www.tiktok.com/@{username}",
                "error_type": "status_code",
                "status_code": 404
            },
            "LinkedIn": {
                "url": "https://www.linkedin.com/in/{username}/",
                "error_type": "status_code",
                "status_code": 999
            },
            "Twitch": {
                "url": "https://api.twitch.tv/kraken/users/{username}",
                "error_type": "status_code",
                "status_code": 404
            },
            "Facebook": {
                "url": "https://www.facebook.com/{username}",
                "error_type": "text",
                "error_text": "We couldn\'t find this page"
            }
        }
    
    def check_username_on_site(self, username: str, site: str, site_info: Dict) -> Dict:
        """Vérifie si un username existe sur un site spécifique"""
        try:
            url = site_info["url"].format(username=username)
            response = self.session.get(url, timeout=10)
            
            if site_info.get("error_type") == "status_code":
                if response.status_code != site_info["status_code"]:
                    return {"site": site, "found": True, "url": url}
            elif site_info.get("error_type") == "text":
                if site_info["error_text"] not in response.text:
                    return {"site": site, "found": True, "url": url}
            
            return {"site": site, "found": False, "url": url}
        
        except Exception as e:
            return {"site": site, "found": False, "error": str(e), "url": url}
    
    def search_username(self, username: str, max_workers: int = 10) -> Dict:
        """Recherche un username sur tous les sites"""
        print(f"\n🔍 Recherche de '{username}' sur {len(self.sites_info)} sites...")
        
        found_accounts = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.check_username_on_site, username, site, info): site
                for site, info in self.sites_info.items()
            }
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result["found"]:
                    found_accounts.append(result)
                    print(f"  ✅ Trouvé sur {result['site']}: {result['url']}")
        
        self.results[username] = found_accounts
        return {"username": username, "found_accounts": found_accounts, "total": len(found_accounts)}
    
    def bulk_search(self, usernames: List[str]) -> Dict:
        """Effectue des recherches en masse"""
        results = {}
        for username in usernames:
            results[username] = self.search_username(username)
        return results
    
    def export_results(self, filename: str = "sherlock_results.json"):
        """Exporte les résultats en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.results, f, indent=2, ensure_ascii=False)
        print(f"\n  Résultats exportés vers {filename}")


if __name__ == "__main__":
    sherlock = SherlockSearch()
    results = sherlock.search_username("admin")
    print(f"\nRésultats: {len(results['found_accounts'])} comptes trouvés")
