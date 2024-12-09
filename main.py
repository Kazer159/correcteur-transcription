#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
from PyQt6.QtWidgets import QApplication
from gui_qt import SpellCheckerGUI

# Rediriger les messages d'erreur vers null
if hasattr(sys, 'frozen'):
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.webenginecontext.debug=false'

# Configuration des chemins pour QtWebEngine
dict_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionaries")
os.makedirs(dict_path, exist_ok=True)  # Créer le dossier s'il n'existe pas

def copy_dictionary_files():
    # Chemin source des dictionnaires (chemin système)
    src_dict_path = os.path.expanduser("~/.local/lib/python3.10/site-packages/PyQt6/Qt6/libexec/qtwebengine_dictionaries")
    
    # Si le répertoire source existe
    if os.path.exists(src_dict_path):
        # Copier tous les fichiers du répertoire source vers le répertoire de destination
        for file in os.listdir(src_dict_path):
            src_file = os.path.join(src_dict_path, file)
            dst_file = os.path.join(dict_path, file)
            if os.path.isfile(src_file):
                shutil.copy2(src_file, dst_file)
                print(f"Copié: {file}")

copy_dictionary_files()  # Copier les fichiers de dictionnaire
os.environ["QTWEBENGINE_DICTIONARIES_PATH"] = dict_path
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-logging --disable-features=SpellcheckService"

def main():
    try:
        app = QApplication(sys.argv)
        window = SpellCheckerGUI()
        window.show()
        app.exec()
    except Exception as e:
        print(f"Une erreur est survenue : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
