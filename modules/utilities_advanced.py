#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Utilitaires Avancés - Outils d'utilitaires et encodage
"""

import logging
import base64
import hashlib
import json
import re
from typing import Optional, Union, Dict, List

logger = logging.getLogger(__name__)


class UtilitiesAdvanced:
    """Utilitaires avancés"""
    
    def __init__(self):
        """Initialisation"""
        pass
    
    def base64_encode(self, text: str) -> str:
        """Encode un texte en Base64"""
        try:
            encoded = base64.b64encode(text.encode()).decode()
            logger.info(f"Base64 encoding: {len(text)} chars")
            return encoded
        except Exception as e:
            logger.error(f"Erreur base64_encode: {str(e)}")
            return ""
    
    def base64_decode(self, encoded_text: str) -> str:
        """Décode un texte Base64"""
        try:
            decoded = base64.b64decode(encoded_text.encode()).decode()
            logger.info(f"Base64 decoding: {len(encoded_text)} chars")
            return decoded
        except Exception as e:
            logger.error(f"Erreur base64_decode: {str(e)}")
            return ""
    
    def hex_encode(self, text: str) -> str:
        """Encode en hexadécimal"""
        try:
            hex_encoded = text.encode().hex()
            logger.info(f"Hex encoding: {len(text)} chars")
            return hex_encoded
        except Exception as e:
            logger.error(f"Erreur hex_encode: {str(e)}")
            return ""
    
    def hex_decode(self, hex_text: str) -> str:
        """Décode depuis hexadécimal"""
        try:
            decoded = bytes.fromhex(hex_text).decode()
            logger.info(f"Hex decoding: {len(hex_text)} chars")
            return decoded
        except Exception as e:
            logger.error(f"Erreur hex_decode: {str(e)}")
            return ""
    
    def url_encode(self, text: str) -> str:
        """URL encoding"""
        try:
            import urllib.parse
            encoded = urllib.parse.quote(text)
            logger.info(f"URL encoding: {len(text)} chars")
            return encoded
        except Exception as e:
            logger.error(f"Erreur url_encode: {str(e)}")
            return ""
    
    def url_decode(self, encoded_text: str) -> str:
        """URL decoding"""
        try:
            import urllib.parse
            decoded = urllib.parse.unquote(encoded_text)
            logger.info(f"URL decoding: {len(encoded_text)} chars")
            return decoded
        except Exception as e:
            logger.error(f"Erreur url_decode: {str(e)}")
            return ""
    
    def rot13_encode(self, text: str) -> str:
        """ROT13 encoding"""
        try:
            result = ""
            for char in text:
                if char.isalpha():
                    if char.islower():
                        result += chr((ord(char) - ord('a') + 13) % 26 + ord('a'))
                    else:
                        result += chr((ord(char) - ord('A') + 13) % 26 + ord('A'))
                else:
                    result += char
            logger.info(f"ROT13 encoding: {len(text)} chars")
            return result
        except Exception as e:
            logger.error(f"Erreur rot13_encode: {str(e)}")
            return ""
    
    def calculate_hash(self, text: str, algorithm: str = "sha256") -> str:
        """Calcule le hash d'un texte"""
        try:
            if algorithm == "md5":
                hash_obj = hashlib.md5()
            elif algorithm == "sha1":
                hash_obj = hashlib.sha1()
            elif algorithm == "sha256":
                hash_obj = hashlib.sha256()
            elif algorithm == "sha512":
                hash_obj = hashlib.sha512()
            else:
                hash_obj = hashlib.sha256()
            
            hash_obj.update(text.encode())
            result = hash_obj.hexdigest()
            logger.info(f"Hash calculation: {algorithm}")
            return result
        except Exception as e:
            logger.error(f"Erreur calculate_hash: {str(e)}")
            return ""
    
    def json_format(self, json_str: str, indent: int = 2) -> str:
        """Formate un JSON"""
        try:
            parsed = json.loads(json_str)
            formatted = json.dumps(parsed, indent=indent, ensure_ascii=False)
            logger.info(f"JSON formatting")
            return formatted
        except Exception as e:
            logger.error(f"Erreur json_format: {str(e)}")
            return ""
    
    def json_minify(self, json_str: str) -> str:
        """Minifie un JSON"""
        try:
            parsed = json.loads(json_str)
            minified = json.dumps(parsed, separators=(',', ':'))
            logger.info(f"JSON minification")
            return minified
        except Exception as e:
            logger.error(f"Erreur json_minify: {str(e)}")
            return ""
    
    def extract_emails(self, text: str) -> List[str]:
        """Extrait les adresses email d'un texte"""
        try:
            pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(pattern, text)
            logger.info(f"Email extraction: {len(emails)} found")
            return list(set(emails))
        except Exception as e:
            logger.error(f"Erreur extract_emails: {str(e)}")
            return []
    
    def extract_urls(self, text: str) -> List[str]:
        """Extrait les URLs d'un texte"""
        try:
            pattern = r'https?://(?:www\.)?[^\s]+'
            urls = re.findall(pattern, text)
            logger.info(f"URL extraction: {len(urls)} found")
            return list(set(urls))
        except Exception as e:
            logger.error(f"Erreur extract_urls: {str(e)}")
            return []
    
    def extract_ips(self, text: str) -> List[str]:
        """Extrait les adresses IP d'un texte"""
        try:
            pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ips = re.findall(pattern, text)
            logger.info(f"IP extraction: {len(ips)} found")
            return list(set(ips))
        except Exception as e:
            logger.error(f"Erreur extract_ips: {str(e)}")
            return []
    
    def remove_duplicates(self, text: str, split_by: str = "\n") -> str:
        """Supprime les doublons"""
        try:
            lines = text.split(split_by)
            unique = list(dict.fromkeys(lines))
            result = split_by.join(unique)
            logger.info(f"Duplicates removed: {len(lines)} -> {len(unique)}")
            return result
        except Exception as e:
            logger.error(f"Erreur remove_duplicates: {str(e)}")
            return text
    
    def line_counter(self, text: str) -> int:
        """Compte les lignes"""
        try:
            count = len(text.strip().split('\n'))
            logger.info(f"Lines counted: {count}")
            return count
        except Exception as e:
            logger.error(f"Erreur line_counter: {str(e)}")
            return 0
    
    def word_counter(self, text: str) -> int:
        """Compte les mots"""
        try:
            words = text.split()
            count = len(words)
            logger.info(f"Words counted: {count}")
            return count
        except Exception as e:
            logger.error(f"Erreur word_counter: {str(e)}")
            return 0
    
    def char_counter(self, text: str) -> int:
        """Compte les caractères"""
        try:
            count = len(text)
            logger.info(f"Characters counted: {count}")
            return count
        except Exception as e:
            logger.error(f"Erreur char_counter: {str(e)}")
            return 0
    
    def convert_case(self, text: str, case_type: str = "upper") -> str:
        """Convertit la casse du texte"""
        try:
            if case_type == "upper":
                result = text.upper()
            elif case_type == "lower":
                result = text.lower()
            elif case_type == "title":
                result = text.title()
            else:
                result = text.upper()
            
            logger.info(f"Case conversion: {case_type}")
            return result
        except Exception as e:
            logger.error(f"Erreur convert_case: {str(e)}")
            return text
    
    def reverse_string(self, text: str) -> str:
        """Inverse un texte"""
        try:
            result = text[::-1]
            logger.info(f"String reversed")
            return result
        except Exception as e:
            logger.error(f"Erreur reverse_string: {str(e)}")
            return text
