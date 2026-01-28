#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Web Avancé - Outils web et sécurité web
"""

import logging
import requests
import re
import ssl
import socket
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)


class WebAdvanced:
    """Outils web avancés"""
    
    def __init__(self):
        """Initialisation"""
        self.timeout = 10
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    def sql_injection_scanner(self, url: str) -> Dict:
        """Scanner les vulnérabilités SQL Injection"""
        try:
            payloads = [
                "' OR '1'='1",
                "' OR 1=1--",
                "' OR 'a'='a",
                "1' UNION SELECT NULL--"
            ]
            
            results = {
                "url": url,
                "vulnerable_params": [],
                "payloads_tested": len(payloads)
            }
            
            for payload in payloads:
                try:
                    response = requests.get(
                        url,
                        params={"id": payload},
                        timeout=self.timeout,
                        headers={"User-Agent": self.user_agent}
                    )
                    
                    # Détection simple
                    if any(keyword in response.text.lower() for keyword in ['mysql', 'syntax error', 'sql']):
                        results["vulnerable_params"].append(payload)
                except:
                    pass
            
            logger.info(f"SQL injection scan: {url}")
            return results
        except Exception as e:
            logger.error(f"Erreur sql_injection_scanner: {str(e)}")
            return {}
    
    def check_http_headers(self, url: str) -> Dict:
        """Vérifie les headers de sécurité HTTP"""
        try:
            response = requests.head(url, timeout=self.timeout, allow_redirects=True)
            
            security_headers = [
                "X-Frame-Options",
                "X-Content-Type-Options",
                "X-XSS-Protection",
                "Strict-Transport-Security",
                "Content-Security-Policy",
                "Access-Control-Allow-Origin"
            ]
            
            results = {
                "url": url,
                "status_code": response.status_code,
                "present": {},
                "missing": []
            }
            
            for header in security_headers:
                if header in response.headers:
                    results["present"][header] = response.headers[header]
                else:
                    results["missing"].append(header)
            
            logger.info(f"HTTP headers check: {url}")
            return results
        except Exception as e:
            logger.error(f"Erreur check_http_headers: {str(e)}")
            return {}
    
    def extract_links(self, url: str) -> List[str]:
        """Extrait tous les liens d'une page"""
        try:
            response = requests.get(
                url,
                timeout=self.timeout,
                headers={"User-Agent": self.user_agent}
            )
            
            # Regex pour extraire les liens
            links = re.findall(r'href=["\'](.*?)["\']', response.text)
            
            # Conversion en URLs absolues
            absolute_links = []
            for link in links:
                if link.startswith(('http://', 'https://')):
                    absolute_links.append(link)
                elif link.startswith('/'):
                    absolute_links.append(urljoin(url, link))
                elif link.startswith('#'):
                    pass
                else:
                    absolute_links.append(urljoin(url, link))
            
            logger.info(f"Links extracted from {url}: {len(absolute_links)} liens")
            return list(set(absolute_links))[:20]
        except Exception as e:
            logger.error(f"Erreur extract_links: {str(e)}")
            return []
    
    def check_ssl_certificate(self, domain: str) -> Dict:
        """Vérifie le certificat SSL"""
        try:
            context = ssl.create_default_context()
            
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    return {
                        "domain": domain,
                        "subject": dict(x[0] for x in cert['subject']),
                        "issuer": dict(x[0] for x in cert['issuer']),
                        "not_before": cert['notBefore'],
                        "not_after": cert['notAfter'],
                        "valid": True
                    }
        except ssl.SSLError as e:
            logger.warning(f"SSL error pour {domain}: {str(e)}")
            return {"domain": domain, "valid": False, "error": str(e)}
        except Exception as e:
            logger.error(f"Erreur check_ssl_certificate: {str(e)}")
            return {"domain": domain, "valid": False, "error": str(e)}
    
    def check_robots_txt(self, url: str) -> List[str]:
        """Analyse le fichier robots.txt"""
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            
            response = requests.get(robots_url, timeout=self.timeout)
            
            if response.status_code == 200:
                lines = response.text.split('\n')
                disallowed = [line for line in lines if line.startswith('Disallow:')]
                logger.info(f"robots.txt trouvé pour {url}")
                return disallowed
            
            return []
        except Exception as e:
            logger.error(f"Erreur check_robots_txt: {str(e)}")
            return []
    
    def test_website_availability(self, url: str) -> Dict:
        """Teste la disponibilité d'un site"""
        try:
            response = requests.get(url, timeout=self.timeout)
            
            return {
                "url": url,
                "status_code": response.status_code,
                "response_time_ms": response.elapsed.total_seconds() * 1000,
                "available": response.status_code < 400,
                "server": response.headers.get("Server", "Unknown"),
                "content_type": response.headers.get("Content-Type", "Unknown")
            }
        except requests.Timeout:
            return {"url": url, "error": "Timeout", "available": False}
        except requests.ConnectionError:
            return {"url": url, "error": "Connection error", "available": False}
        except Exception as e:
            logger.error(f"Erreur test_website_availability: {str(e)}")
            return {"url": url, "error": str(e), "available": False}
