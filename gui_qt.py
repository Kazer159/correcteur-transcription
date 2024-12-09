from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QTextEdit, QTreeWidget, QTreeWidgetItem,
                               QLabel, QProgressBar, QSplitter, QFileDialog, QMessageBox,
                               QFrame, QGroupBox, QApplication, QDialog, QLineEdit)
from PyQt6.QtCore import Qt, QUrl, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QTextCharFormat, QColor, QSyntaxHighlighter, QTextCursor
from PyQt6.QtWebEngineWidgets import QWebEngineView
from spell_checker import SpellCheckerManager
from dictionary_manager import DictionaryManager
from youtube_manager import YouTubeManager
from unidecode import unidecode
import re

class SpellCheckWorker(QThread):
    finished = pyqtSignal(list)
    progress = pyqtSignal(int)

    def __init__(self, spell_manager, text):
        super().__init__()
        self.spell_manager = spell_manager
        self.text = text

    def run(self):
        error_words = []
        words = list(self.spell_manager.extract_words(self.text))
        total_words = len(words)
        
        for i, match in enumerate(words):
            word = match.group(1)
            if not self.spell_manager.check_word(word):
                start = match.start(1)
                error_words.append((word, start, len(word)))
            # Émettre la progression
            progress = int((i + 1) / total_words * 100)
            self.progress.emit(progress)
            
        self.finished.emit(error_words)

class SpellHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.error_format = QTextCharFormat()
        self.error_format.setForeground(QColor("red"))
        self.error_format.setUnderlineStyle(QTextCharFormat.UnderlineStyle.SingleUnderline)
        self.error_words = []

    def highlightBlock(self, text):
        for word, start, length in self.error_words:
            block_start = self.currentBlock().position()
            word_start = start - block_start
            if word_start >= 0 and word_start + length <= len(text):
                if text[word_start:word_start+length].strip() == word:
                    self.setFormat(word_start, length, self.error_format)

class SpellCheckerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Correcteur Orthographique")
        self.resize(1900, 1000)
        
        # Initialisation des gestionnaires
        self.spell_manager = SpellCheckerManager()
        self.dict_manager = DictionaryManager()
        
        # Chargement des corrections personnalisées
        self.dict_manager.corrections_perso = self.dict_manager.load_custom_corrections()
        
        # Variable pour stocker le mot erroné sélectionné
        self.selected_error_word = None
        self.selected_error_index = None
        
        # Thread de correction
        self.spell_check_thread = None
        
        # Bouton de correction
        self.check_button = None
        
        self.setup_gui()
        self.refresh_dict()
        
        # Initialiser le gestionnaire YouTube après setup_gui
        self.youtube_manager = YouTubeManager(self.status_label)
        
    def setup_gui(self):
        """Configure l'interface graphique principale"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)  # Réduire l'espacement entre les widgets
        layout.setContentsMargins(0, 0, 0, 0)  # Supprimer les marges
        
        # Création de la barre d'outils
        toolbar = QWidget()
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        
        self.create_toolbar(toolbar_layout)
        layout.addWidget(toolbar)
        
        # Zone principale avec splitter
        main_splitter = QSplitter()
        main_splitter.setOrientation(Qt.Orientation.Horizontal)
        
        # Zone de texte
        self.text_area = QTextEdit()
        self.text_area.setFont(QFont('DejaVu Sans Mono', 11))
        self.text_area.setStyleSheet("background-color: black; color: white;")
        main_splitter.addWidget(self.text_area)
        
        # Panneau droit
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(5, 5, 5, 5)
        self.create_right_panel(right_layout)
        main_splitter.addWidget(right_panel)
        
        # Définir les proportions du splitter
        main_splitter.setStretchFactor(0, 7)  # Zone de texte (70%)
        main_splitter.setStretchFactor(1, 3)  # Panneau droit (30%)
        
        layout.addWidget(main_splitter, stretch=1)  # Donner le maximum d'espace au splitter
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 0.5px;
            }
        """)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Label pour le statut
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)
        
        # Initialiser le highlighter
        self.highlighter = SpellHighlighter(self.text_area.document())
        
    def create_toolbar(self, layout):
        """Crée la barre d'outils"""
        open_btn = QPushButton("Ouvrir")
        save_btn = QPushButton("Sauvegarder")
        self.check_button = QPushButton("Corriger")
        clear_btn = QPushButton("Effacer surlignages")
        
        # Ajouter les éléments YouTube
        self.url_input = QTextEdit()
        self.url_input.setMaximumHeight(30)
        self.url_input.setMaximumWidth(600)  
        load_btn = QPushButton("Charger")
        
        open_btn.clicked.connect(self.open_file)
        save_btn.clicked.connect(self.save_file)
        self.check_button.clicked.connect(self.check_spelling)
        clear_btn.clicked.connect(self.clear_highlights)
        load_btn.clicked.connect(self.load_video)
        
        layout.addWidget(open_btn)
        layout.addWidget(save_btn)
        layout.addWidget(self.check_button)
        layout.addWidget(clear_btn)
        layout.addWidget(self.url_input)
        layout.addWidget(load_btn)
        layout.addStretch()
        
    def create_right_panel(self, layout):
        """Crée le panneau droit"""
        # Frame de correction
        self.correction_group = QGroupBox("Corrections (0 erreur)")
        correction_layout = QVBoxLayout(self.correction_group)
        correction_layout.setContentsMargins(5, 5, 5, 5)
        
        # Lecteur vidéo
        video_group = QGroupBox("")
        video_layout = QVBoxLayout(video_group)
        video_layout.setContentsMargins(5, 5, 5, 5)
        
        # Lecteur vidéo intégré
        self.web_view = QWebEngineView()
        self.web_view.setMinimumHeight(400)
        video_layout.addWidget(self.web_view)
        
        video_group.setLayout(video_layout)
        layout.addWidget(video_group)
        
        # Dictionnaire personnel
        dict_group = QGroupBox("Dictionnaire Personnel")
        dict_layout = QVBoxLayout(dict_group)
        dict_layout.setContentsMargins(5, 5, 5, 5)
        
        self.dict_tree = QTreeWidget()
        self.dict_tree.setHeaderLabels(["Mot", "Correction"])
        self.dict_tree.itemDoubleClicked.connect(self.on_dict_word_double_click)
        self.dict_tree.setMaximumHeight(200)  # Réduire la hauteur de moitié
        dict_layout.addWidget(self.dict_tree)
        
        # Boutons pour le dictionnaire
        buttons_layout = QHBoxLayout()
        add_btn = QPushButton("Ajouter")
        edit_btn = QPushButton("Modifier")
        delete_btn = QPushButton("Supprimer")
        
        # Connecter les boutons aux fonctions
        add_btn.clicked.connect(self.add_dict_word)
        edit_btn.clicked.connect(self.edit_dict_word)
        delete_btn.clicked.connect(self.delete_dict_word)
        
        # Ajouter les boutons au layout
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(edit_btn)
        buttons_layout.addWidget(delete_btn)
        dict_layout.addLayout(buttons_layout)
        
        layout.addWidget(dict_group)
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", 
                                                 "Fichiers texte (*.txt);;Tous les fichiers (*)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as file:
                    content = file.read()
                    # Ajouter un retour à la ligne après chaque phrase
                    content = re.sub(r'([.!?])\s+', r'\1\n\n', content)
                    self.text_area.setText(content)
                    self.text_area.setFont(QFont('DejaVu Sans Mono', 11))
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le fichier : {str(e)}")
                
    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Sauvegarder le fichier", "", 
                                                 "Fichiers texte (*.txt);;Tous les fichiers (*)")
        if file_name:
            try:
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(self.text_area.toPlainText())
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder le fichier : {str(e)}")
                
    def check_spelling(self):
        """Vérifie l'orthographe du texte"""
        # Désactiver le bouton de correction pendant le processus
        self.check_button.setEnabled(False)
        
        # Réinitialiser et afficher la barre de progression
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)
        self.progress_bar.repaint()  # Force le rafraîchissement immédiat
        self.status_label.setText("Vérification de l'orthographe en cours...")
        
        # Créer et démarrer le thread de correction
        text = self.text_area.toPlainText()
        self.spell_check_thread = SpellCheckWorker(self.spell_manager, text)
        self.spell_check_thread.finished.connect(self.on_spell_check_finished)
        self.spell_check_thread.progress.connect(self.update_progress)
        self.spell_check_thread.start()
        
    def update_progress(self, value):
        """Met à jour la barre de progression"""
        self.progress_bar.setValue(value)
        self.progress_bar.repaint()  # Force le rafraîchissement immédiat
        
    def on_spell_check_finished(self, error_words):
        """Appelé lorsque la vérification orthographique est terminée"""
        self.highlighter.error_words = error_words
        self.highlighter.rehighlight()
        
        # Mise à jour du label de correction
        self.correction_group.setTitle(f"Corrections ({len(error_words)} erreurs)")
        
        # Réactiver le bouton de correction
        self.check_button.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.status_label.setText("Vérification terminée")
        
    def clear_highlights(self):
        """Efface tous les surlignages"""
        self.highlighter.error_words = []
        self.highlighter.rehighlight()
        self.correction_group.setTitle("Corrections (0 erreur)")
        
    def refresh_dict(self):
        """Rafraîchit l'affichage du dictionnaire personnel"""
        self.dict_tree.clear()
        # Trier les mots en ignorant les accents et majuscules
        sorted_items = sorted(self.dict_manager.corrections_perso.items(), 
                            key=lambda x: unidecode(x[0].lower()))
        
        for mot, variantes in sorted_items:
            # Filtrer les variantes pour ne pas inclure le mot exact ou sa version capitalisée
            variantes_filtrees = [var for var in variantes if var.lower() != mot.lower()]
            # Trier les variantes en ignorant les accents et majuscules
            variantes_triees = sorted(variantes_filtrees, 
                                    key=lambda x: unidecode(x.lower()))
            # Joindre les variantes avec des virgules
            variantes_str = ", ".join(variantes_triees)
            item = QTreeWidgetItem([mot, variantes_str])
            self.dict_tree.addTopLevelItem(item)
            
    def on_dict_word_double_click(self, item, column):
        """Gère le double-clic sur un mot du dictionnaire"""
        word = item.text(0)
        correction = item.text(1)
        if QMessageBox.question(self, "Supprimer", 
                              f"Voulez-vous supprimer la correction '{correction}' pour '{word}' ?",
                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            del self.dict_manager.corrections_perso[word]
            self.dict_manager.save_custom_corrections()
            self.refresh_dict()
            
    def load_video(self):
        """Charge et affiche la vidéo YouTube"""
        url = self.url_input.toPlainText()
        if url:
            try:
                # Charger la vidéo avec le gestionnaire YouTube
                self.youtube_manager.load_video(url)
                
                # Extraire l'ID de la vidéo
                video_id = url.split("v=")[-1].split("&")[0]
                
                # Créer l'URL d'intégration
                embed_url = f"https://www.youtube.com/embed/{video_id}"
                
                # Charger la vidéo dans le lecteur intégré
                self.web_view.setUrl(QUrl(embed_url))
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", f"Impossible de charger la vidéo : {str(e)}")
                
    def add_dict_word(self):
        """Ajouter un nouveau mot au dictionnaire"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un mot")
        dialog.setMinimumWidth(600)  # Définir une largeur minimale
        layout = QVBoxLayout()

        # Champs de saisie
        mot_layout = QHBoxLayout()
        mot_label = QLabel("Mot exact:")
        mot_input = QLineEdit()
        mot_layout.addWidget(mot_label)
        mot_layout.addWidget(mot_input)

        variantes_layout = QVBoxLayout()  # Changé en VBox pour meilleur affichage
        variantes_label = QLabel("Variantes (séparées par des virgules):")
        variantes_input = QTextEdit()  # Changé en QTextEdit pour plus d'espace
        variantes_input.setMinimumHeight(100)  # Hauteur minimale
        variantes_layout.addWidget(variantes_label)
        variantes_layout.addWidget(variantes_input)

        # Boutons
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Annuler")
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(mot_layout)
        layout.addLayout(variantes_layout)
        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)

        # Connecter les boutons
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            mot = mot_input.text().strip()
            variantes = {var.strip() for var in variantes_input.toPlainText().split(',') if var.strip()}
            
            if mot:
                if mot not in self.dict_manager.corrections_perso:
                    self.dict_manager.corrections_perso[mot] = set()
                self.dict_manager.corrections_perso[mot].update(variantes)
                self.dict_manager.save_custom_corrections(self.dict_manager.corrections_perso)
                self.refresh_dict()
            else:
                QMessageBox.warning(self, "Attention", "Le mot exact ne peut pas être vide")
        
    def edit_dict_word(self):
        """Modifier un mot du dictionnaire"""
        item = self.dict_tree.currentItem()
        if not item:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un mot à modifier")
            return

        old_mot = item.text(0)
        old_variantes = item.text(1)

        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier un mot")
        dialog.setMinimumWidth(600)  # Définir une largeur minimale
        layout = QVBoxLayout()

        # Champs de saisie
        mot_layout = QHBoxLayout()
        mot_label = QLabel("Mot exact:")
        mot_input = QLineEdit(old_mot)
        mot_layout.addWidget(mot_label)
        mot_layout.addWidget(mot_input)

        variantes_layout = QVBoxLayout()  # Changé en VBox pour meilleur affichage
        variantes_label = QLabel("Variantes (séparées par des virgules):")
        variantes_input = QTextEdit()  # Changé en QTextEdit pour plus d'espace
        variantes_input.setMinimumHeight(100)  # Hauteur minimale
        variantes_input.setText(old_variantes)
        variantes_layout.addWidget(variantes_label)
        variantes_layout.addWidget(variantes_input)

        # Boutons
        buttons_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Annuler")
        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(cancel_button)

        layout.addLayout(mot_layout)
        layout.addLayout(variantes_layout)
        layout.addLayout(buttons_layout)
        dialog.setLayout(layout)

        # Connecter les boutons
        ok_button.clicked.connect(dialog.accept)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            nouveau_mot = mot_input.text().strip()
            nouvelles_variantes = {var.strip() for var in variantes_input.toPlainText().split(',') if var.strip()}
            
            if nouveau_mot:
                # Supprimer l'ancien mot
                if old_mot in self.dict_manager.corrections_perso:
                    del self.dict_manager.corrections_perso[old_mot]
                
                # Ajouter le nouveau mot avec ses variantes
                self.dict_manager.corrections_perso[nouveau_mot] = nouvelles_variantes
                self.dict_manager.save_custom_corrections(self.dict_manager.corrections_perso)
                self.refresh_dict()
            else:
                QMessageBox.warning(self, "Attention", "Le mot exact ne peut pas être vide")
        
    def delete_dict_word(self):
        """Supprimer un mot du dictionnaire"""
        item = self.dict_tree.currentItem()
        if item:
            word = item.text(0)
            if QMessageBox.question(self, "Supprimer", 
                                  f"Voulez-vous supprimer '{word}' du dictionnaire ?",
                                  QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                del self.dict_manager.corrections_perso[word]
                self.dict_manager.save_custom_corrections()
                self.refresh_dict()
        else:
            QMessageBox.warning(self, "Attention", "Veuillez sélectionner un mot à supprimer")
            
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = SpellCheckerGUI()
    window.show()
    sys.exit(app.exec())
