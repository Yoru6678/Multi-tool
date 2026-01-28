@echo off
REM ============================================================================
REM Multi-Tool Unifié - Script d'Installation pour Windows
REM Compatible: Windows 10/11
REM ============================================================================

title Multi-Tool Unifié - Installation

echo.
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                              ║
echo ║                    MULTI-TOOL UNIFIÉ - INSTALLATION                          ║
echo ║                         Version 1.0.0                                        ║
echo ║                                                                              ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

REM Vérification des privilèges administrateur
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Exécution avec privilèges administrateur
) else (
    echo [!] ATTENTION: Exécution sans privilèges administrateur
    echo [!] Certaines fonctionnalités peuvent nécessiter des droits élevés
    echo.
)

REM Vérification de Python
echo [1/7] Vérification de Python...
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez installer Python 3.8 ou supérieur depuis:
    echo https://www.python.org/downloads/
    echo.
    echo N'oubliez pas de cocher "Add Python to PATH" lors de l'installation!
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% détecté
echo.

REM Vérification de pip
echo [2/7] Vérification de pip...
python -m pip --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] pip n'est pas installé
    echo Installation de pip...
    python -m ensurepip --default-pip
    if %errorLevel% neq 0 (
        echo [ERREUR] Impossible d'installer pip
        pause
        exit /b 1
    )
)
echo [OK] pip est installé
echo.

REM Mise à jour de pip
echo [3/7] Mise à jour de pip...
python -m pip install --upgrade pip --quiet
if %errorLevel% neq 0 (
    echo [AVERTISSEMENT] Impossible de mettre à jour pip
) else (
    echo [OK] pip mis à jour
)
echo.

REM Création de l'environnement virtuel (optionnel)
echo [4/7] Configuration de l'environnement...
set /p CREATE_VENV="Créer un environnement virtuel? (O/N): "
if /i "%CREATE_VENV%"=="O" (
    if exist venv (
        echo [!] Un environnement virtuel existe déjà
        set /p RECREATE="Le recréer? (O/N): "
        if /i "%RECREATE%"=="O" (
            echo Suppression de l'ancien environnement...
            rmdir /s /q venv
            echo Création du nouvel environnement virtuel...
            python -m venv venv
        )
    ) else (
        echo Création de l'environnement virtuel...
        python -m venv venv
    )
    
    if exist venv\Scripts\activate.bat (
        echo [OK] Environnement virtuel créé
        call venv\Scripts\activate.bat
        echo [OK] Environnement virtuel activé
    ) else (
        echo [ERREUR] Échec de la création de l'environnement virtuel
    )
) else (
    echo [!] Installation dans l'environnement Python global
)
echo.

REM Installation des dépendances
echo [5/7] Installation des dépendances...
echo Ce processus peut prendre plusieurs minutes...
echo.

python -m pip install -r requirements.txt --quiet --no-warn-script-location
if %errorLevel% neq 0 (
    echo [ERREUR] Échec de l'installation des dépendances
    echo.
    echo Tentative d'installation avec plus de détails...
    python -m pip install -r requirements.txt
    if %errorLevel% neq 0 (
        echo.
        echo [ERREUR CRITIQUE] Impossible d'installer les dépendances
        echo Vérifiez votre connexion internet et réessayez
        pause
        exit /b 1
    )
)
echo [OK] Toutes les dépendances sont installées
echo.

REM Création des répertoires nécessaires
echo [6/7] Création des répertoires...
if not exist "logs" mkdir logs
if not exist "output" mkdir output
if not exist "temp" mkdir temp
if not exist "config" mkdir config
echo [OK] Répertoires créés
echo.

REM Création du fichier de configuration par défaut
echo [7/7] Configuration initiale...
if not exist "config\config.ini" (
    copy "config\config.example.ini" "config\config.ini" >nul 2>&1
    if %errorLevel% equ 0 (
        echo [OK] Fichier de configuration créé
    ) else (
        echo [!] Fichier de configuration non créé (sera créé au premier lancement)
    )
) else (
    echo [!] Fichier de configuration existant conservé
)
echo.

REM Vérification de l'installation
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                        VÉRIFICATION DE L'INSTALLATION                        ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.

python -c "import sys; print('[OK] Python:', sys.version.split()[0])"
python -c "import colorama; print('[OK] colorama installé')" 2>nul || echo [!] colorama non installé
python -c "import cryptography; print('[OK] cryptography installé')" 2>nul || echo [!] cryptography non installé
python -c "import requests; print('[OK] requests installé')" 2>nul || echo [!] requests non installé
echo.

REM Résumé
echo ╔══════════════════════════════════════════════════════════════════════════════╗
echo ║                          INSTALLATION TERMINÉE                               ║
echo ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo ✓ Python %PYTHON_VERSION% configuré
echo ✓ Dépendances installées
echo ✓ Répertoires créés
echo ✓ Configuration initialisée
echo.
echo Pour lancer le Multi-Tool Unifié:
echo   1. Double-cliquez sur run.bat
echo   2. Ou exécutez: python main.py
echo.
echo Pour plus d'informations, consultez README.md
echo.

pause
