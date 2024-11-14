# Name: paths.py
# Author: Carter Hidalgo
#
# Purpose: provide access to helpful paths for assets to avoid circular imports

from pathlib import Path

base_path = Path(__file__).resolve().parent.parent.parent  # Get directory where the script is located

berserk_path = base_path / 'assets' / 'berserk.exe'
obsidian_path = base_path / 'assets' / 'obsidian.exe'
stockfish_path = base_path / 'assets' / 'stockfish.exe'