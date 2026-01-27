"""
Module Réseau - Outils d'analyse réseau légitimes
Sources: 3TH1C4L-MultiTool, Cyb3rtech-Tool, Multi-tools
"""

import socket
import subprocess
import platform
import time
from typing import Optional, List, Dict, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    requests = None


class NetworkTools:
    """Collection d'outils réseau légitimes"""
    
    COMMON_PORTS = {
        21: 'FTP',
        22: 'SSH',
        23: 'Telnet',
        25: 'SMTP',
        53: 'DNS',
        80: 'HTTP',
        110: 'POP3',
        143: 'IMAP',
        443: 'HTTPS',
        445: 'SMB',
        993: 'IMAPS',
        995: 'POP3S',
        3306: 'MySQL',
        3389: 'RDP',
        5432: 'PostgreSQL',
        5900: 'VNC',
        8080: 'HTTP-Proxy',
        8443: 'HTTPS-Alt'
    }
    
    @staticmethod
    def get_my_ip() -> Dict[str, str]:
        """
        Récupère l'adresse IP locale et publique
        
        Returns:
            Dictionnaire avec les IPs
        """
        result = {
            'ip_locale': 'Non disponible',
            'ip_publique': 'Non disponible',
            'hostname': 'Non disponible'
        }
        
        try:
            result['hostname'] = socket.gethostname()
            result['ip_locale'] = socket.gethostbyname(result['hostname'])
        except socket.error:
            pass
        
        if requests:
            try:
                response = requests.get('https://api.ipify.org?format=json', timeout=5)
                if response.status_code == 200:
                    result['ip_publique'] = response.json().get('ip', 'Non disponible')
            except Exception:
                pass
        
        return result
    
    @staticmethod
    def ping_host(host: str, count: int = 4) -> Dict[str, any]:
        """
        Ping un hôte
        
        Args:
            host: Hôte à ping
            count: Nombre de paquets
            
        Returns:
            Résultats du ping
        """
        result = {
            'host': host,
            'accessible': False,
            'temps_moyen': None,
            'paquets_perdus': 100,
            'details': ''
        }
        
        count = min(count, 10)
        
        try:
            is_windows = platform.system().lower() == 'windows'
            param = '-n' if is_windows else '-c'
            
            cmd = ['ping', param, str(count), host]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            result['details'] = process.stdout
            
            if process.returncode == 0:
                result['accessible'] = True
                
                if is_windows:
                    for line in process.stdout.split('\n'):
                        if 'Moyenne' in line or 'Average' in line:
                            parts = line.split('=')
                            if len(parts) >= 2:
                                try:
                                    result['temps_moyen'] = parts[-1].strip().replace('ms', '')
                                except Exception:
                                    pass
                else:
                    for line in process.stdout.split('\n'):
                        if 'avg' in line or 'moyenne' in line.lower():
                            parts = line.split('/')
                            if len(parts) >= 5:
                                try:
                                    result['temps_moyen'] = parts[4]
                                except Exception:
                                    pass
                                    
        except subprocess.TimeoutExpired:
            result['details'] = "Timeout - L'hôte n'a pas répondu"
        except Exception as e:
            result['details'] = f"Erreur: {str(e)}"
        
        return result
    
    @staticmethod
    def scan_port(host: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
        """
        Scanne un port unique
        
        Args:
            host: Hôte cible
            port: Port à scanner
            timeout: Timeout en secondes
            
        Returns:
            Tuple (port, ouvert, service)
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            
            is_open = result == 0
            service = NetworkTools.COMMON_PORTS.get(port, 'Inconnu')
            
            return port, is_open, service
        except Exception:
            return port, False, 'Erreur'
    
    @staticmethod
    def scan_ports(
        host: str,
        start_port: int = 1,
        end_port: int = 1024,
        timeout: float = 0.5,
        max_workers: int = 50
    ) -> List[Dict]:
        """
        Scanne une plage de ports
        
        Args:
            host: Hôte cible
            start_port: Port de début
            end_port: Port de fin
            timeout: Timeout par port
            max_workers: Threads maximum
            
        Returns:
            Liste des ports ouverts
        """
        open_ports = []
        
        start_port = max(1, min(start_port, 65535))
        end_port = max(1, min(end_port, 65535))
        max_workers = min(max_workers, 100)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(NetworkTools.scan_port, host, port, timeout): port
                for port in range(start_port, end_port + 1)
            }
            
            for future in as_completed(futures):
                try:
                    port, is_open, service = future.result()
                    if is_open:
                        open_ports.append({
                            'port': port,
                            'service': service,
                            'etat': 'Ouvert'
                        })
                except Exception:
                    pass
        
        return sorted(open_ports, key=lambda x: x['port'])
    
    @staticmethod
    def dns_lookup(domain: str) -> Dict[str, any]:
        """
        Effectue une recherche DNS
        
        Args:
            domain: Domaine à rechercher
            
        Returns:
            Informations DNS
        """
        result = {
            'domaine': domain,
            'adresses_ip': [],
            'adresses_ipv6': [],
            'mx_records': [],
            'cname': None,
            'erreur': None
        }
        
        try:
            ips = socket.gethostbyname_ex(domain)
            result['adresses_ip'] = list(set(ips[2]))
        except socket.gaierror as e:
            result['erreur'] = str(e)
        
        try:
            import dns.resolver
            
            try:
                mx_records = dns.resolver.resolve(domain, 'MX')
                result['mx_records'] = [str(r.exchange) for r in mx_records]
            except Exception:
                pass
            
            try:
                aaaa_records = dns.resolver.resolve(domain, 'AAAA')
                result['adresses_ipv6'] = [str(r) for r in aaaa_records]
            except Exception:
                pass
                
        except ImportError:
            pass
        
        return result
    
    @staticmethod
    def whois_lookup(domain: str) -> Dict[str, any]:
        """
        Effectue une recherche WHOIS
        
        Args:
            domain: Domaine à rechercher
            
        Returns:
            Informations WHOIS
        """
        result = {
            'domaine': domain,
            'registrar': None,
            'creation_date': None,
            'expiration_date': None,
            'name_servers': [],
            'status': None,
            'erreur': None
        }
        
        try:
            import whois
            
            w = whois.whois(domain)
            
            result['registrar'] = w.registrar
            result['creation_date'] = str(w.creation_date) if w.creation_date else None
            result['expiration_date'] = str(w.expiration_date) if w.expiration_date else None
            result['name_servers'] = w.name_servers if isinstance(w.name_servers, list) else [w.name_servers] if w.name_servers else []
            result['status'] = w.status if isinstance(w.status, list) else [w.status] if w.status else []
            
        except ImportError:
            result['erreur'] = "Module whois non installé"
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def get_ip_info(ip: str) -> Dict[str, any]:
        """
        Récupère les informations géographiques d'une IP
        
        Args:
            ip: Adresse IP
            
        Returns:
            Informations géographiques
        """
        result = {
            'ip': ip,
            'pays': None,
            'region': None,
            'ville': None,
            'fournisseur': None,
            'organisation': None,
            'latitude': None,
            'longitude': None,
            'erreur': None
        }
        
        if not requests:
            result['erreur'] = "Module requests non installé"
            return result
        
        try:
            response = requests.get(f'http://ip-api.com/json/{ip}', timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('status') == 'success':
                    result['pays'] = data.get('country')
                    result['region'] = data.get('regionName')
                    result['ville'] = data.get('city')
                    result['fournisseur'] = data.get('isp')
                    result['organisation'] = data.get('org')
                    result['latitude'] = data.get('lat')
                    result['longitude'] = data.get('lon')
                else:
                    result['erreur'] = data.get('message', 'IP invalide ou privée')
                    
        except requests.exceptions.Timeout:
            result['erreur'] = "Timeout lors de la requête"
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def check_website_status(url: str) -> Dict[str, any]:
        """
        Vérifie le statut d'un site web
        
        Args:
            url: URL à vérifier
            
        Returns:
            Informations sur le statut
        """
        result = {
            'url': url,
            'accessible': False,
            'code_status': None,
            'temps_reponse': None,
            'serveur': None,
            'content_type': None,
            'erreur': None
        }
        
        if not requests:
            result['erreur'] = "Module requests non installé"
            return result
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            start_time = time.time()
            response = requests.get(
                url,
                timeout=10,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; MultiTool/1.0)'},
                allow_redirects=True
            )
            end_time = time.time()
            
            result['accessible'] = True
            result['code_status'] = response.status_code
            result['temps_reponse'] = round((end_time - start_time) * 1000, 2)
            result['serveur'] = response.headers.get('Server')
            result['content_type'] = response.headers.get('Content-Type')
            
        except requests.exceptions.Timeout:
            result['erreur'] = "Timeout - Le site n'a pas répondu"
        except requests.exceptions.ConnectionError:
            result['erreur'] = "Erreur de connexion - Site inaccessible"
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def traceroute(host: str, max_hops: int = 30) -> List[Dict]:
        """
        Effectue un traceroute
        
        Args:
            host: Hôte cible
            max_hops: Nombre maximum de sauts
            
        Returns:
            Liste des sauts
        """
        hops = []
        max_hops = min(max_hops, 30)
        
        try:
            is_windows = platform.system().lower() == 'windows'
            
            if is_windows:
                cmd = ['tracert', '-h', str(max_hops), host]
            else:
                cmd = ['traceroute', '-m', str(max_hops), host]
            
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            lines = process.stdout.strip().split('\n')
            
            for line in lines[1:]:
                if line.strip():
                    hops.append({
                        'raw': line.strip()
                    })
                    
        except subprocess.TimeoutExpired:
            hops.append({'raw': 'Timeout - Traceroute incomplet'})
        except FileNotFoundError:
            hops.append({'raw': 'Commande traceroute non disponible'})
        except Exception as e:
            hops.append({'raw': f'Erreur: {str(e)}'})
        
        return hops
