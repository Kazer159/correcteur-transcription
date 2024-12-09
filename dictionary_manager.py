from unidecode import unidecode

class DictionaryManager:
    def __init__(self):
        self.corrections_perso = {}  # Format: {mot_correct: set(variantes)}
        self.dict_file = "dictionnaire_perso.json"
        
    def load_custom_corrections(self, filename='mots-corrections.txt'):
        """Charge le dictionnaire de corrections personnalisées de manière triée, 
        en ignorant les majuscules et les accents"""
        try:
            corrections = {}
            # Lire toutes les lignes et les trier d'abord, en ignorant accents et majuscules
            with open(filename, 'r', encoding='utf-8') as f:
                lignes = f.readlines()
                # Trier les lignes en utilisant une clé qui ignore accents et majuscules
                lignes = sorted(lignes, key=lambda x: unidecode(x.lower()))
                
            # Traiter les lignes triées
            for ligne in lignes:
                if ':' in ligne:
                    mot_correct, variantes = ligne.strip().split(':')
                    mot_correct = mot_correct.strip()
                    # Stocker le mot correct en minuscules et majuscules
                    if mot_correct not in corrections:
                        corrections[mot_correct] = set()
                        # Ajouter aussi la version avec majuscule
                        corrections[mot_correct].add(mot_correct)
                        corrections[mot_correct].add(mot_correct.capitalize())
                    if variantes:
                        # Trier les variantes en ignorant accents et majuscules
                        variantes_list = variantes.split(',')
                        variantes_list = sorted(variantes_list, key=lambda x: unidecode(x.lower().strip()))
                        for variante in variantes_list:
                            variante = variante.strip()
                            corrections[mot_correct].add(variante.lower())
                            corrections[mot_correct].add(variante.capitalize())
            
            # Convertir en dictionnaire trié en ignorant accents et majuscules
            return dict(sorted(corrections.items(), key=lambda x: unidecode(x[0].lower())))
        except FileNotFoundError:
            return {}
            
    def save_custom_corrections(self, corrections, filename='mots-corrections.txt'):
        """Sauvegarde le dictionnaire de corrections personnalisées"""
        with open(filename, 'w', encoding='utf-8') as f:
            for correction, variantes in sorted(corrections.items()):
                variantes_str = ",".join(sorted(variantes))
                f.write(f"{correction}:{variantes_str}\n")
                
    def add_correction(self, correction, variante):
        """Ajoute une correction au dictionnaire"""
        if correction not in self.corrections_perso:
            self.corrections_perso[correction] = set()
        self.corrections_perso[correction].add(variante.lower())
        
    def remove_correction(self, correction):
        """Supprime une correction du dictionnaire"""
        if correction in self.corrections_perso:
            del self.corrections_perso[correction]
            
    def get_correction_count(self):
        """Retourne le nombre de corrections dans le dictionnaire"""
        return len(self.corrections_perso)
