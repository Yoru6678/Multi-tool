#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Discord Avancé - Fonctionnalités complètes Discord
Intégration de: 3TH1C4L-MultiTool, Butcher-Tools, Discord-All-Tools-In-One
"""

import logging
import requests
import json
from typing import Dict, List, Optional, Tuple
import re

logger = logging.getLogger(__name__)


class DiscordAdvanced:
    """Outils Discord avancés et sécurisés"""
    
    BASE_URL = "https://discord.com/api/v10"
    HEADERS_TEMPLATE = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9"
    }
    
    def __init__(self):
        """Initialisation"""
        self.session = requests.Session()
        self.timeout = 10
    
    def validate_token(self, token: str) -> Tuple[bool, Dict]:
        """
        Valide un token Discord et récupère les informations
        
        Args:
            token: Token Discord à valider
        
        Returns:
            Tuple[bool, Dict]: (valid, user_info)
        """
        try:
            headers = self.HEADERS_TEMPLATE.copy()
            headers["Authorization"] = token
            
            response = self.session.get(
                f"{self.BASE_URL}/users/@me",
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"Token valide pour: {user_data.get('username')}")
                return True, {
                    "id": user_data.get("id"),
                    "username": user_data.get("username"),
                    "email": user_data.get("email"),
                    "phone": user_data.get("phone"),
                    "verified": user_data.get("verified"),
                    "avatar": user_data.get("avatar"),
                    "nitro": user_data.get("premium_type", 0) > 0
                }
            
            return False, {"error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            logger.error(f"Erreur validation token: {str(e)}")
            return False, {"error": str(e)}
    
    def check_tokens_batch(self, tokens: List[str]) -> Dict:
        """
        Vérifie multiple tokens rapidement
        
        Args:
            tokens: Liste de tokens
        
        Returns:
            Dict: Résultats pour chaque token
        """
        results = {
            "valid": [],
            "invalid": [],
            "error": []
        }
        
        for token in tokens:
            token = token.strip()
            if not token:
                continue
            
            valid, data = self.validate_token(token)
            
            if valid:
                results["valid"].append({
                    "token": token[:20] + "***",
                    "user": data
                })
            elif "error" in data:
                results["error"].append(token[:20] + "***")
            else:
                results["invalid"].append(token[:20] + "***")
        
        logger.info(f"Batch check: {len(results['valid'])} valides, {len(results['invalid'])} invalides")
        return results
    
    def get_user_info(self, user_id: str, token: str) -> Optional[Dict]:
        """
        Récupère les infos d'un utilisateur Discord
        
        Args:
            user_id: ID Discord de l'utilisateur
            token: Token d'authentification
        
        Returns:
            Dict: Informations utilisateur
        """
        try:
            headers = self.HEADERS_TEMPLATE.copy()
            headers["Authorization"] = token
            
            response = self.session.get(
                f"{self.BASE_URL}/users/{user_id}",
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            
            return None
        except Exception as e:
            logger.error(f"Erreur get_user_info: {str(e)}")
            return None
    
    def get_server_info(self, server_id: str, token: str) -> Optional[Dict]:
        """
        Récupère les infos d'un serveur Discord
        
        Args:
            server_id: ID du serveur
            token: Token d'authentification
        
        Returns:
            Dict: Informations serveur
        """
        try:
            headers = self.HEADERS_TEMPLATE.copy()
            headers["Authorization"] = token
            
            response = self.session.get(
                f"{self.BASE_URL}/guilds/{server_id}",
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "id": data.get("id"),
                    "name": data.get("name"),
                    "icon": data.get("icon"),
                    "owner_id": data.get("owner_id"),
                    "members": data.get("member_count"),
                    "channels": data.get("channels"),
                    "roles": data.get("roles"),
                    "created_at": data.get("created_at")
                }
            
            return None
        except Exception as e:
            logger.error(f"Erreur get_server_info: {str(e)}")
            return None
    
    def get_server_from_invite(self, invite_code: str) -> Optional[Dict]:
        """
        Récupère les infos d'un serveur via invite link
        
        Args:
            invite_code: Code d'invitation Discord
        
        Returns:
            Dict: Informations publiques du serveur
        """
        try:
            # Extraction du code d'invitation
            match = re.search(r'discord\.gg/([a-zA-Z0-9-]+)', invite_code)
            if not match:
                match = re.search(r'([a-zA-Z0-9-]+)', invite_code)
            
            if not match:
                return None
            
            code = match.group(1)
            
            response = self.session.get(
                f"{self.BASE_URL}/invites/{code}",
                headers=self.HEADERS_TEMPLATE,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "guild": data.get("guild"),
                    "channel": data.get("channel"),
                    "inviter": data.get("inviter"),
                    "members": data.get("approximate_member_count"),
                    "online": data.get("approximate_presence_count"),
                    "uses": data.get("uses")
                }
            
            return None
        except Exception as e:
            logger.error(f"Erreur get_server_from_invite: {str(e)}")
            return None
    
    def get_user_guilds(self, token: str) -> List[Dict]:
        """
        Récupère tous les serveurs de l'utilisateur
        
        Args:
            token: Token d'authentification
        
        Returns:
            List[Dict]: Serveurs
        """
        try:
            headers = self.HEADERS_TEMPLATE.copy()
            headers["Authorization"] = token
            
            response = self.session.get(
                f"{self.BASE_URL}/users/@me/guilds",
                headers=headers,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
            
            return []
        except Exception as e:
            logger.error(f"Erreur get_user_guilds: {str(e)}")
            return []
    
    def send_webhook_message(self, webhook_url: str, message: str, username: str = "Bot") -> bool:
        """
        Envoie un message via webhook Discord
        
        Args:
            webhook_url: URL du webhook
            message: Message à envoyer
            username: Nom du bot
        
        Returns:
            bool: Succès
        """
        try:
            payload = {
                "content": message,
                "username": username
            }
            
            response = self.session.post(
                webhook_url,
                json=payload,
                timeout=self.timeout
            )
            
            return response.status_code in [200, 204]
        except Exception as e:
            logger.error(f"Erreur send_webhook_message: {str(e)}")
            return False
    
    def delete_webhook(self, webhook_url: str) -> bool:
        """
        Supprime un webhook Discord
        
        Args:
            webhook_url: URL du webhook
        
        Returns:
            bool: Succès
        """
        try:
            response = self.session.delete(
                webhook_url,
                timeout=self.timeout
            )
            
            return response.status_code in [204, 404]
        except Exception as e:
            logger.error(f"Erreur delete_webhook: {str(e)}")
            return False
