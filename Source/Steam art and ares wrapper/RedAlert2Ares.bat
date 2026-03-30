@echo off

set GAME_DIR=G:\Games\Steam\SteamLibrary\steamapps\common\Command ^& Conquer Red Alert II

cd /d "%GAME_DIR%"

start "" "%GAME_DIR%\Syringe.exe" "%GAME_DIR%\gamemd.exe" %*