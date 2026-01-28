#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Proxy Scraper - Intégré depuis Nexus-MultiTool
Scrape et valide des proxies desde plusieurs sources
"""

import requests
from typing import List, Dict
import concurrent.futures
import time

class ProxyScraper:
    """Scrape des proxies depuis plusieurs sources"""
    
    PROXY_SOURCES = [
        "https://www.proxy-list.download/api/v1/get?type=http",
        "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
    ]
    
    def __init__(self, timeout: int = 5):
        self.timeout = timeout
        self.proxies = []
        self.valid_proxies = []
    
    @staticmethod
    def fetch_proxies_from_source(source: str) -> List[str]:
        """Récupère les proxies d'une source"""
        proxies = []
        try:
            response = requests.get(source, timeout=10)
            if response.status_code == 200:
                if source.endswith('.json'):
                    data = response.json()
                    if isinstance(data, dict) and 'data' in data:
                        proxies = [p['ip_address'] + ':' + p['port'] for p in data['data']['proxies']]
                else:
                    # Format texte
                    proxies = [line.strip() for line in response.text.split('\n') if line.strip()]
        except Exception as e:
            pass
        
        return proxies
    
    def scrape_all_sources(self) -> List[str]:
        """Scrape toutes les sources de proxies"""
        print("  Scraping des proxies...")
        all_proxies = set()
        
        for source in self.PROXY_SOURCES:
            proxies = self.fetch_proxies_from_source(source)
            all_proxies.update(proxies)
            print(f"    - {len(proxies)} proxies de {source.split('/')[2]}")
        
        self.proxies = list(all_proxies)
        print(f"  Total: {len(self.proxies)} proxies uniques")
        return self.proxies
    
    def validate_proxy(self, proxy: str) -> bool:
        """Valide un proxy en testant une connexion"""
        try:
            test_url = "http://httpbin.org/ip"
            proxy_dict = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            response = requests.get(test_url, proxies=proxy_dict, timeout=self.timeout)
            return response.status_code == 200
        except Exception:
            return False
    
    def validate_all_proxies(self, max_workers: int = 10) -> List[str]:
        """Valide tous les proxies en parallèle"""
        print("  Validation des proxies...")
        valid = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(self.validate_proxy, proxy): proxy 
                      for proxy in self.proxies}
            
            for i, future in enumerate(concurrent.futures.as_completed(futures)):
                if future.result():
                    valid.append(futures[future])
                if (i + 1) % 10 == 0:
                    print(f"    - Testés: {i + 1}/{len(self.proxies)}")
        
        self.valid_proxies = valid
        print(f"  Proxies valides: {len(self.valid_proxies)}")
        return self.valid_proxies
    
    def get_random_proxy(self) -> str:
        """Retourne un proxy aléatoire"""
        import random
        return random.choice(self.valid_proxies) if self.valid_proxies else None
    
    def export_to_file(self, filename: str = "valid_proxies.txt"):
        """Exporte les proxies valides vers un fichier"""
        with open(filename, 'w') as f:
            f.write('\n'.join(self.valid_proxies))
        print(f"  Proxies exportés vers {filename}")
    
    def get_formatted_proxies(self) -> List[Dict]:
        """Retourne les proxies au format formaté"""
        return [{"http": f"http://{proxy}", "https": f"http://{proxy}"} 
                for proxy in self.valid_proxies]


if __name__ == "__main__":
    scraper = ProxyScraper()
    proxies = scraper.scrape_all_sources()
    valid = scraper.validate_all_proxies(max_workers=5)
