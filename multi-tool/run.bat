@echo off
chcp 65001 >nul 2>&1
title Multi-Tool

:: Vérifier que Python est disponible
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERREUR] Python n'est pas installé.
    echo Veuillez exécuter install.bat d'abord.
    pause
    exit /b 1
)

:: Lancer le Multi-Tool
python main.py

:: En cas d'erreur
if %errorlevel% neq 0 (
    echo.
    echo [INFO] Le programme s'est terminé avec une erreur.
    pause
)
