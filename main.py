#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt6.QtWidgets import QApplication
from gui_qt import SpellCheckerGUI

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
