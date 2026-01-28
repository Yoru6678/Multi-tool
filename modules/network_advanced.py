#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Network Avancé - Outils réseau professionnels
Intégration de: 3TH1C4L-MultiTool, Network tools
"""

import logging
import socket
import subprocess
import platform
import os
import re
import requests
from typing import Dict, List, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

logger = logging.getLogger(__name__)


class NetworkAdvanced:
    """Outils réseau avancés et sécurisés"""
    
    def __init__(self):
        """Initialisation"""
        self.timeout = 5
        self.max_threads = 10
        self.lock = threading.Lock()
    
    def get_public_ip(self) -> Optional[str]:
        """
        Récupère l'adresse IP publique
        
        Returns:
            str: Adresse IP publique
        """
        try:
            services = [
                'https://api.ipify.org?format=json',
                'https://api.myip.com',
                'https://ipinfo.io/json'
            ]
            
            for service in services:
                try:
                    response = requests.get(service, timeout=self.timeout)
                    if response.status_code == 200:
                        data = response.json()
                        ip = data.get('ip') or data.get('ipAddress')
                        if ip:
                            logger.info(f"IP publique récupérée: {ip}")
                            return ip
                except:
                    continue
            
            return None
        except Exception as e:
            logger.error(f"Erreur get_public_ip: {str(e)}")
            return None
    
    def ip_scanner(self, ip_range: str) -> Dict[str, List]:
        """
        Scanne une plage d'adresses IP
        
        Args:
            ip_range: Plage (ex: 192.168.1.1-192.168.1.254)
        
        Returns:
            Dict: IPs actives et inactives
        """
        try:
            # Parse la plage
            parts = ip_range.split('-')
            if len(parts) != 2:
                return {"error": "Format invalide"}
            
            start_ip = parts[0].strip()
            end_ip = parts[1].strip()
            
            # Extraction du dernier octet
            start_last = int(start_ip.split('.')[-1])
            end_last = int(end_ip.split('.')[-1])
            base = '.'.join(start_ip.split('.')[:-1])
            
            results = {
                "active": [],
                "inactive": [],
                "total": 0
            }
            
            def ping_ip(ip):
                """Ping une seule IP"""
                try:
                    if platform.system().lower() == 'windows':
                        result = subprocess.run(
                            ['ping', '-n', '1', '-w', '500', ip],
                            capture_output=True,
                            timeout=2
                        )
                    else:
                        result = subprocess.run(
                            ['ping', '-c', '1', '-W', '500', ip],
                            capture_output=True,
                            timeout=2
                        )
                    
                    return (ip, result.returncode == 0)
                except:
                    return (ip, False)
            
            # Scan parallélisé
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = []
                
                for last_octet in range(start_last, end_last + 1):
                    ip = f"{base}.{last_octet}"
                    futures.append(executor.submit(ping_ip, ip))
                    results["total"] += 1
                
                for future in as_completed(futures):
                    ip, is_active = future.result()
                    if is_active:
                        results["active"].append(ip)
                    else:
                        results["inactive"].append(ip)
            
            logger.info(f"IP scan: {len(results['active'])} actives trouvées")
            return results
        
        except Exception as e:
            logger.error(f"Erreur ip_scanner: {str(e)}")
            return {"error": str(e)}
    
    def port_scanner(self, target: str, ports: str = "20-443") -> Dict:
        """
        Scanne les ports ouverts d'une cible
        
        Args:
            target: Adresse IP ou domaine
            ports: Plage de ports (ex: 20-443 ou 22,80,443)
        
        Returns:
            Dict: Ports ouverts et fermés
        """
        try:
            # Résolution du domaine
            try:
                target_ip = socket.gethostbyname(target)
            except:
                target_ip = target
            
            # Parse les ports
            if '-' in ports:
                start, end = ports.split('-')
                port_list = range(int(start), int(end) + 1)
            else:
                port_list = [int(p) for p in ports.split(',')]
            
            results = {
                "target": target,
                "ip": target_ip,
                "open": [],
                "closed": [],
                "filtered": []
            }
            
            def scan_port(port):
                """Scanne un port"""
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((target_ip, port))
                    sock.close()
                    return (port, result == 0)
                except:
                    return (port, False)
            
            # Scan parallélisé
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                futures = [executor.submit(scan_port, port) for port in port_list]
                
                for future in as_completed(futures):
                    port, is_open = future.result()
                    if is_open:
                        results["open"].append(port)
                    else:
                        results["closed"].append(port)
            
            logger.info(f"Port scan {target}: {len(results['open'])} ouverts")
            return results
        
        except Exception as e:
            logger.error(f"Erreur port_scanner: {str(e)}")
            return {"error": str(e)}
    
    def dns_lookup(self, domain: str) -> Dict:
        """
        Résolution DNS d'un domaine
        
        Args:
            domain: Domaine à résoudre
        
        Returns:
            Dict: Résolutions DNS
        """
        try:
            results = {
                "domain": domain,
                "a": [],
                "aaaa": [],
                "mx": [],
                "txt": [],
                "cname": []
            }
            
            # A records
            try:
                results["a"] = socket.gethostbyname_ex(domain)[2]
            except:
                pass
            
            # IPv6
            try:
                results["aaaa"] = socket.getaddrinfo(domain, None, socket.AF_INET6)
            except:
                pass
            
            logger.info(f"DNS lookup: {domain}")
            return results
        
        except Exception as e:
            logger.error(f"Erreur dns_lookup: {str(e)}")
            return {"error": str(e)}
    
    def traceroute(self, target: str, max_hops: int = 30) -> List[Dict]:
        """
        Effectue un traceroute vers une cible
        
        Args:
            target: Adresse IP ou domaine
            max_hops: Nombre max de hops
        
        Returns:
            List[Dict]: Hops trouvés
        """
        try:
            hops = []
            
            if platform.system().lower() == 'windows':
                cmd = ['tracert', '-h', str(max_hops), target]
            else:
                cmd = ['traceroute', '-m', str(max_hops), target]
            
            try:
                result = subprocess.run(cmd, capture_output=True, timeout=30, text=True)
                lines = result.stdout.split('\n')
                
                for line in lines:
                    # Parse les résultats
                    if re.search(r'\d+\s+', line):
                        hops.append({"raw": line.strip()})
            except:
                pass
            
            logger.info(f"Traceroute: {len(hops)} hops trouvés pour {target}")
            return hops
        
        except Exception as e:
            logger.error(f"Erreur traceroute: {str(e)}")
            return []
    
    def whois_lookup(self, domain: str) -> Dict:
        """
        Récupère les informations WHOIS
        
        Args:
            domain: Domaine à rechercher
        
        Returns:
            Dict: Informations WHOIS
        """
        try:
            results = {
                "domain": domain,
                "registrar": None,
                "created": None,
                "expires": None,
                "updated": None,
                "nameservers": []
            }
            
            # Tentative avec socket
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(('whois.iana.org', 43))
                sock.send(f"{domain}\r\n".encode())
                
                response = ""
                while True:
                    data = sock.recv(4096)
                    if not data:
                        break
                    response += data.decode()
                sock.close()
                
                results["raw_response"] = response[:500]
            except:
                pass
            
            logger.info(f"WHOIS lookup: {domain}")
            return results
        
        except Exception as e:
            logger.error(f"Erreur whois_lookup: {str(e)}")
            return {"error": str(e)}
