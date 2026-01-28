@echo off
REM ============================================================================
REM Multi-Tool Unifié - Script de Lancement pour Windows
REM Compatible: Windows 10/11
REM ============================================================================

title Multi-Tool Unifié v1.0.0

REM Vérification de Python
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH
    echo.
    echo Veuillez exécuter install.bat d'abord
    pause
    exit /b 1
)

REM Activation de l'environnement virtuel si présent
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
    echo [INFO] Environnement virtuel activé
)

REM Vérification des dépendances critiques
python -c "import colorama" >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERREUR] Dépendances manquantes
    echo.
    echo Veuillez exécuter install.bat d'abord
    pause
    exit /b 1
)

REM Lancement du programme
cls
python main.py

REM Gestion de la sortie
if %errorLevel% neq 0 (
    echo.
    echo [ERREUR] Le programme s'est terminé avec une erreur
    echo Code d'erreur: %errorLevel%
    echo.
    echo Consultez les logs dans le dossier 'logs' pour plus de détails
    pause
)

REM Désactivation de l'environnement virtuel
if exist venv\Scripts\deactivate.bat (
    call venv\Scripts\deactivate.bat
)
