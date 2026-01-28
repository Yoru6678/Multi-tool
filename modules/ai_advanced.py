#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import logging

logger = logging.getLogger(__name__)

class AIAdvanced:
    def get_random_fact(self):
        """Fetches a random useless fact."""
        try:
            response = requests.get("https://uselessfacts.jsph.pl/api/v2/facts/random")
            response.raise_for_status()  # Raise an exception for bad status codes
            fact = response.json().get("text")
            return fact
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching random fact: {e}")
            return None

    def suggest_activity(self):
        """Suggests a random activity."""
        try:
            response = requests.get("https://www.boredapi.com/api/activity")
            response.raise_for_status()  # Raise an exception for bad status codes
            activity = response.json().get("activity")
            return activity
        except requests.exceptions.RequestException as e:
            logger.error(f"Error suggesting an activity: {e}")
            return None
