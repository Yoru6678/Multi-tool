# Multi-Tool Unifié

Un outil de sécurité et OSINT (Open Source Intelligence) éthique et légal, combinant plusieurs fonctionnalités utiles dans une interface unifiée.

## Description

Ce multi-tool regroupe des outils légitimes de :
- **Analyse réseau** : scan de ports, ping, DNS, WHOIS, géolocalisation IP
- **Renseignement open source (OSINT)** : recherche de noms d'utilisateur, analyse d'emails et téléphones
- **Cryptographie** : génération de mots de passe, hachage, encodage/décodage
- **Utilitaires** : informations système, gestion de fichiers, conversions

## Fonctionnalités

### Outils Réseau
| Fonction | Description | Source originale |
|----------|-------------|------------------|
| Afficher mon IP | IP locale et publique | 3TH1C4L-MultiTool |
| Ping | Test de connectivité | Cyb3rtech-Tool |
| Scanner de ports | Détection des ports ouverts | 3TH1C4L-MultiTool |
| Recherche DNS | Résolution de noms | Multi-tools |
| Recherche WHOIS | Informations domaine | Cyb3rtech-Tool |
| Géolocalisation IP | Localisation d'une IP | Multi-tools |
| Statut site web | Vérification d'accessibilité | 3TH1C4L-MultiTool |
| Traceroute | Traçage de route | Nouveau |

### Outils OSINT
| Fonction | Description | Source originale |
|----------|-------------|------------------|
| Recherche username | Multi-plateformes | Sherlock, 3TH1C4L-MultiTool |
| Infos GitHub | Profil utilisateur | Nouveau |
| Analyse email | Validation et infos | Multi-tools |
| Analyse téléphone | Infos numéro | Cyb3rtech-Tool |
| Infos site web | Technologies détectées | Multi-tools |
| Recherche image inversée | URLs de recherche | Nouveau |

### Outils Cryptographiques
| Fonction | Description | Source originale |
|----------|-------------|------------------|
| Générateur mot de passe | Sécurisé et configurable | 3TH1C4L-MultiTool |
| Phrase de passe | Mémorisable | Nouveau |
| Hash texte/fichier | MD5, SHA1, SHA256, etc. | Multi-tools |
| Identification hash | Détection du type | Nouveau |
| Base64 | Encodage/décodage | Multi-tools |
| Hexadécimal | Encodage/décodage | Nouveau |
| Chiffrement César | Chiffrement classique | Nouveau |
| Code Morse | Encodage/décodage | Nouveau |
| Force mot de passe | Évaluation sécurité | Nouveau |

### Utilitaires
| Fonction | Description |
|----------|-------------|
| Infos système | Détails de la machine |
| Explorateur fichiers | Navigation répertoires |
| Statistiques texte | Analyse de contenu |
| Convertisseur couleurs | HEX, RGB, HSL |
| Convertisseur unités | Longueur, poids, données |
| JSON formatter | Prettify/Minify |
| Chronomètre | Mesure de temps |

## Prérequis

- **Système** : Windows 10/11 (compatible Linux/macOS)
- **Python** : 3.8 ou supérieur
- **Connexion Internet** : Requise pour certaines fonctionnalités

## Installation

### Windows (Automatique)

1. Téléchargez le projet
2. Double-cliquez sur `install.bat`
3. Attendez l'installation des dépendances

### Windows (Manuel)

```powershell
# Ouvrir PowerShell
cd multi-tool

# Créer un environnement virtuel (optionnel mais recommandé)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r requirements.txt
```

### Linux/macOS

```bash
cd multi-tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Utilisation

### Lancement

**Windows** : Double-cliquez sur `run.bat` ou :
```powershell
python main.py
```

**Linux/macOS** :
```bash
python3 main.py
```

### Navigation

1. Le menu principal s'affiche avec les catégories d'outils
2. Entrez le numéro correspondant à votre choix
3. Suivez les instructions à l'écran
4. Appuyez sur `0` pour revenir au menu précédent
5. `Ctrl+C` pour quitter à tout moment

## Mesures de Sécurité

### Validation des entrées
- Toutes les entrées utilisateur sont nettoyées et validées
- Protection contre les injections (SQL, commandes, XSS)
- Vérification des chemins pour éviter les path traversal

### Gestion des données sensibles
- Aucune donnée sensible n'est stockée en clair
- Les logs ne contiennent pas d'informations sensibles
- Masquage automatique des mots de passe et tokens dans les logs

### Sécurité du code
- Pas d'utilisation de `eval()` ou `exec()` avec des entrées utilisateur
- Pas d'exécution de commandes système non validées
- Timeouts sur toutes les requêtes réseau

### Dépendances
- Utilisation de bibliothèques maintenues et sécurisées
- Toutes les dépendances ont des wheels Windows
- Aucune compilation requise

## Structure du Projet

```
multi-tool/
├── main.py              # Point d'entrée principal
├── modules/             # Modules de fonctionnalités
│   ├── __init__.py
│   ├── network.py       # Outils réseau
│   ├── osint.py         # Outils OSINT
│   ├── crypto_tools.py  # Outils cryptographiques
│   └── utilities.py     # Utilitaires
├── utils/               # Fonctions utilitaires
│   ├── __init__.py
│   ├── security.py      # Fonctions de sécurité
│   ├── validators.py    # Validation des entrées
│   ├── crypto.py        # Cryptographie
│   ├── logger.py        # Logging sécurisé
│   └── config.py        # Configuration
├── config/              # Fichiers de configuration
├── requirements.txt     # Dépendances Python
├── install.bat          # Script d'installation Windows
├── run.bat              # Script de lancement Windows
├── config.example.ini   # Exemple de configuration
├── .gitignore           # Fichiers à ignorer par Git
├── LICENSE              # Licence MIT
└── README.md            # Ce fichier
```

## FAQ et Dépannage

### Le programme ne se lance pas
- Vérifiez que Python 3.8+ est installé : `python --version`
- Vérifiez que les dépendances sont installées : `pip list`
- Sur Windows, utilisez `install.bat` pour réinstaller

### Les couleurs ne s'affichent pas
- Sur Windows ancien, exécutez : `pip install colorama --upgrade`
- Certains terminaux ne supportent pas les couleurs ANSI

### Erreur "Module not found"
```powershell
pip install -r requirements.txt
```

### Le scan de ports est lent
- C'est normal, le scan est limité pour éviter les faux positifs antivirus
- Réduisez la plage de ports pour accélérer

### Erreur de permission
- Sur Windows, lancez en tant qu'administrateur si nécessaire
- Sur Linux/macOS, vérifiez les permissions des fichiers

## Avertissements Légaux

Cet outil est destiné à des fins **légitimes et éthiques** uniquement :
- Tests de sécurité sur vos propres systèmes
- Recherche d'informations publiques
- Apprentissage et éducation

**Il est interdit d'utiliser cet outil pour :**
- Scanner des systèmes sans autorisation
- Collecter des données personnelles sans consentement
- Toute activité illégale

L'utilisateur est entièrement responsable de l'utilisation qu'il fait de cet outil.

## Licence

MIT License - Voir le fichier [LICENSE](LICENSE)

## Crédits

Ce projet est une fusion sécurisée des outils suivants :
- 3TH1C4L-MultiTool
- Cyb3rtech-Tool
- Multi-tools
- Sherlock Project
- Et autres contributions open source

Merci à tous les contributeurs originaux.

## Changelog

### Version 1.0.0 (2024)
- Version initiale
- Fusion de multiples outils
- Interface CLI unifiée
- Mesures de sécurité implémentées
- Compatibilité Windows garantie
