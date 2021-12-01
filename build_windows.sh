#!/usr/bin/bash
PYINSTALLER_PATH="/home/hans/.wine/drive_c/users/hans/Local Settings/Application Data/Programs/Python/Python310-32/Scripts/"
wine "$PYINSTALLER_PATH/pyinstaller.exe" --onefile main.py
