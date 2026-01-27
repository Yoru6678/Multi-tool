@echo off
chcp 65001 >nul 2>&1
title Multi-Tool - Installation

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           MULTI-TOOL - INSTALLATION                      ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

:: Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installé ou n'est pas dans le PATH.
    echo Veuillez installer Python 3.8+ depuis https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python détecté
python --version

:: Vérifier pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] pip n'est pas disponible.
    pause
    exit /b 1
)

echo [OK] pip détecté
echo.

:: Mettre à jour pip
echo [INFO] Mise à jour de pip...
python -m pip install --upgrade pip >nul 2>&1

:: Installer les dépendances
echo [INFO] Installation des dépendances...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo [ERREUR] L'installation des dépendances a échoué.
    pause
    exit /b 1
)

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║           INSTALLATION TERMINÉE AVEC SUCCÈS              ║
echo ╚══════════════════════════════════════════════════════════╝
echo.
echo Pour lancer le Multi-Tool, exécutez: run.bat
echo Ou directement: python main.py
echo.

pause
