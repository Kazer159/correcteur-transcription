# Documentation de spell_checker.py

## Description générale
`spell_checker.py` est le module central de vérification orthographique de l'application. Il utilise la bibliothèque `pyspellchecker` pour fournir des fonctionnalités de correction orthographique en français.

## Classe principale : SpellCheckerManager

### Initialisation
```python
def __init__(self, language='fr')
```
- **Paramètres :**
  - `language` : Code de la langue pour la vérification (par défaut 'fr' pour français)
- **Attributs :**
  - `self.spell` : Instance de SpellChecker configurée pour la langue spécifiée

### Méthodes

#### check_word(word)
```python
def check_word(self, word)
```
- **Description :** Vérifie si un mot est correctement orthographié
- **Paramètres :**
  - `word` : Le mot à vérifier
- **Particularités :**
  - Les mots avec apostrophe sont automatiquement considérés comme corrects
  - Ignore les mots de 2 caractères ou moins
  - Ignore les nombres
  - Nettoie la ponctuation avant la vérification
- **Retour :**
  - `True` si le mot est correct, contient une apostrophe, ou doit être ignoré
  - `False` si le mot est mal orthographié

#### get_suggestions(word)
```python
def get_suggestions(self, word)
```
- **Description :** Fournit des suggestions de correction pour un mot mal orthographié
- **Paramètres :**
  - `word` : Le mot pour lequel obtenir des suggestions
- **Retour :**
  - Un ensemble de mots suggérés comme corrections possibles

#### extract_words(text)
```python
def extract_words(self, text)
```
- **Description :** Extrait les mots d'un texte tout en préservant la ponctuation
- **Paramètres :**
  - `text` : Le texte à analyser
- **Particularités :**
  - Utilise une expression régulière avancée
  - Gère les mots avec apostrophe comme une seule unité
  - Préserve la ponctuation pour le remplacement
- **Retour :**
  - Un itérateur de correspondances regex contenant les mots et leur ponctuation

## Dépendances
- spellchecker : Pour la vérification orthographique de base
- re : Pour l'extraction des mots avec expressions régulières
- string : Pour le traitement de la ponctuation

## Expressions régulières
Le module utilise l'expression régulière suivante pour l'extraction des mots :
```python
r'\b([a-zA-ZÀ-ÿ]+(?:\'[a-zA-ZÀ-ÿ]+)?)([\s\.,;:!?\'\"]*)'
```
- Capture les caractères alphabétiques, y compris les accents
- Gère les mots composés avec apostrophe
- Préserve la ponctuation et les espaces

## Notes techniques
- Support complet des caractères accentués français
- Traitement spécial des mots avec apostrophe
- Optimisé pour la langue française
- Filtrage intelligent des mots courts et des nombres

## Exemple d'utilisation
```python
# Création d'une instance
checker = SpellCheckerManager()

# Vérification d'un mot
if not checker.check_word("bonjour"):
    suggestions = checker.get_suggestions("bonjour")
    print(f"Suggestions : {suggestions}")

# Extraction et vérification de mots dans un texte
for match in checker.extract_words("Le texte à vérifier"):
    word = match.group(1)
    if not checker.check_word(word):
        print(f"Erreur : {word}")
