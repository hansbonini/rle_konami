#!/usr/bin/bash
PYINSTALLER_PATH="/home/hans/.wine/drive_c/Python35/Scripts"
wine "$PYINSTALLER_PATH/pyinstaller.exe" --onefile main.py
