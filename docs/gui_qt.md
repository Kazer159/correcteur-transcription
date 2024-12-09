# Documentation de gui_qt.py

## Description générale
`gui_qt.py` est l'interface graphique principale de l'application de correction orthographique. Elle est construite avec PyQt6 et offre une interface moderne et fonctionnelle pour la correction de texte.

## Composants principaux

### SpellCheckWorker
Une classe qui hérite de `QThread` pour effectuer la vérification orthographique en arrière-plan, évitant ainsi de bloquer l'interface utilisateur.

**Fonctionnalités :**
- Traitement asynchrone de la vérification orthographique
- Émission de signaux de progression
- Émission des mots erronés détectés

### SpellHighlighter
Un surligneur personnalisé qui hérite de `QSyntaxHighlighter` pour mettre en évidence les erreurs orthographiques dans le texte.

**Fonctionnalités :**
- Soulignement des mots incorrects en rouge
- Mise à jour dynamique du surlignage

### SpellCheckerGUI
La classe principale de l'interface graphique.

**Composants de l'interface :**
1. **Barre d'outils :**
   - Bouton "Ouvrir" : Pour charger un fichier texte
   - Bouton "Sauvegarder" : Pour enregistrer le texte
   - Bouton "Corriger" : Pour lancer la vérification orthographique
   - Bouton "Effacer surlignages" : Pour supprimer les marquages d'erreurs
   - Champ de saisie URL : Pour les liens YouTube
   - Bouton "Charger" : Pour charger une vidéo YouTube

2. **Zone principale :**
   - Éditeur de texte avec coloration syntaxique
   - Panneau de correction à droite
   - Lecteur YouTube intégré
   - Dictionnaire personnel

## Fonctionnalités principales
- Correction orthographique en temps réel
- Gestion d'un dictionnaire personnel
- Intégration de vidéos YouTube
- Sauvegarde et chargement de fichiers
- Interface divisée avec splitter ajustable
- Barre de progression pour les opérations longues

## Dépendances
- PyQt6
- PyQt6.QtWebEngineWidgets (pour le lecteur YouTube)
- Modules internes :
  - spell_checker.py
  - dictionary_manager.py
  - youtube_manager.py

## Notes techniques
- L'interface utilise un thème sombre pour l'éditeur de texte
- La police par défaut est 'DejaVu Sans Mono' en taille 11
- Les opérations de correction sont effectuées dans un thread séparé pour maintenir la réactivité de l'interface
