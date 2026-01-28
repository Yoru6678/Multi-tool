Je te fournis un dépôt GitHub contenant plusieurs multi-tools (outils multifonctions) en Python. Ta mission est de cloner le dépôt, analyser TOUS les multi-tools présents et créer un seul multi-tool unifié qui combine toutes leurs fonctionnalités, avec un focus particulier sur la sécurité et la compatibilité Windows.
Instructions précises :
Clone et Analyse :
Clone le dépôt GitHub complet
Explore TOUTE l'arborescence pour identifier tous les multi-tools
Examine chaque outil pour identifier :
Toutes les fonctionnalités disponibles
Les structures de code utilisées
Les dépendances et bibliothèques Python nécessaires
L'interface utilisateur (GUI avec tkinter, CLI, etc.)
Les potentielles failles de sécurité existantes
Fusion complète : Crée un multi-tool unique en Python qui :
Intègre TOUTES les fonctionnalités de TOUS les outils du dépôt
Évite les duplications de code
Résout les conflits de noms ou de fonctions similaires
Utilise une architecture modulaire et bien organisée
Maintient une interface cohérente et intuitive
Fonctionne parfaitement sur Windows 10/11
SÉCURITÉ (CRITIQUE) : Implémente les mesures de sécurité suivantes :
Validation des entrées : Sanitise toutes les entrées utilisateur contre les injections (SQL, commandes, XSS, etc.)
Gestion des fichiers : Vérifie les chemins pour éviter les path traversal attacks
Permissions : Demande uniquement les permissions strictement nécessaires
Données sensibles : Chiffre les données sensibles (mots de passe, tokens, clés API, etc.)
Logs sécurisés : Ne jamais logger d'informations sensibles (mots de passe, tokens, etc.)
Dépendances : Utilise uniquement des bibliothèques à jour et sécurisées (vérifie les CVE)
Gestion d'erreurs : N'expose pas d'informations système sensibles dans les messages d'erreur
Exécution de code : Évite absolument eval(), exec() et os.system() avec des entrées utilisateur
Scan antivirus : Assure-toi que le code ne déclenche pas de faux positifs
Authentification : Ajoute de l'authentification si nécessaire pour les fonctions sensibles
Rate limiting : Limite les tentatives pour éviter les abus
Compatibilité Windows : Assure-toi que :
Les chemins de fichiers utilisent os.path.join() ou pathlib.Path
Les commandes système sont compatibles Windows (PowerShell/CMD)
L'encodage est géré correctement (UTF-8 avec BOM si nécessaire)
Les dépendances ont des wheels disponibles pour Windows
Teste les chemins spéciaux Windows (%APPDATA%, %TEMP%, %USERPROFILE%, etc.)
Gestion des permissions Windows (UAC si nécessaire)
Compatible avec les antivirus Windows (pas de comportements suspects)
Organisation : Le multi-tool final doit avoir :
Un menu principal clair et numéroté listant toutes les fonctionnalités
Un code bien commenté et structuré (respect de PEP 8)
Une gestion d'erreurs robuste avec des messages clairs en français
Une structure de dossiers propre :
Multi-tool-unified/
├── main.py (point d'entrée)
├── modules/ (fonctionnalités organisées)
├── utils/ (fonctions utilitaires)
├── config/ (fichiers de configuration)
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
Documentation (README.md) : Doit inclure :
Titre et description du projet
Liste complète des fonctionnalités (avec origine de chaque outil)
Instructions d'installation sur Windows (étape par étape)
Prérequis système (Python version, Windows version)
Guide d'utilisation pour chaque fonctionnalité
Mesures de sécurité implémentées
FAQ et dépannage
Licence et crédits
Livrables :
Code Python (.py) compatible Windows
requirements.txt avec versions spécifiques et commentaires
README.md complet en français
.gitignore approprié pour Python
install.bat pour installation automatique sur Windows
run.bat pour lancer facilement le multi-tool
Fichier de configuration exemple (config.example.ini)
Technologies recommandées :
Python 3.8+ (compatible Windows)
Interface : tkinter (natif) ou CLI avec colorama/rich
Sécurité : cryptography, hashlib, secrets, bcrypt
Fichiers : pathlib, os.path
Configuration : configparser ou python-dotenv
Logs : logging (module natif)
Livrable attendu :
Un dépôt GitHub (ou dossier) contenant le multi-tool Python unifié, sécurisé, fusionnant TOUS les outils du dépôt source, prêt à être utilisé sur Windows, avec tous les fichiers nécessaires, une documentation claire en français et des scripts d'installation/lancement pour Windows
