# PARTIE 2
class Author:
    # Question 2.1
    def __init__(self, name):
        self.name = name
        self.ndoc = 0
        self.production = {}

    # Question 2.2
    def add(self, id, doc):
        self.ndoc += 1
        self.production[id] = doc

    def __str__(self):
        titres = ', '.join([doc.titre for doc in self.production.values()])
        return f"Auteur(s) : {self.name}\nNombre de documents : {self.ndoc}\nProductions : {titres}"

    # Question 2.4
    def taille_moyenne_doc(self):
        if self.ndoc:
            somme = sum(len(doc.texte) for doc in self.production.values())
            return f"Taille moyenne des documents : {somme//self.ndoc} caractères"
        else:
            return f"Aucun document n'est écrit par cet auteur"