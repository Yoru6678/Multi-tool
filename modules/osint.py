#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module OSINT - Outils de recherche et investigation
"""

class OSINTTools:
    """Gestionnaire des outils OSINT"""
    
    def __init__(self):
        """Initialisation des outils OSINT"""
        self.username_tracker = self._import_tool("osint.username_tracker", "UsernameTracker")
        self.email_info = self._import_tool("osint.email_info", "EmailInfo")
        self.phone_info = self._import_tool("osint.number_info", "PhoneInfo")
        self.ip_info = self._import_tool("osint.ip_info", "IPInfo")
        self.social_search = self._import_tool("osint.instagram_user_info", "InstagramUserInfo")
    
    def _import_tool(self, module_name, class_name):
        """Import dynamique d'un outil"""
        try:
            module = __import__(module_name, fromlist=[class_name])
            return getattr(module, class_name)()
        except (ImportError, AttributeError) as e:
            return None
    
    def tracker_username(self, username):
        """Tracker un nom d'utilisateur sur les réseaux"""
        if self.username_tracker:
            return self.username_tracker.search(username)
        return None
    
    def search_email(self, email):
        """Rechercher des informations sur un email"""
        if self.email_info:
            return self.email_info.search(email)
        return None
    
    def search_phone(self, phone):
        """Rechercher des informations sur un numéro de téléphone"""
        if self.phone_info:
            return self.phone_info.search(phone)
        return None
    
    def geoip_lookup(self, ip):
        """Rechercher l'IP et la géolocalisation"""
        if self.ip_info:
            return self.ip_info.search(ip)
        return None
