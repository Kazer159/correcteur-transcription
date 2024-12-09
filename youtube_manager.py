from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtCore import Qt
from pytube import YouTube

class YouTubeManager:
    def __init__(self, status_label):
        self.status_label = status_label
        self.current_video_url = None
        
    def load_video(self, url):
        """Charge une vidéo YouTube"""
        url = url.strip()
        if url:
            try:
                # Tentative avec un timeout plus long
                yt = YouTube(url, use_oauth=False, allow_oauth_cache=False)
                
                # Attendre que les métadonnées soient chargées
                try:
                    title = yt.title
                except:
                    # Si le titre ne peut pas être récupéré, on utilise l'ID de la vidéo
                    video_id = url.split("v=")[-1].split("&")[0]
                    title = f"Video {video_id}"
                
                # Stocker l'URL
                self.current_video_url = url
                
                # Afficher le titre de la vidéo
                self.status_label.setText(f"Vidéo chargée : {title}")
                
            except Exception as e:
                QMessageBox.warning(None, "Erreur", f"Impossible de charger la vidéo : {str(e)}\nEssayez de mettre à jour pytube avec 'pip install --upgrade pytube'")
                self.status_label.setText("")
