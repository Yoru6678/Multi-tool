#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module Système Avancé - Informations et gestion système
"""

import logging
import os
import platform
import psutil
import subprocess
from typing import Dict, List

logger = logging.getLogger(__name__)


class SystemAdvanced:
    """Outils système avancés"""
    
    def __init__(self):
        """Initialisation"""
        pass
    
    def get_system_info(self) -> Dict:
        """Récupère les informations système"""
        try:
            return {
                "system": platform.system(),
                "release": platform.release(),
                "version": platform.version(),
                "machine": platform.machine(),
                "processor": platform.processor(),
                "python": platform.python_version(),
                "hostname": platform.node()
            }
        except Exception as e:
            logger.error(f"Erreur get_system_info: {str(e)}")
            return {}
    
    def get_cpu_info(self) -> Dict:
        """Récupère les infos CPU"""
        try:
            return {
                "cores_physical": psutil.cpu_count(logical=False),
                "cores_logical": psutil.cpu_count(),
                "usage_percent": psutil.cpu_percent(interval=1),
                "freq_current": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                "freq_max": psutil.cpu_freq().max if psutil.cpu_freq() else None
            }
        except Exception as e:
            logger.error(f"Erreur get_cpu_info: {str(e)}")
            return {}
    
    def get_memory_info(self) -> Dict:
        """Récupère les infos mémoire"""
        try:
            ram = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            return {
                "ram_total_gb": round(ram.total / (1024**3), 2),
                "ram_available_gb": round(ram.available / (1024**3), 2),
                "ram_used_gb": round(ram.used / (1024**3), 2),
                "ram_percent": ram.percent,
                "swap_total_gb": round(swap.total / (1024**3), 2),
                "swap_used_gb": round(swap.used / (1024**3), 2),
                "swap_percent": swap.percent
            }
        except Exception as e:
            logger.error(f"Erreur get_memory_info: {str(e)}")
            return {}
    
    def get_disk_info(self) -> Dict:
        """Récupère les infos disque"""
        try:
            disks = {}
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disks[partition.device] = {
                        "mountpoint": partition.mountpoint,
                        "fstype": partition.fstype,
                        "total_gb": round(usage.total / (1024**3), 2),
                        "used_gb": round(usage.used / (1024**3), 2),
                        "free_gb": round(usage.free / (1024**3), 2),
                        "percent": usage.percent
                    }
                except:
                    continue
            
            return disks
        except Exception as e:
            logger.error(f"Erreur get_disk_info: {str(e)}")
            return {}
    
    def get_network_info(self) -> Dict:
        """Récupère les infos réseau"""
        try:
            return {
                "interfaces": psutil.net_if_addrs(),
                "stats": psutil.net_if_stats(),
                "connections": len(psutil.net_connections())
            }
        except Exception as e:
            logger.error(f"Erreur get_network_info: {str(e)}")
            return {}
    
    def list_processes(self) -> List[Dict]:
        """Liste les processus"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append(proc.info)
                except psutil.NoSuchProcess:
                    pass
            
            return sorted(processes, key=lambda x: x['memory_percent'], reverse=True)[:20]
        except Exception as e:
            logger.error(f"Erreur list_processes: {str(e)}")
            return []
    
    def get_process_info(self, pid: int) -> Dict:
        """Récupère les infos d'un processus"""
        try:
            proc = psutil.Process(pid)
            return {
                "pid": proc.pid,
                "name": proc.name(),
                "status": proc.status(),
                "cpu_percent": proc.cpu_percent(),
                "memory_mb": round(proc.memory_info().rss / (1024**2), 2),
                "create_time": proc.create_time(),
                "exe": proc.exe(),
                "cwd": proc.cwd()
            }
        except Exception as e:
            logger.error(f"Erreur get_process_info: {str(e)}")
            return {}
    
    def get_environment_variables(self) -> Dict:
        """Récupère les variables d'environnement"""
        try:
            return dict(os.environ)
        except Exception as e:
            logger.error(f"Erreur get_environment_variables: {str(e)}")
            return {}
    
    def get_boot_time(self) -> str:
        """Récupère le temps de démarrage"""
        try:
            import datetime
            boot_time = psutil.boot_time()
            return datetime.datetime.fromtimestamp(boot_time).strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            logger.error(f"Erreur get_boot_time: {str(e)}")
            return ""
