"""
Module Cryptographie - Outils de chiffrement et hachage
Sources: Multi-tools, 3TH1C4L-MultiTool
"""

import hashlib
import base64
import secrets
import string
from typing import Optional, Dict, List, Tuple
from pathlib import Path


class CryptoTools:
    """Collection d'outils cryptographiques"""
    
    HASH_ALGORITHMS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'sha3_256', 'sha3_512']
    
    @staticmethod
    def generate_password(
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        digits: bool = True,
        special: bool = True,
        exclude_ambiguous: bool = False
    ) -> str:
        """
        Génère un mot de passe sécurisé
        
        Args:
            length: Longueur du mot de passe
            uppercase: Inclure les majuscules
            lowercase: Inclure les minuscules
            digits: Inclure les chiffres
            special: Inclure les caractères spéciaux
            exclude_ambiguous: Exclure les caractères ambigus (0, O, l, 1, I)
            
        Returns:
            Mot de passe généré
        """
        length = max(8, min(length, 128))
        
        chars = ""
        required = []
        
        lower_chars = "abcdefghijkmnopqrstuvwxyz" if exclude_ambiguous else string.ascii_lowercase
        upper_chars = "ABCDEFGHJKLMNPQRSTUVWXYZ" if exclude_ambiguous else string.ascii_uppercase
        digit_chars = "23456789" if exclude_ambiguous else string.digits
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        if lowercase:
            chars += lower_chars
            required.append(secrets.choice(lower_chars))
        if uppercase:
            chars += upper_chars
            required.append(secrets.choice(upper_chars))
        if digits:
            chars += digit_chars
            required.append(secrets.choice(digit_chars))
        if special:
            chars += special_chars
            required.append(secrets.choice(special_chars))
        
        if not chars:
            chars = string.ascii_letters + string.digits
        
        remaining_length = length - len(required)
        password_chars = required + [secrets.choice(chars) for _ in range(remaining_length)]
        
        secrets.SystemRandom().shuffle(password_chars)
        
        return ''.join(password_chars)
    
    @staticmethod
    def generate_passphrase(word_count: int = 4, separator: str = '-') -> str:
        """
        Génère une phrase de passe facile à mémoriser
        
        Args:
            word_count: Nombre de mots
            separator: Séparateur entre les mots
            
        Returns:
            Phrase de passe
        """
        word_list = [
            "soleil", "lune", "etoile", "nuage", "pluie", "neige", "vent", "orage",
            "montagne", "riviere", "ocean", "foret", "desert", "prairie", "colline", "vallee",
            "rouge", "bleu", "vert", "jaune", "orange", "violet", "blanc", "noir",
            "lion", "tigre", "aigle", "loup", "renard", "ours", "cerf", "lapin",
            "rapide", "lent", "grand", "petit", "fort", "doux", "vif", "calme",
            "piano", "guitar", "violon", "flute", "tambour", "harpe", "orgue", "trompette",
            "printemps", "ete", "automne", "hiver", "matin", "soir", "nuit", "aube",
            "cafe", "the", "pain", "miel", "pomme", "cerise", "orange", "citron"
        ]
        
        word_count = max(3, min(word_count, 10))
        
        words = [secrets.choice(word_list) for _ in range(word_count)]
        words.append(str(secrets.randbelow(100)))
        
        return separator.join(words)
    
    @staticmethod
    def hash_text(text: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Calcule le hash d'un texte
        
        Args:
            text: Texte à hacher
            algorithm: Algorithme de hachage
            
        Returns:
            Hash hexadécimal ou None si erreur
        """
        if algorithm.lower() not in CryptoTools.HASH_ALGORITHMS:
            return None
        
        try:
            hasher = hashlib.new(algorithm.lower())
            hasher.update(text.encode('utf-8'))
            return hasher.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def hash_all(text: str) -> Dict[str, str]:
        """
        Calcule le hash avec tous les algorithmes supportés
        
        Args:
            text: Texte à hacher
            
        Returns:
            Dictionnaire des hashs
        """
        results = {}
        for algo in CryptoTools.HASH_ALGORITHMS:
            try:
                hasher = hashlib.new(algo)
                hasher.update(text.encode('utf-8'))
                results[algo.upper()] = hasher.hexdigest()
            except Exception:
                results[algo.upper()] = "Non disponible"
        return results
    
    @staticmethod
    def hash_file(file_path: str, algorithm: str = 'sha256') -> Optional[str]:
        """
        Calcule le hash d'un fichier
        
        Args:
            file_path: Chemin du fichier
            algorithm: Algorithme de hachage
            
        Returns:
            Hash hexadécimal ou None si erreur
        """
        try:
            path = Path(file_path)
            if not path.exists() or not path.is_file():
                return None
            
            hasher = hashlib.new(algorithm.lower())
            
            with open(path, 'rb') as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            
            return hasher.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def identify_hash(hash_string: str) -> List[str]:
        """
        Identifie le type probable d'un hash
        
        Args:
            hash_string: Hash à identifier
            
        Returns:
            Liste des types possibles
        """
        hash_string = hash_string.strip().lower()
        
        if not all(c in '0123456789abcdef' for c in hash_string):
            return ["Format invalide - doit être hexadécimal"]
        
        length = len(hash_string)
        
        type_map = {
            32: ["MD5", "MD4", "NTLM"],
            40: ["SHA-1", "RIPEMD-160"],
            56: ["SHA-224", "SHA3-224"],
            64: ["SHA-256", "SHA3-256", "BLAKE2s"],
            96: ["SHA-384", "SHA3-384"],
            128: ["SHA-512", "SHA3-512", "BLAKE2b", "Whirlpool"]
        }
        
        return type_map.get(length, [f"Type inconnu (longueur: {length} caractères)"])
    
    @staticmethod
    def encode_base64(text: str) -> str:
        """Encode en Base64"""
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_base64(encoded: str) -> Optional[str]:
        """Décode du Base64"""
        try:
            decoded = base64.b64decode(encoded.encode('utf-8'))
            return decoded.decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def encode_base32(text: str) -> str:
        """Encode en Base32"""
        return base64.b32encode(text.encode('utf-8')).decode('utf-8')
    
    @staticmethod
    def decode_base32(encoded: str) -> Optional[str]:
        """Décode du Base32"""
        try:
            decoded = base64.b32decode(encoded.encode('utf-8'))
            return decoded.decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def encode_hex(text: str) -> str:
        """Encode en hexadécimal"""
        return text.encode('utf-8').hex()
    
    @staticmethod
    def decode_hex(encoded: str) -> Optional[str]:
        """Décode de l'hexadécimal"""
        try:
            return bytes.fromhex(encoded).decode('utf-8')
        except Exception:
            return None
    
    @staticmethod
    def rot13(text: str) -> str:
        """Applique le chiffrement ROT13"""
        result = []
        for char in text:
            if 'a' <= char <= 'z':
                result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
            elif 'A' <= char <= 'Z':
                result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def caesar_cipher(text: str, shift: int = 3, decrypt: bool = False) -> str:
        """
        Applique le chiffrement de César
        
        Args:
            text: Texte à chiffrer/déchiffrer
            shift: Décalage
            decrypt: True pour déchiffrer
            
        Returns:
            Texte transformé
        """
        if decrypt:
            shift = -shift
        
        result = []
        for char in text:
            if char.isalpha():
                base = ord('A') if char.isupper() else ord('a')
                result.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def morse_encode(text: str) -> str:
        """Encode en Morse"""
        morse_dict = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.',
            'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
            'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.',
            'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
            '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...',
            '8': '---..', '9': '----.', ' ': '/'
        }
        return ' '.join(morse_dict.get(c.upper(), '') for c in text)
    
    @staticmethod
    def morse_decode(morse: str) -> str:
        """Décode du Morse"""
        morse_dict = {
            '.-': 'A', '-...': 'B', '-.-.': 'C', '-..': 'D', '.': 'E', '..-.': 'F',
            '--.': 'G', '....': 'H', '..': 'I', '.---': 'J', '-.-': 'K', '.-..': 'L',
            '--': 'M', '-.': 'N', '---': 'O', '.--.': 'P', '--.-': 'Q', '.-.': 'R',
            '...': 'S', '-': 'T', '..-': 'U', '...-': 'V', '.--': 'W', '-..-': 'X',
            '-.--': 'Y', '--..': 'Z', '-----': '0', '.----': '1', '..---': '2',
            '...--': '3', '....-': '4', '.....': '5', '-....': '6', '--...': '7',
            '---..': '8', '----.': '9', '/': ' '
        }
        return ''.join(morse_dict.get(code, '?') for code in morse.split())
    
    @staticmethod
    def check_password_strength(password: str) -> Dict:
        """
        Évalue la force d'un mot de passe
        
        Args:
            password: Mot de passe à évaluer
            
        Returns:
            Analyse détaillée
        """
        result = {
            'longueur': len(password),
            'majuscules': sum(1 for c in password if c.isupper()),
            'minuscules': sum(1 for c in password if c.islower()),
            'chiffres': sum(1 for c in password if c.isdigit()),
            'speciaux': sum(1 for c in password if not c.isalnum()),
            'score': 0,
            'niveau': 'Très faible',
            'suggestions': []
        }
        
        score = 0
        
        if result['longueur'] >= 8:
            score += 1
        else:
            result['suggestions'].append("Minimum 8 caractères recommandés")
        
        if result['longueur'] >= 12:
            score += 1
        if result['longueur'] >= 16:
            score += 1
        
        if result['majuscules'] > 0:
            score += 1
        else:
            result['suggestions'].append("Ajoutez des majuscules")
        
        if result['minuscules'] > 0:
            score += 1
        else:
            result['suggestions'].append("Ajoutez des minuscules")
        
        if result['chiffres'] > 0:
            score += 1
        else:
            result['suggestions'].append("Ajoutez des chiffres")
        
        if result['speciaux'] > 0:
            score += 1
        else:
            result['suggestions'].append("Ajoutez des caractères spéciaux")
        
        unique_ratio = len(set(password)) / len(password) if password else 0
        if unique_ratio > 0.7:
            score += 1
        else:
            result['suggestions'].append("Évitez les caractères répétitifs")
        
        common_patterns = ['123', 'abc', 'qwerty', 'password', 'azerty']
        if any(p in password.lower() for p in common_patterns):
            score -= 2
            result['suggestions'].append("Évitez les séquences communes")
        
        result['score'] = max(0, score)
        
        if score <= 2:
            result['niveau'] = 'Très faible'
        elif score <= 4:
            result['niveau'] = 'Faible'
        elif score <= 6:
            result['niveau'] = 'Moyen'
        elif score <= 8:
            result['niveau'] = 'Fort'
        else:
            result['niveau'] = 'Très fort'
        
        return result
    
    @staticmethod
    def generate_uuid() -> str:
        """Génère un UUID v4"""
        import uuid
        return str(uuid.uuid4())
    
    @staticmethod
    def generate_token(length: int = 32, format: str = 'hex') -> str:
        """
        Génère un token sécurisé
        
        Args:
            length: Longueur en bytes
            format: Format ('hex', 'base64', 'urlsafe')
            
        Returns:
            Token généré
        """
        length = max(16, min(length, 128))
        
        if format == 'base64':
            return secrets.token_bytes(length).hex()
        elif format == 'urlsafe':
            return secrets.token_urlsafe(length)
        else:
            return secrets.token_hex(length)
