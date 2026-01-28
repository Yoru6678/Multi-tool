# 🛠️ Multi-Tool Unifié - Version Sécurisée

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%2010%2F11-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Security](https://img.shields.io/badge/security-enhanced-brightgreen.svg)]()

## 📋 Table des Matières

- [Description](#-description)
- [Fonctionnalités](#-fonctionnalités)
- [Mesures de Sécurité](#-mesures-de-sécurité)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [Configuration](#-configuration)
- [FAQ](#-faq)
- [Dépannage](#-dépannage)
- [Avertissement Légal](#%EF%B8%8F-avertissement-légal)
- [Licence](#-licence)
- [Crédits](#-crédits)

## 📖 Description

**Multi-Tool Unifié** est une fusion sécurisée et optimisée de plusieurs multi-tools Python populaires, spécialement conçue pour Windows 10/11. Ce projet combine les fonctionnalités de :

- **3TH1C4L-MultiTool** - Outils réseau et Discord
- **Butcher-Tools** - Outils OSINT et Discord
- **Cyb3rtech-Tool** - Outils de sécurité et recherche
- **Discord-All-Tools-In-One** - Suite complète Discord
- **Multi-tools** - Collection d'utilitaires variés
- **fsociety** - Framework de pentesting

Le projet a été entièrement refondu avec un **focus particulier sur la sécurité**, la **compatibilité Windows**, et une **architecture modulaire** propre.

## ✨ Fonctionnalités

### 🌐 Outils Réseau
- **Afficher mon IP publique** - Récupère votre adresse IP publique
- **Scanner IP** - Scanne une plage d'adresses IP
- **Ping IP** - Teste la connectivité vers une IP
- **Scanner de ports** - Identifie les ports ouverts
- **Informations sur un site web** - Analyse complète d'un site
- **Lookup DNS** - Résolution de noms de domaine
- **Traceroute** - Trace le chemin réseau
- **Whois** - Informations sur un domaine

### 🔍 Outils OSINT
- **Tracker de nom d'utilisateur** - Recherche sur 300+ plateformes
- **Recherche d'email** - Validation et informations
- **Recherche de numéro de téléphone** - Localisation et opérateur
- **Recherche d'adresse IP (GeoIP)** - Géolocalisation précise
- **Recherche sur les réseaux sociaux** - Profils multiples
- **Recherche de domaine** - Historique et propriétaire

### 🔐 Outils Sécurité
- **Générateur de mots de passe** - Mots de passe ultra-sécurisés
- **Vérificateur de force** - Analyse de robustesse
- **Chiffrement de fichiers** - AES-256 avec Fernet
- **Déchiffrement de fichiers** - Déchiffrement sécurisé
- **Hash de fichiers** - MD5, SHA1, SHA256, SHA512
- **Générateur de clés** - Clés cryptographiques

### 💻 Outils Système
- **Informations système** - CPU, RAM, Disque, OS
- **Processus en cours** - Liste et gestion
- **Utilisation du disque** - Analyse d'espace
- **Utilisation du réseau** - Statistiques réseau
- **Nettoyage de fichiers temporaires** - Libération d'espace
- **Variables d'environnement** - Affichage et gestion

### 🌍 Outils Web
- **Scanner de vulnérabilités SQL** - Détection d'injections
- **Vérificateur de headers HTTP** - Analyse de sécurité
- **Extracteur de liens** - Extraction depuis pages web
- **Vérificateur de certificat SSL** - Validation HTTPS
- **Analyseur de robots.txt** - Parsing de directives

### 💬 Outils Discord
- **Informations sur un token** - Détails du compte
- **Vérificateur de tokens** - Validation multiple
- **Informations sur un serveur** - Statistiques complètes
- **Informations sur un utilisateur** - Profil détaillé
- **Convertir ID en token** - Première partie du token
- **Générateur de lien d'invitation** - Pour bots

### 🪝 Outils Webhook
- **Informations sur un webhook** - Détails complets
- **Envoyer un message** - Via webhook
- **Supprimer un webhook** - Suppression sécurisée

### 🎲 Générateurs
- **Générateur de mots de passe** - Personnalisable
- **Générateur de codes Nitro** - Discord Nitro
- **Générateur de noms d'utilisateur** - Aléatoires
- **Générateur de QR codes** - Personnalisés
- **Générateur de UUID** - Identifiants uniques

### 🔧 Utilitaires
- **Encodeur/Décodeur Base64** - Conversion rapide
- **Convertisseur de formats** - Multiples formats
- **Calculatrice de hash** - Algorithmes variés
- **Générateur de Lorem Ipsum** - Texte de remplissage
- **Convertisseur d'unités** - Conversions diverses

## 🔒 Mesures de Sécurité

Ce multi-tool implémente des mesures de sécurité avancées :

### ✅ Validation des Entrées
- **Sanitisation complète** - Suppression des caractères dangereux
- **Validation par regex** - Patterns stricts pour chaque type
- **Protection contre les injections** - SQL, commandes, XSS
- **Limitation de longueur** - Prévention des buffer overflows
- **Détection de caractères nuls** - Protection contre null byte injection

### 🔐 Gestion des Données Sensibles
- **Chiffrement AES-256** - Pour tokens, mots de passe, clés API
- **Hashing sécurisé** - PBKDF2 avec 100,000 itérations
- **Masquage dans les logs** - Aucune donnée sensible loggée
- **Stockage sécurisé** - Jamais en clair
- **Génération cryptographique** - Utilisation de `secrets` module

### 🛡️ Protection des Fichiers
- **Validation des chemins** - Anti path-traversal
- **Vérification des permissions** - Accès contrôlé
- **Répertoires sensibles protégés** - Windows, Program Files
- **Caractères interdits filtrés** - Noms de fichiers Windows

### 📝 Logs Sécurisés
- **Formateur personnalisé** - Masquage automatique
- **Rotation des fichiers** - 10 MB max par fichier
- **Nettoyage automatique** - Suppression après 30 jours
- **Niveaux de log** - INFO, WARNING, ERROR, CRITICAL
- **Pas d'informations système sensibles** - Dans les erreurs

### 🚫 Prévention des Abus
- **Rate limiting** - Limitation des tentatives
- **Timeouts configurables** - Évite les blocages
- **Confirmation requise** - Pour actions sensibles
- **Authentification** - Pour fonctions critiques (optionnel)

### 🦠 Compatibilité Antivirus
- **Pas d'obfuscation** - Code clair et lisible
- **Pas de comportements suspects** - Aucune injection de code
- **Pas d'exécution dynamique** - Évite `eval()`, `exec()`
- **Signatures propres** - Pas de faux positifs

## 📦 Prérequis

### Système d'Exploitation
- **Windows 10** (version 1809 ou supérieure)
- **Windows 11** (toutes versions)

### Python
- **Python 3.8** ou supérieur
- **pip** (gestionnaire de paquets Python)

### Espace Disque
- **Minimum** : 100 MB
- **Recommandé** : 500 MB (avec logs et cache)

### Connexion Internet
- Requise pour certaines fonctionnalités (OSINT, vérifications en ligne)

## 🚀 Installation

### Méthode 1 : Installation Automatique (Recommandée)

1. **Téléchargez le projet**
   ```bash
   # Via Git
   git clone https://github.com/votre-repo/Multi-tool-unified.git
   cd Multi-tool-unified
   
   # Ou téléchargez le ZIP et extrayez-le
   ```

2. **Lancez le script d'installation**
   ```cmd
   install.bat
   ```
   
   Ce script va :
   - Vérifier la version de Python
   - Créer un environnement virtuel
   - Installer toutes les dépendances
   - Créer les répertoires nécessaires
   - Configurer les paramètres par défaut

3. **Lancez le multi-tool**
   ```cmd
   run.bat
   ```

### Méthode 2 : Installation Manuelle

1. **Vérifiez Python**
   ```cmd
   python --version
   ```
   Doit afficher Python 3.8 ou supérieur

2. **Créez un environnement virtuel (optionnel mais recommandé)**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Installez les dépendances**
   ```cmd
   pip install -r requirements.txt
   ```

4. **Lancez le programme**
   ```cmd
   python main.py
   ```

### Vérification de l'Installation

Pour vérifier que tout fonctionne :
```cmd
python main.py --version
```

## 💡 Utilisation

### Démarrage Rapide

1. **Lancez le programme**
   ```cmd
   run.bat
   ```
   ou
   ```cmd
   python main.py
   ```

2. **Acceptez les conditions d'utilisation**
   - Lisez attentivement l'avertissement légal
   - Tapez `O` pour accepter

3. **Naviguez dans les menus**
   - Utilisez les numéros pour sélectionner les options
   - Tapez `00` pour revenir en arrière
   - Tapez `99` pour voir les informations

### Exemples d'Utilisation

#### Exemple 1 : Scanner un réseau
```
Menu Principal → [01] Outils Réseau → [02] Scanner IP
Entrez la plage : 192.168.1.1-192.168.1.254
```

#### Exemple 2 : Générer un mot de passe sécurisé
```
Menu Principal → [03] Outils Sécurité → [01] Générateur de mots de passe
Longueur : 16
Caractères spéciaux : O
```

#### Exemple 3 : Rechercher un nom d'utilisateur
```
Menu Principal → [02] Outils OSINT → [01] Tracker de nom d'utilisateur
Nom d'utilisateur : exemple123
```

### Raccourcis Clavier

- **Ctrl+C** : Quitter le programme
- **Entrée** : Valider une saisie
- **Échap** : Annuler (dans certains menus)

## 📁 Structure du Projet

```
Multi-tool-unified/
│
├── main.py                      # Point d'entrée principal
├── requirements.txt             # Dépendances Python
├── README.md                    # Ce fichier
├── LICENSE                      # Licence MIT
├── .gitignore                   # Fichiers à ignorer par Git
│
├── install.bat                  # Script d'installation Windows
├── run.bat                      # Script de lancement Windows
│
├── config/                      # Configuration
│   ├── __init__.py
│   ├── settings.py              # Gestionnaire de configuration
│   ├── config.ini               # Fichier de configuration
│   └── config.example.ini       # Exemple de configuration
│
├── modules/                     # Modules fonctionnels
│   ├── __init__.py
│   ├── network.py               # Outils réseau
│   ├── osint.py                 # Outils OSINT
│   ├── security_tools.py        # Outils de sécurité
│   ├── system.py                # Outils système
│   ├── web.py                   # Outils web
│   ├── discord_tools.py         # Outils Discord
│   ├── webhook.py               # Outils webhook
│   ├── generators.py            # Générateurs
│   └── utilities.py             # Utilitaires
│
├── utils/                       # Utilitaires communs
│   ├── __init__.py
│   ├── security.py              # Gestionnaire de sécurité
│   ├── logger.py                # Système de logging
│   ├── ui.py                    # Interface utilisateur
│   └── helpers.py               # Fonctions d'aide
│
├── logs/                        # Fichiers de logs
│   └── multi_tool_YYYYMMDD.log
│
├── output/                      # Fichiers de sortie
│   └── (résultats des outils)
│
└── temp/                        # Fichiers temporaires
    └── (fichiers temporaires)
```

## ⚙️ Configuration

### Fichier de Configuration

Le fichier `config/config.ini` contient tous les paramètres :

```ini
[general]
language = fr
theme = default
log_level = INFO
auto_update = false

[security]
mask_sensitive_data = true
require_confirmation = true
max_retries = 3
timeout = 30

[network]
default_timeout = 10
max_threads = 10
use_proxy = false
proxy_url = 

[paths]
output_dir = output
temp_dir = temp
log_dir = logs
```

### Modification de la Configuration

1. **Via l'interface**
   ```
   Menu Principal → [10] Configuration → [02] Modifier les paramètres
   ```

2. **Manuellement**
   - Éditez `config/config.ini` avec un éditeur de texte
   - Redémarrez le programme

### Variables d'Environnement

Vous pouvez également utiliser des variables d'environnement :

```cmd
set MULTITOOL_LOG_LEVEL=DEBUG
set MULTITOOL_TIMEOUT=60
```

## ❓ FAQ

### Q: Le programme ne démarre pas, que faire ?
**R:** Vérifiez que Python 3.8+ est installé et que toutes les dépendances sont installées avec `pip install -r requirements.txt`.

### Q: Mon antivirus bloque le programme, est-ce normal ?
**R:** Certains antivirus peuvent signaler des faux positifs. Le code est open-source et peut être vérifié. Ajoutez une exception si nécessaire.

### Q: Puis-je utiliser ce tool sur Linux/Mac ?
**R:** Le tool est optimisé pour Windows, mais devrait fonctionner sur Linux/Mac avec quelques adaptations mineures.

### Q: Les outils Discord sont-ils légaux ?
**R:** Les outils d'information sont légaux. N'utilisez JAMAIS ces outils pour du spam, du raid, ou toute activité malveillante.

### Q: Comment mettre à jour le programme ?
**R:** Téléchargez la dernière version depuis GitHub et remplacez les fichiers (sauvegardez votre configuration).

### Q: Le programme est-il gratuit ?
**R:** Oui, totalement gratuit et open-source sous licence MIT.

### Q: Puis-je contribuer au projet ?
**R:** Absolument ! Les pull requests sont les bienvenues sur GitHub.

### Q: Les données sont-elles envoyées quelque part ?
**R:** Non, tout est local. Aucune télémétrie, aucun tracking.

## 🔧 Dépannage

### Problème : "Python n'est pas reconnu..."
**Solution :**
1. Réinstallez Python depuis [python.org](https://www.python.org/)
2. Cochez "Add Python to PATH" lors de l'installation
3. Redémarrez votre terminal

### Problème : "Module 'xxx' not found"
**Solution :**
```cmd
pip install --upgrade -r requirements.txt
```

### Problème : "Permission denied"
**Solution :**
- Lancez le terminal en tant qu'administrateur
- Ou installez en mode utilisateur : `pip install --user -r requirements.txt`

### Problème : Le programme est lent
**Solution :**
- Vérifiez votre connexion internet
- Réduisez le nombre de threads dans la configuration
- Fermez les autres programmes

### Problème : Les couleurs ne s'affichent pas
**Solution :**
- Utilisez Windows Terminal au lieu de CMD
- Ou installez : `pip install --upgrade colorama`

### Problème : Erreur de chiffrement
**Solution :**
- Vérifiez que `cryptography` est bien installé
- Réinstallez : `pip uninstall cryptography && pip install cryptography`

## ⚖️ Avertissement Légal

**IMPORTANT : LISEZ ATTENTIVEMENT**

Ce logiciel est fourni à des fins **ÉDUCATIVES** et de **RECHERCHE** uniquement.

### Responsabilités

- L'utilisateur est **SEUL RESPONSABLE** de l'utilisation qu'il fait de cet outil
- Les développeurs ne peuvent être tenus responsables de toute utilisation malveillante, illégale ou non autorisée
- Toute utilisation abusive peut entraîner des **poursuites judiciaires**

### Conditions d'Utilisation

En utilisant ce logiciel, vous acceptez de :
- ✅ Respecter toutes les lois locales et internationales
- ✅ Ne pas utiliser l'outil à des fins malveillantes
- ✅ Obtenir les autorisations nécessaires avant tout test
- ✅ Assumer l'entière responsabilité de vos actions
- ❌ Ne pas utiliser pour du spam, raid, ou harcèlement
- ❌ Ne pas utiliser sur des systèmes sans autorisation
- ❌ Ne pas distribuer de versions modifiées malveillantes

### Clause de Non-Responsabilité

LES AUTEURS OU DÉTENTEURS DU COPYRIGHT NE PEUVENT ÊTRE TENUS RESPONSABLES DE TOUTE RÉCLAMATION, DOMMAGE OU AUTRE RESPONSABILITÉ, QUE CE SOIT DANS UNE ACTION CONTRACTUELLE, DÉLICTUELLE OU AUTRE, DÉCOULANT DE, HORS DE OU EN RELATION AVEC LE LOGICIEL OU L'UTILISATION OU D'AUTRES TRANSACTIONS DANS LE LOGICIEL.

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

```
MIT License

Copyright (c) 2026 Multi-Tool Unifié Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Crédits

Ce projet est une fusion et amélioration de plusieurs outils open-source :

### Outils Sources
- **3TH1C4L-MultiTool** par RPxGoon
- **Butcher-Tools** par intrable
- **Cyb3rtech-Tool** par l'équipe Cyb3rtech
- **Discord-All-Tools-In-One** par AstraaDev
- **Multi-tools** par divers contributeurs
- **fsociety** par Manisso

### Remerciements Spéciaux
- La communauté Python pour les excellentes bibliothèques
- Les contributeurs de tous les projets sources
- Les testeurs et utilisateurs pour leurs retours

### Développement
- **Architecture et sécurité** : Refonte complète
- **Compatibilité Windows** : Optimisations spécifiques
- **Documentation** : Guide complet en français
- **Tests** : Validation sur Windows 10/11

---

## 📞 Support et Contact

- **Issues GitHub** : [Créer une issue](https://github.com/votre-repo/Multi-tool-unified/issues)
- **Discussions** : [Forum de discussion](https://github.com/votre-repo/Multi-tool-unified/discussions)
- **Email** : support@multitool-unified.com (si disponible)

---

## 🔄 Changelog

### Version 1.0.0 (2026-01-28)
- 🎉 Version initiale
- ✅ Fusion de 6 multi-tools
- 🔒 Implémentation des mesures de sécurité
- 🪟 Optimisation pour Windows 10/11
- 📚 Documentation complète en français
- 🧪 Tests sur Windows 10 et 11

---

**⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile sur GitHub !**

**🐛 Vous avez trouvé un bug ? Créez une issue !**

**💡 Vous avez une idée d'amélioration ? Proposez-la !**

---

<div align="center">
  <sub>Développé avec ❤️ pour la communauté</sub>
</div>
