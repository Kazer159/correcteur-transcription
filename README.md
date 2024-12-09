# Correcteur Orthographique avec Interface Qt

Un correcteur orthographique avancé avec interface graphique, intégrant des fonctionnalités de gestion de dictionnaire personnalisé et de transcription de vidéos YouTube.

## Fonctionnalités

- Vérification orthographique en temps réel
- Dictionnaire personnalisé modifiable
- Interface graphique moderne avec Qt6
- Support pour l'ouverture et la sauvegarde de fichiers texte
- Intégration de vidéos YouTube avec transcription
- Surlignage des erreurs orthographiques
- Suggestions de corrections

## Prérequis

- Python 3.10 ou supérieur
- PyQt6 et ses dépendances
- Connexion Internet pour les fonctionnalités YouTube

## Installation

1. Clonez le dépôt :
```bash
git clone [URL_du_depot]
cd "test windsurf 3"
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

1. Lancez l'application :
```bash
python main.py
```

2. L'interface principale permet de :
   - Saisir ou coller du texte à vérifier
   - Charger un fichier texte existant
   - Gérer le dictionnaire personnalisé
   - Intégrer des vidéos YouTube

## Structure du Projet

- `main.py` : Point d'entrée de l'application
- `gui_qt.py` : Interface graphique Qt
- `spell_checker.py` : Logique de vérification orthographique
- `dictionary_manager.py` : Gestion du dictionnaire personnalisé
- `youtube_manager.py` : Gestion des fonctionnalités YouTube
- `dictionaries/` : Dossier contenant les dictionnaires
- `requirements.txt` : Liste des dépendances Python

## Dépendances Principales

- PyQt6 >= 6.6.1
- PyQt6-WebEngine == 6.6.0
- pyspellchecker >= 0.7.2
- pytube >= 15.0.0
- Pillow >= 10.1.0
- python-dotenv == 1.0.0
- unidecode == 1.3.6

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Proposer des améliorations
- Soumettre des pull requests

## Licence

Ce projet est sous licence libre.