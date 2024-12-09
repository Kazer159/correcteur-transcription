# Documentation de main.py

## Description générale
`main.py` est le point d'entrée principal de l'application de correction orthographique. Il gère l'initialisation de l'application PyQt, la configuration de QtWebEngine et la gestion des dictionnaires.

## Structure du fichier

### Configuration initiale
- Encodage UTF-8
- Importation des modules nécessaires
- Configuration des variables d'environnement pour QtWebEngine

### Fonctions principales

#### copy_dictionary_files()
```python
def copy_dictionary_files()
```
- **Description :** Copie les fichiers de dictionnaire depuis l'installation système vers le dossier local de l'application
- **Fonctionnement :**
  - Localise les dictionnaires dans le dossier d'installation de PyQt6
  - Crée un dossier local `dictionaries` si nécessaire
  - Copie tous les fichiers de dictionnaire
- **Chemin source :** `~/.local/lib/python3.10/site-packages/PyQt6/Qt6/libexec/qtwebengine_dictionaries`
- **Chemin destination :** `./dictionaries/`

#### main()
```python
def main()
```
- **Description :** Point d'entrée principal de l'application
- **Fonctionnalités :**
  - Initialisation de QApplication
  - Création et affichage de la fenêtre principale
  - Gestion des erreurs avec message sur stderr
  - Exécution de la boucle d'événements Qt

## Configuration de l'environnement

### Variables d'environnement
```python
os.environ["QTWEBENGINE_DICTIONARIES_PATH"] = dict_path
os.environ["QTWEBENGINE_CHROMIUM_FLAGS"] = "--disable-logging --disable-features=SpellcheckService"
```
- Configuration du chemin des dictionnaires pour QtWebEngine
- Désactivation des logs et du service de vérification orthographique de Chromium

### Gestion des logs
```python
if hasattr(sys, 'frozen'):
    os.environ['QT_LOGGING_RULES'] = '*.debug=false;qt.webenginecontext.debug=false'
```
- Désactivation des messages de débogage Qt en mode exécutable

## Dépendances
- PyQt6 : Framework d'interface graphique
- sys : Accès aux paramètres système
- os : Opérations sur le système de fichiers
- shutil : Opérations avancées sur les fichiers

## Structure des dossiers
```
./
├── main.py
└── dictionaries/        # Dossier créé automatiquement
    └── [fichiers de dictionnaire]
```

## Notes techniques
- L'application vérifie si elle est "frozen" (compilée en exécutable)
- Gestion automatique de la copie des dictionnaires
- Gestion robuste des erreurs avec messages appropriés
- Configuration optimisée pour minimiser les logs inutiles

## Exemple d'utilisation
```bash
# Lancement direct depuis Python
python3 main.py

# Ou si le fichier est exécutable
./main.py
```

## Gestion des erreurs
- Les erreurs sont capturées dans le bloc try/except de la fonction main()
- Les messages d'erreur sont redirigés vers stderr
- Code de sortie 1 en cas d'erreur

## Maintenance
Pour maintenir le bon fonctionnement du module :
- Vérifier régulièrement les chemins des dictionnaires
- S'assurer que les permissions sont correctes pour la copie des fichiers
- Mettre à jour les flags Chromium si nécessaire
- Vérifier la compatibilité avec les nouvelles versions de PyQt6
