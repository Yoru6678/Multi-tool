#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module des outils réseau - Sécurisé et compatible Windows
"""

import socket
import requests
import subprocess
import platform
import logging
from pathlib import Path
from typing import Optional, List, Tuple

from utils.security import SecurityManager
from utils.ui import UI
from utils.logger import log_action

logger = logging.getLogger(__name__)


class NetworkTools:
    """Outils réseau sécurisés"""
    
    def __init__(self):
        """Initialisation des outils réseau"""
        self.security = SecurityManager()
        self.ui = UI()
        self.timeout = 5
    
    def show_my_ip(self):
        """Affiche l'adresse IP publique de l'utilisateur"""
        try:
            self.ui.print_header("MON ADRESSE IP PUBLIQUE")
            self.ui.show_loading("Récupération de votre IP", 1.0)
            
            # Utilisation de plusieurs services pour fiabilité
            services = [
                'https://api.ipify.org?format=json',
                'https://api.myip.com',
                'https://ipinfo.io/json'
            ]
            
            ip_address = None
            for service in services:
                try:
                    response = requests.get(service, timeout=self.timeout)
                    if response.status_code == 200:
                        data = response.json()
                        ip_address = data.get('ip') or data.get('ipAddress')
                        if ip_address:
                            break
                except Exception as e:
                    logger.warning(f"Service {service} échoué: {str(e)}")
                    continue
            
            if ip_address:
                # Validation de l'IP
                is_valid, error = self.security.validate_input(ip_address, 'ip')
                if is_valid:
                    self.ui.print_success(f"Votre adresse IP publique: {ip_address}")
                    log_action(logger, "Récupération IP publique", {"ip": ip_address})
                else:
                    self.ui.print_error(f"IP invalide reçue: {error}")
            else:
                self.ui.print_error("Impossible de récupérer votre IP publique")
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur show_my_ip: {str(e)}", exc_info=True)
    
    def ip_scanner(self):
        """Scanne une plage d'adresses IP"""
        try:
            self.ui.print_header("SCANNER IP")
            self.ui.print_warning("⚠️  Scannez uniquement des réseaux dont vous avez l'autorisation!")
            
            # Demande de la plage IP
            ip_range = self.ui.get_input("Plage IP (ex: 192.168.1.1-192.168.1.10)")
            
            # Validation de base
            if '-' not in ip_range:
                self.ui.print_error("Format invalide. Utilisez: IP_START-IP_END")
                return
            
            start_ip, end_ip = ip_range.split('-')
            start_ip = start_ip.strip()
            end_ip = end_ip.strip()
            
            # Validation des IPs
            is_valid_start, error_start = self.security.validate_input(start_ip, 'ip')
            is_valid_end, error_end = self.security.validate_input(end_ip, 'ip')
            
            if not is_valid_start:
                self.ui.print_error(f"IP de départ invalide: {error_start}")
                return
            
            if not is_valid_end:
                self.ui.print_error(f"IP de fin invalide: {error_end}")
                return
            
            # Extraction des octets
            start_parts = list(map(int, start_ip.split('.')))
            end_parts = list(map(int, end_ip.split('.')))
            
            # Vérification de la plage
            if start_parts[3] > end_parts[3]:
                self.ui.print_error("La plage est invalide (début > fin)")
                return
            
            # Limitation de la plage pour éviter les abus
            range_size = end_parts[3] - start_parts[3] + 1
            if range_size > 255:
                self.ui.print_error("Plage trop grande (maximum 255 IPs)")
                return
            
            self.ui.print_info(f"Scan de {range_size} adresses IP...")
            
            # Scan
            active_hosts = []
            base_ip = '.'.join(map(str, start_parts[:3]))
            
            for i in range(start_parts[3], end_parts[3] + 1):
                ip = f"{base_ip}.{i}"
                self.ui.show_progress(i - start_parts[3] + 1, range_size, "Scan en cours")
                
                try:
                    # Ping simple (compatible Windows)
                    param = '-n' if platform.system().lower() == 'windows' else '-c'
                    command = ['ping', param, '1', '-w', '1000', ip]
                    result = subprocess.run(
                        command,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        timeout=2
                    )
                    
                    if result.returncode == 0:
                        active_hosts.append(ip)
                        self.ui.print_success(f"✓ {ip} - ACTIF")
                
                except subprocess.TimeoutExpired:
                    pass
                except Exception as e:
                    logger.warning(f"Erreur scan {ip}: {str(e)}")
            
            # Résultats
            print()
            self.ui.print_separator()
            self.ui.print_info(f"Scan terminé: {len(active_hosts)}/{range_size} hôtes actifs")
            
            if active_hosts:
                self.ui.print_success("Hôtes actifs:")
                for host in active_hosts:
                    print(f"  • {host}")
            
            log_action(logger, "Scan IP", {
                "range": ip_range,
                "active_hosts": len(active_hosts)
            })
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur ip_scanner: {str(e)}", exc_info=True)
    
    def ip_pinger(self):
        """Ping une adresse IP"""
        try:
            self.ui.print_header("PING IP")
            
            # Demande de l'IP
            ip = self.ui.get_input("Adresse IP ou domaine à pinger")
            
            # Validation
            is_valid_ip, _ = self.security.validate_input(ip, 'ip')
            is_valid_domain, _ = self.security.validate_input(ip, 'domain')
            
            if not (is_valid_ip or is_valid_domain):
                self.ui.print_error("Adresse IP ou domaine invalide")
                return
            
            # Nombre de pings
            count_str = self.ui.get_input("Nombre de pings (1-100, défaut: 4)")
            try:
                count = int(count_str) if count_str else 4
                count = max(1, min(100, count))
            except ValueError:
                count = 4
            
            self.ui.print_info(f"Ping de {ip} ({count} fois)...")
            
            # Commande ping selon l'OS
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, str(count), ip]
            
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=count * 2
                )
                
                print()
                print(result.stdout)
                
                if result.returncode == 0:
                    self.ui.print_success("Ping réussi")
                else:
                    self.ui.print_error("Ping échoué")
                
                log_action(logger, "Ping IP", {"target": ip, "count": count})
            
            except subprocess.TimeoutExpired:
                self.ui.print_error("Timeout dépassé")
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur ip_pinger: {str(e)}", exc_info=True)
    
    def port_scanner(self):
        """Scanne les ports d'une adresse IP"""
        try:
            self.ui.print_header("SCANNER DE PORTS")
            self.ui.print_warning("⚠️  Scannez uniquement des systèmes dont vous avez l'autorisation!")
            
            # Demande de l'IP
            ip = self.ui.get_input("Adresse IP à scanner")
            
            # Validation
            is_valid, error = self.security.validate_input(ip, 'ip')
            if not is_valid:
                self.ui.print_error(f"IP invalide: {error}")
                return
            
            # Demande de la plage de ports
            port_range = self.ui.get_input("Plage de ports (ex: 1-1000, défaut: 1-1024)")
            
            if not port_range:
                start_port, end_port = 1, 1024
            else:
                try:
                    if '-' in port_range:
                        start_port, end_port = map(int, port_range.split('-'))
                    else:
                        start_port = end_port = int(port_range)
                except ValueError:
                    self.ui.print_error("Format de ports invalide")
                    return
            
            # Validation des ports
            if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535):
                self.ui.print_error("Ports invalides (1-65535)")
                return
            
            if start_port > end_port:
                self.ui.print_error("Port de départ > port de fin")
                return
            
            # Limitation pour éviter les abus
            port_count = end_port - start_port + 1
            if port_count > 10000:
                self.ui.print_error("Plage trop grande (maximum 10000 ports)")
                return
            
            self.ui.print_info(f"Scan de {port_count} ports sur {ip}...")
            
            # Scan
            open_ports = []
            for port in range(start_port, end_port + 1):
                self.ui.show_progress(port - start_port + 1, port_count, "Scan en cours")
                
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    
                    if result == 0:
                        open_ports.append(port)
                        # Tentative d'identification du service
                        try:
                            service = socket.getservbyport(port)
                        except:
                            service = "inconnu"
                        self.ui.print_success(f"✓ Port {port} OUVERT ({service})")
                
                except Exception as e:
                    logger.debug(f"Erreur scan port {port}: {str(e)}")
            
            # Résultats
            print()
            self.ui.print_separator()
            self.ui.print_info(f"Scan terminé: {len(open_ports)}/{port_count} ports ouverts")
            
            if open_ports:
                self.ui.print_success("Ports ouverts:")
                for port in open_ports:
                    try:
                        service = socket.getservbyport(port)
                    except:
                        service = "inconnu"
                    print(f"  • {port} ({service})")
            
            log_action(logger, "Scan de ports", {
                "target": ip,
                "range": f"{start_port}-{end_port}",
                "open_ports": len(open_ports)
            })
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur port_scanner: {str(e)}", exc_info=True)
    
    def website_info(self):
        """Récupère des informations sur un site web"""
        try:
            self.ui.print_header("INFORMATIONS SUR UN SITE WEB")
            
            # Demande de l'URL
            url = self.ui.get_input("URL du site (avec http:// ou https://)")
            
            # Validation
            is_valid, error = self.security.validate_input(url, 'url')
            if not is_valid:
                self.ui.print_error(f"URL invalide: {error}")
                return
            
            self.ui.show_loading("Récupération des informations", 1.0)
            
            try:
                # Requête HTTP
                response = requests.get(url, timeout=self.timeout, allow_redirects=True)
                
                # Affichage des informations
                self.ui.display_box("INFORMATIONS DU SITE", [
                    f"URL: {url}",
                    f"Code de statut: {response.status_code}",
                    f"Taille: {len(response.content)} octets",
                    f"Encodage: {response.encoding}",
                    f"Type de contenu: {response.headers.get('Content-Type', 'N/A')}",
                    f"Serveur: {response.headers.get('Server', 'N/A')}",
                    f"Redirections: {len(response.history)}"
                ])
                
                # Headers de sécurité
                security_headers = {
                    'Strict-Transport-Security': 'HSTS',
                    'X-Frame-Options': 'Clickjacking Protection',
                    'X-Content-Type-Options': 'MIME Sniffing Protection',
                    'Content-Security-Policy': 'CSP',
                    'X-XSS-Protection': 'XSS Protection'
                }
                
                print()
                self.ui.print_info("Headers de sécurité:")
                for header, description in security_headers.items():
                    if header in response.headers:
                        self.ui.print_success(f"✓ {description}: {response.headers[header][:50]}")
                    else:
                        self.ui.print_warning(f"✗ {description}: Non présent")
                
                log_action(logger, "Info site web", {"url": url, "status": response.status_code})
            
            except requests.exceptions.Timeout:
                self.ui.print_error("Timeout: Le site ne répond pas")
            except requests.exceptions.ConnectionError:
                self.ui.print_error("Erreur de connexion au site")
            except requests.exceptions.RequestException as e:
                self.ui.print_error(f"Erreur de requête: {str(e)}")
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur website_info: {str(e)}", exc_info=True)
    
    def dns_lookup(self):
        """Effectue une résolution DNS"""
        try:
            self.ui.print_header("LOOKUP DNS")
            
            # Demande du domaine
            domain = self.ui.get_input("Nom de domaine")
            
            # Validation
            is_valid, error = self.security.validate_input(domain, 'domain')
            if not is_valid:
                self.ui.print_error(f"Domaine invalide: {error}")
                return
            
            self.ui.show_loading("Résolution DNS", 1.0)
            
            try:
                # Résolution DNS
                ip_address = socket.gethostbyname(domain)
                
                self.ui.print_success(f"Adresse IP: {ip_address}")
                
                # Résolution inverse
                try:
                    hostname = socket.gethostbyaddr(ip_address)[0]
                    self.ui.print_info(f"Hostname: {hostname}")
                except:
                    self.ui.print_warning("Résolution inverse impossible")
                
                log_action(logger, "DNS Lookup", {"domain": domain, "ip": ip_address})
            
            except socket.gaierror:
                self.ui.print_error("Impossible de résoudre le domaine")
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur dns_lookup: {str(e)}", exc_info=True)
    
    def traceroute(self):
        """Effectue un traceroute"""
        try:
            self.ui.print_header("TRACEROUTE")
            
            # Demande de la cible
            target = self.ui.get_input("Adresse IP ou domaine")
            
            # Validation
            is_valid_ip, _ = self.security.validate_input(target, 'ip')
            is_valid_domain, _ = self.security.validate_input(target, 'domain')
            
            if not (is_valid_ip or is_valid_domain):
                self.ui.print_error("Adresse IP ou domaine invalide")
                return
            
            self.ui.print_info(f"Traceroute vers {target}...")
            
            # Commande selon l'OS
            if platform.system().lower() == 'windows':
                command = ['tracert', target]
            else:
                command = ['traceroute', target]
            
            try:
                result = subprocess.run(
                    command,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=60
                )
                
                print()
                print(result.stdout)
                
                log_action(logger, "Traceroute", {"target": target})
            
            except subprocess.TimeoutExpired:
                self.ui.print_error("Timeout dépassé")
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur traceroute: {str(e)}", exc_info=True)
    
    def whois_lookup(self):
        """Effectue une recherche WHOIS"""
        try:
            self.ui.print_header("WHOIS LOOKUP")
            
            # Demande du domaine
            domain = self.ui.get_input("Nom de domaine")
            
            # Validation
            is_valid, error = self.security.validate_input(domain, 'domain')
            if not is_valid:
                self.ui.print_error(f"Domaine invalide: {error}")
                return
            
            self.ui.show_loading("Recherche WHOIS", 1.0)
            
            try:
                import whois
                
                # Recherche WHOIS
                w = whois.whois(domain)
                
                # Affichage des informations
                info = [
                    f"Domaine: {w.domain_name}",
                    f"Registrar: {w.registrar}",
                    f"Date de création: {w.creation_date}",
                    f"Date d'expiration: {w.expiration_date}",
                    f"Serveurs DNS: {', '.join(w.name_servers) if w.name_servers else 'N/A'}",
                    f"Statut: {w.status}"
                ]
                
                self.ui.display_box("INFORMATIONS WHOIS", info)
                
                log_action(logger, "WHOIS Lookup", {"domain": domain})
            
            except ImportError:
                self.ui.print_error("Module 'python-whois' non installé")
                self.ui.print_info("Installez-le avec: pip install python-whois")
            except Exception as e:
                self.ui.print_error(f"Erreur WHOIS: {str(e)}")
        
        except Exception as e:
            self.ui.print_error(f"Erreur: {str(e)}")
            logger.error(f"Erreur whois_lookup: {str(e)}", exc_info=True)
