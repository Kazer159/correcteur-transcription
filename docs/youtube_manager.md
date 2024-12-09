# Documentation de youtube_manager.py

## Description générale
`youtube_manager.py` est un module qui gère l'intégration des vidéos YouTube dans l'application. Il utilise la bibliothèque `pytube` pour interagir avec l'API YouTube et fournit une interface simple pour charger et gérer les vidéos.

## Classe principale : YouTubeManager

### Initialisation
```python
def __init__(self, status_label)
```
- **Paramètres :**
  - `status_label` : Un widget QLabel pour afficher le statut des opérations
- **Attributs :**
  - `self.status_label` : Référence vers le label de statut
  - `self.current_video_url` : Stocke l'URL de la vidéo actuellement chargée

### Méthodes

#### load_video(url)
```python
def load_video(self, url)
```
- **Description :** Charge une vidéo YouTube à partir de son URL
- **Paramètres :**
  - `url` : L'URL de la vidéo YouTube
- **Fonctionnalités :**
  - Nettoyage de l'URL (suppression des espaces)
  - Configuration de YouTube sans OAuth (use_oauth=False, allow_oauth_cache=False)
  - Tentative de chargement des métadonnées avec gestion d'erreur robuste
  - Fallback sur l'ID de la vidéo si le titre ne peut pas être récupéré
  - Stockage de l'URL courante
  - Mise à jour du label de statut avec le titre de la vidéo
  - Gestion des erreurs avec message d'avertissement détaillé

## Dépendances
- PyQt6 :
  - QMessageBox : Pour afficher les messages d'erreur
  - Qt : Pour les constantes Qt
- pytube : Pour l'interaction avec YouTube

## Gestion des erreurs
- Affichage d'un message d'erreur via QMessageBox en cas d'échec du chargement
- Suggestion de mise à jour de pytube en cas d'erreur
- Fallback sur l'ID de la vidéo si le titre ne peut pas être récupéré

## Notes techniques
- N'utilise pas l'authentification OAuth (use_oauth=False)
- Gestion gracieuse des erreurs de chargement des métadonnées
- Interface utilisateur réactive avec retour visuel via le label de statut

## Exemple d'utilisation
```python
# Création d'une instance
youtube_manager = YouTubeManager(status_label)

# Chargement d'une vidéo
youtube_manager.load_video("https://www.youtube.com/watch?v=example")
```

## Maintenance
Pour maintenir le bon fonctionnement du module, il est recommandé de :
- Garder pytube à jour : `pip install --upgrade pytube`
- Vérifier régulièrement la compatibilité avec l'API YouTube
- Tester avec différents types d'URLs YouTube
