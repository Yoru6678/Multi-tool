#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module CMS Vulnerability Scanner - Intégré depuis fsociety
Détecte et teste les vulnérabilités sur WordPress, Joomla, Drupal, etc.
"""

import requests
from typing import Dict, List
from urllib.parse import urljoin

class CMSScanner:
    """Scanne les vulnérabilités des CMS populaires"""
    
    def __init__(self, target_url: str):
        self.target_url = target_url.rstrip('/')
        self.session = requests.Session()
        self.vulnerabilities = []
    
    def detect_wordpress(self) -> bool:
        """Détecte si le site utilise WordPress"""
        indicators = [
            "/wp-content/",
            "/wp-includes/",
            "/wp-admin/",
            "wp-version"
        ]
        
        for indicator in indicators:
            try:
                url = urljoin(self.target_url, indicator)
                response = self.session.get(url, timeout=5)
                if response.status_code < 400:
                    return True
            except:
                pass
        
        return False
    
    def detect_joomla(self) -> bool:
        """Détecte si le site utilise Joomla"""
        indicators = [
            "/components/",
            "/modules/",
            "/administrator/",
            "Joomla"
        ]
        
        for indicator in indicators:
            try:
                url = urljoin(self.target_url, indicator)
                response = self.session.get(url, timeout=5)
                if indicator in response.text or response.status_code < 400:
                    return True
            except:
                pass
        
        return False
    
    def detect_drupal(self) -> bool:
        """Détecte si le site utilise Drupal"""
        indicators = [
            "/sites/",
            "/modules/",
            "/themes/",
            "/misc/"
        ]
        
        for indicator in indicators:
            try:
                url = urljoin(self.target_url, indicator)
                response = self.session.get(url, timeout=5)
                if response.status_code < 400:
                    return True
            except:
                pass
        
        return False
    
    def check_wordpress_vulnerabilities(self) -> List[Dict]:
        """Vérifie les vulnérabilités WordPress"""
        vulns = []
        
        # Vérifier les fichiers sensibles
        sensitive_files = [
            ("wp-config.php", "WordPress configuration exposée"),
            ("wp-content/uploads/", "Uploads directory accessible"),
            ("readme.html", "Version détectable via readme.html"),
        ]
        
        for file, description in sensitive_files:
            try:
                url = urljoin(self.target_url, file)
                response = self.session.get(url, timeout=5)
                if response.status_code < 400:
                    vulns.append({
                        "type": "Information Disclosure",
                        "file": file,
                        "description": description
                    })
            except:
                pass
        
        return vulns
    
    def check_sql_injection(self, param: str = "id") -> Dict:
        """Teste les injections SQL basiques"""
        try:
            # Teste avec les payloads classiques
            payloads = ["1' OR '1'='1", "1 OR 1=1", "admin' --"]
            
            for payload in payloads:
                url = f"{self.target_url}?{param}={payload}"
                response = self.session.get(url, timeout=5)
                
                # Cherche les signes d'erreur SQL
                sql_errors = ["SQL", "mysql_fetch", "Warning: mysql", "syntax error"]
                if any(error in response.text for error in sql_errors):
                    return {
                        "vulnerable": True,
                        "type": "SQL Injection",
                        "parameter": param,
                        "payload": payload
                    }
            
            return {"vulnerable": False}
        except Exception as e:
            return {"error": str(e)}
    
    def full_scan(self) -> Dict:
        """Effectue un scan complet du site"""
        print(f"\n🔍 Scan CMS pour {self.target_url}...")
        
        results = {
            "target": self.target_url,
            "cms_detected": None,
            "vulnerabilities": [],
            "sql_injection": {"vulnerable": False}
        }
        
        # Détection CMS
        if self.detect_wordpress():
            results["cms_detected"] = "WordPress"
            results["vulnerabilities"] = self.check_wordpress_vulnerabilities()
        elif self.detect_joomla():
            results["cms_detected"] = "Joomla"
        elif self.detect_drupal():
            results["cms_detected"] = "Drupal"
        
        # Test SQL Injection
        results["sql_injection"] = self.check_sql_injection()
        
        return results


if __name__ == "__main__":
    scanner = CMSScanner("https://example.com")
    results = scanner.full_scan()
    print(f"\nRésultats: {results}")
