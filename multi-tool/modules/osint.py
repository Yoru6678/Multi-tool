"""
Module OSINT - Outils de renseignement open source légitimes
Sources: 3TH1C4L-MultiTool, Cyb3rtech-Tool, Sherlock, ReconXplorer
"""

import re
import json
from typing import Optional, List, Dict
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import requests
except ImportError:
    requests = None


class OSINTTools:
    """Collection d'outils OSINT légitimes"""
    
    SOCIAL_PLATFORMS = {
        'github': 'https://api.github.com/users/{}',
        'twitter': 'https://twitter.com/{}',
        'instagram': 'https://www.instagram.com/{}/',
        'reddit': 'https://www.reddit.com/user/{}/about.json',
        'tiktok': 'https://www.tiktok.com/@{}',
        'pinterest': 'https://www.pinterest.com/{}/',
        'linkedin': 'https://www.linkedin.com/in/{}/',
        'youtube': 'https://www.youtube.com/@{}',
        'twitch': 'https://www.twitch.tv/{}',
        'medium': 'https://medium.com/@{}',
        'dev.to': 'https://dev.to/{}',
        'gitlab': 'https://gitlab.com/{}',
        'steam': 'https://steamcommunity.com/id/{}',
    }
    
    @staticmethod
    def search_username(username: str, timeout: int = 10) -> List[Dict]:
        """
        Recherche un nom d'utilisateur sur plusieurs plateformes
        
        Args:
            username: Nom d'utilisateur à rechercher
            timeout: Timeout par requête
            
        Returns:
            Liste des plateformes où le profil existe
        """
        results = []
        
        if not requests:
            return [{'erreur': 'Module requests non installé'}]
        
        username = re.sub(r'[^a-zA-Z0-9_.-]', '', username)
        if not username:
            return [{'erreur': 'Nom d\'utilisateur invalide'}]
        
        def check_platform(platform: str, url_template: str) -> Optional[Dict]:
            url = url_template.format(username)
            try:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=False)
                
                if response.status_code == 200:
                    return {
                        'plateforme': platform,
                        'url': url,
                        'statut': 'Trouvé',
                        'code': response.status_code
                    }
                elif response.status_code in [301, 302]:
                    return {
                        'plateforme': platform,
                        'url': url,
                        'statut': 'Possible (redirection)',
                        'code': response.status_code
                    }
            except requests.exceptions.Timeout:
                return {
                    'plateforme': platform,
                    'url': url,
                    'statut': 'Timeout',
                    'code': None
                }
            except Exception:
                pass
            
            return None
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(check_platform, platform, url): platform
                for platform, url in OSINTTools.SOCIAL_PLATFORMS.items()
            }
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)
        
        return sorted(results, key=lambda x: x['plateforme'])
    
    @staticmethod
    def get_github_info(username: str) -> Dict:
        """
        Récupère les informations GitHub d'un utilisateur
        
        Args:
            username: Nom d'utilisateur GitHub
            
        Returns:
            Informations du profil
        """
        result = {
            'username': username,
            'nom': None,
            'bio': None,
            'entreprise': None,
            'localisation': None,
            'blog': None,
            'repos_publics': None,
            'followers': None,
            'following': None,
            'date_creation': None,
            'avatar_url': None,
            'erreur': None
        }
        
        if not requests:
            result['erreur'] = "Module requests non installé"
            return result
        
        try:
            response = requests.get(
                f'https://api.github.com/users/{username}',
                timeout=10,
                headers={'Accept': 'application/vnd.github.v3+json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                result['nom'] = data.get('name')
                result['bio'] = data.get('bio')
                result['entreprise'] = data.get('company')
                result['localisation'] = data.get('location')
                result['blog'] = data.get('blog')
                result['repos_publics'] = data.get('public_repos')
                result['followers'] = data.get('followers')
                result['following'] = data.get('following')
                result['date_creation'] = data.get('created_at')
                result['avatar_url'] = data.get('avatar_url')
            elif response.status_code == 404:
                result['erreur'] = "Utilisateur non trouvé"
            else:
                result['erreur'] = f"Erreur HTTP {response.status_code}"
                
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def analyze_email(email: str) -> Dict:
        """
        Analyse une adresse email (format et domaine)
        
        Args:
            email: Adresse email à analyser
            
        Returns:
            Informations sur l'email
        """
        result = {
            'email': email,
            'valide': False,
            'nom_utilisateur': None,
            'domaine': None,
            'fournisseur_commun': False,
            'mx_records': [],
            'erreur': None
        }
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            result['erreur'] = "Format d'email invalide"
            return result
        
        result['valide'] = True
        parts = email.split('@')
        result['nom_utilisateur'] = parts[0]
        result['domaine'] = parts[1]
        
        common_providers = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com',
            'live.com', 'icloud.com', 'protonmail.com', 'aol.com',
            'mail.com', 'gmx.com', 'yandex.com', 'zoho.com'
        ]
        
        result['fournisseur_commun'] = result['domaine'].lower() in common_providers
        
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(result['domaine'], 'MX')
            result['mx_records'] = [str(r.exchange) for r in mx_records]
        except ImportError:
            pass
        except Exception:
            pass
        
        return result
    
    @staticmethod
    def analyze_phone(phone: str) -> Dict:
        """
        Analyse un numéro de téléphone
        
        Args:
            phone: Numéro de téléphone
            
        Returns:
            Informations sur le numéro
        """
        result = {
            'numero': phone,
            'format_valide': False,
            'pays': None,
            'operateur': None,
            'type': None,
            'international': None,
            'national': None,
            'erreur': None
        }
        
        try:
            import phonenumbers
            from phonenumbers import carrier, geocoder, timezone
            
            if not phone.startswith('+'):
                phone = '+' + phone.lstrip('0')
            
            parsed = phonenumbers.parse(phone, None)
            
            result['format_valide'] = phonenumbers.is_valid_number(parsed)
            result['pays'] = geocoder.country_name_for_number(parsed, 'fr')
            result['operateur'] = carrier.name_for_number(parsed, 'fr')
            result['type'] = 'Mobile' if phonenumbers.number_type(parsed) == phonenumbers.PhoneNumberType.MOBILE else 'Fixe'
            result['international'] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            result['national'] = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            
        except ImportError:
            result['erreur'] = "Module phonenumbers non installé"
        except Exception as e:
            result['erreur'] = f"Numéro invalide: {str(e)}"
        
        return result
    
    @staticmethod
    def search_breach_database(email: str) -> Dict:
        """
        Vérifie si un email a été compromis (via API publiques)
        
        Args:
            email: Email à vérifier
            
        Returns:
            Informations sur les brèches
        """
        result = {
            'email': email,
            'compromis': False,
            'breches': [],
            'erreur': None
        }
        
        if not requests:
            result['erreur'] = "Module requests non installé"
            return result
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            result['erreur'] = "Format d'email invalide"
            return result
        
        result['erreur'] = "Utilisez https://haveibeenpwned.com pour vérifier manuellement"
        
        return result
    
    @staticmethod
    def get_website_info(url: str) -> Dict:
        """
        Récupère les informations d'un site web
        
        Args:
            url: URL du site
            
        Returns:
            Informations sur le site
        """
        result = {
            'url': url,
            'titre': None,
            'description': None,
            'technologies': [],
            'headers': {},
            'serveur': None,
            'powered_by': None,
            'erreur': None
        }
        
        if not requests:
            result['erreur'] = "Module requests non installé"
            return result
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            response = requests.get(
                url,
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0 (compatible; MultiTool/1.0)'}
            )
            
            headers = dict(response.headers)
            result['headers'] = {k: v for k, v in headers.items() if k.lower() in [
                'server', 'x-powered-by', 'content-type', 'x-frame-options',
                'content-security-policy', 'strict-transport-security'
            ]}
            
            result['serveur'] = headers.get('Server')
            result['powered_by'] = headers.get('X-Powered-By')
            
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                title_tag = soup.find('title')
                result['titre'] = title_tag.text.strip() if title_tag else None
                
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                result['description'] = meta_desc.get('content') if meta_desc else None
                
                techs = []
                if 'wp-content' in response.text:
                    techs.append('WordPress')
                if 'Joomla' in response.text:
                    techs.append('Joomla')
                if 'drupal' in response.text.lower():
                    techs.append('Drupal')
                if 'react' in response.text.lower():
                    techs.append('React')
                if 'vue' in response.text.lower():
                    techs.append('Vue.js')
                if 'angular' in response.text.lower():
                    techs.append('Angular')
                if 'jquery' in response.text.lower():
                    techs.append('jQuery')
                if 'bootstrap' in response.text.lower():
                    techs.append('Bootstrap')
                
                result['technologies'] = techs
                
            except ImportError:
                result['erreur'] = "BeautifulSoup non installé pour l'analyse complète"
                
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def reverse_image_urls(image_url: str) -> Dict:
        """
        Génère des URLs pour la recherche d'image inversée
        
        Args:
            image_url: URL de l'image
            
        Returns:
            URLs de recherche
        """
        from urllib.parse import quote
        
        encoded_url = quote(image_url, safe='')
        
        return {
            'image_url': image_url,
            'google_images': f'https://lens.google.com/uploadbyurl?url={encoded_url}',
            'tineye': f'https://tineye.com/search?url={encoded_url}',
            'yandex': f'https://yandex.com/images/search?rpt=imageview&url={encoded_url}',
            'bing': f'https://www.bing.com/images/search?view=detailv2&iss=sbi&q=imgurl:{encoded_url}'
        }
