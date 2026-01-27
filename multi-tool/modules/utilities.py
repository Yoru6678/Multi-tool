"""
Module Utilitaires - Outils divers
Sources: Multi-tools, Butcher-Tools, 3TH1C4L-MultiTool
"""

import os
import sys
import json
import time
import platform
import subprocess
from typing import Optional, Dict, List
from pathlib import Path
from datetime import datetime


class UtilityTools:
    """Collection d'outils utilitaires"""
    
    @staticmethod
    def get_system_info() -> Dict:
        """
        Récupère les informations système
        
        Returns:
            Informations système détaillées
        """
        info = {
            'systeme': platform.system(),
            'version': platform.version(),
            'architecture': platform.machine(),
            'processeur': platform.processor(),
            'python_version': sys.version,
            'hostname': platform.node(),
            'utilisateur': os.environ.get('USER') or os.environ.get('USERNAME'),
            'repertoire_courant': str(Path.cwd()),
            'repertoire_home': str(Path.home()),
            'date_heure': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if platform.system() == 'Windows':
            info['edition'] = platform.win32_edition() if hasattr(platform, 'win32_edition') else 'N/A'
        
        return info
    
    @staticmethod
    def list_directory(path: str = '.', hidden: bool = False) -> Dict:
        """
        Liste le contenu d'un répertoire
        
        Args:
            path: Chemin du répertoire
            hidden: Inclure les fichiers cachés
            
        Returns:
            Contenu du répertoire
        """
        result = {
            'chemin': path,
            'fichiers': [],
            'dossiers': [],
            'erreur': None
        }
        
        try:
            dir_path = Path(path).resolve()
            
            if not dir_path.exists():
                result['erreur'] = "Chemin inexistant"
                return result
            
            if not dir_path.is_dir():
                result['erreur'] = "Le chemin n'est pas un répertoire"
                return result
            
            for item in dir_path.iterdir():
                if not hidden and item.name.startswith('.'):
                    continue
                
                item_info = {
                    'nom': item.name,
                    'taille': item.stat().st_size if item.is_file() else None,
                    'modifie': datetime.fromtimestamp(item.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                }
                
                if item.is_file():
                    result['fichiers'].append(item_info)
                elif item.is_dir():
                    result['dossiers'].append(item_info)
                    
        except PermissionError:
            result['erreur'] = "Permission refusée"
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def file_info(file_path: str) -> Dict:
        """
        Récupère les informations d'un fichier
        
        Args:
            file_path: Chemin du fichier
            
        Returns:
            Informations du fichier
        """
        result = {
            'chemin': file_path,
            'existe': False,
            'nom': None,
            'extension': None,
            'taille': None,
            'taille_lisible': None,
            'cree': None,
            'modifie': None,
            'accede': None,
            'est_fichier': False,
            'est_dossier': False,
            'permissions': None,
            'erreur': None
        }
        
        try:
            path = Path(file_path)
            
            if not path.exists():
                result['erreur'] = "Fichier inexistant"
                return result
            
            stat = path.stat()
            
            result['existe'] = True
            result['nom'] = path.name
            result['extension'] = path.suffix
            result['taille'] = stat.st_size
            result['taille_lisible'] = UtilityTools._format_size(stat.st_size)
            result['cree'] = datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
            result['modifie'] = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
            result['accede'] = datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')
            result['est_fichier'] = path.is_file()
            result['est_dossier'] = path.is_dir()
            result['permissions'] = oct(stat.st_mode)[-3:]
            
        except PermissionError:
            result['erreur'] = "Permission refusée"
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Formate une taille en bytes de manière lisible"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
    
    @staticmethod
    def convert_timestamp(timestamp: float) -> str:
        """Convertit un timestamp en date lisible"""
        try:
            return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        except Exception:
            return "Timestamp invalide"
    
    @staticmethod
    def date_to_timestamp(date_str: str, format: str = '%Y-%m-%d') -> Optional[float]:
        """Convertit une date en timestamp"""
        try:
            dt = datetime.strptime(date_str, format)
            return dt.timestamp()
        except Exception:
            return None
    
    @staticmethod
    def json_prettify(json_str: str) -> Optional[str]:
        """
        Formate du JSON de manière lisible
        
        Args:
            json_str: Chaîne JSON
            
        Returns:
            JSON formaté ou None si invalide
        """
        try:
            parsed = json.loads(json_str)
            return json.dumps(parsed, indent=2, ensure_ascii=False)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def json_minify(json_str: str) -> Optional[str]:
        """
        Minifie du JSON
        
        Args:
            json_str: Chaîne JSON
            
        Returns:
            JSON minifié ou None si invalide
        """
        try:
            parsed = json.loads(json_str)
            return json.dumps(parsed, separators=(',', ':'), ensure_ascii=False)
        except json.JSONDecodeError:
            return None
    
    @staticmethod
    def text_stats(text: str) -> Dict:
        """
        Calcule les statistiques d'un texte
        
        Args:
            text: Texte à analyser
            
        Returns:
            Statistiques du texte
        """
        words = text.split()
        lines = text.split('\n')
        
        return {
            'caracteres': len(text),
            'caracteres_sans_espaces': len(text.replace(' ', '').replace('\n', '')),
            'mots': len(words),
            'lignes': len(lines),
            'paragraphes': len([p for p in text.split('\n\n') if p.strip()]),
            'mot_le_plus_long': max(words, key=len) if words else '',
            'longueur_moyenne_mot': sum(len(w) for w in words) / len(words) if words else 0
        }
    
    @staticmethod
    def color_converter(color: str) -> Dict:
        """
        Convertit une couleur entre différents formats
        
        Args:
            color: Couleur en HEX (#RRGGBB) ou RGB (r,g,b)
            
        Returns:
            Couleur dans différents formats
        """
        result = {
            'input': color,
            'hex': None,
            'rgb': None,
            'hsl': None,
            'erreur': None
        }
        
        try:
            if color.startswith('#'):
                hex_color = color.lstrip('#')
                if len(hex_color) == 3:
                    hex_color = ''.join(c*2 for c in hex_color)
                
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
            elif ',' in color:
                parts = [int(p.strip()) for p in color.split(',')]
                r, g, b = parts[0], parts[1], parts[2]
                hex_color = f'{r:02x}{g:02x}{b:02x}'
            else:
                result['erreur'] = "Format non reconnu"
                return result
            
            result['hex'] = f'#{hex_color.upper()}'
            result['rgb'] = f'rgb({r}, {g}, {b})'
            
            r_norm, g_norm, b_norm = r/255, g/255, b/255
            max_c = max(r_norm, g_norm, b_norm)
            min_c = min(r_norm, g_norm, b_norm)
            l = (max_c + min_c) / 2
            
            if max_c == min_c:
                h = s = 0
            else:
                d = max_c - min_c
                s = d / (2 - max_c - min_c) if l > 0.5 else d / (max_c + min_c)
                if max_c == r_norm:
                    h = (g_norm - b_norm) / d + (6 if g_norm < b_norm else 0)
                elif max_c == g_norm:
                    h = (b_norm - r_norm) / d + 2
                else:
                    h = (r_norm - g_norm) / d + 4
                h /= 6
            
            result['hsl'] = f'hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)'
            
        except Exception as e:
            result['erreur'] = str(e)
        
        return result
    
    @staticmethod
    def unit_converter(value: float, from_unit: str, to_unit: str) -> Optional[float]:
        """
        Convertit des unités
        
        Args:
            value: Valeur à convertir
            from_unit: Unité source
            to_unit: Unité cible
            
        Returns:
            Valeur convertie ou None
        """
        length_units = {
            'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
        }
        
        weight_units = {
            'mg': 0.000001, 'g': 0.001, 'kg': 1, 't': 1000,
            'oz': 0.0283495, 'lb': 0.453592
        }
        
        data_units = {
            'b': 1, 'kb': 1024, 'mb': 1024**2, 'gb': 1024**3, 'tb': 1024**4
        }
        
        from_lower = from_unit.lower()
        to_lower = to_unit.lower()
        
        for units in [length_units, weight_units, data_units]:
            if from_lower in units and to_lower in units:
                return value * units[from_lower] / units[to_lower]
        
        return None
    
    @staticmethod
    def get_clipboard() -> Optional[str]:
        """Récupère le contenu du presse-papier"""
        try:
            if platform.system() == 'Windows':
                result = subprocess.run(['powershell', 'Get-Clipboard'], 
                                        capture_output=True, text=True, timeout=5)
                return result.stdout.strip()
            else:
                result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                                        capture_output=True, text=True, timeout=5)
                return result.stdout.strip()
        except Exception:
            return None
    
    @staticmethod
    def set_clipboard(text: str) -> bool:
        """Définit le contenu du presse-papier"""
        try:
            if platform.system() == 'Windows':
                subprocess.run(['powershell', f'Set-Clipboard -Value "{text}"'], 
                               timeout=5, check=True)
                return True
            else:
                process = subprocess.Popen(['xclip', '-selection', 'clipboard'], 
                                           stdin=subprocess.PIPE)
                process.communicate(text.encode())
                return True
        except Exception:
            return False
    
    @staticmethod
    def stopwatch() -> None:
        """Chronomètre simple (retourne le temps écoulé)"""
        print("\nChronométre démarré. Appuyez sur Entrée pour arrêter...")
        start = time.time()
        input()
        elapsed = time.time() - start
        
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = elapsed % 60
        
        print(f"Temps écoulé: {hours:02d}:{minutes:02d}:{seconds:05.2f}")
    
    @staticmethod
    def countdown(seconds: int) -> None:
        """Compte à rebours"""
        seconds = min(seconds, 3600)
        
        for remaining in range(seconds, 0, -1):
            mins, secs = divmod(remaining, 60)
            print(f"\rTemps restant: {mins:02d}:{secs:02d}", end='', flush=True)
            time.sleep(1)
        
        print("\nTerminé!")
