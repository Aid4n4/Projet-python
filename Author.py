# PARTIE 2
# Classe qui représente un auteur et l'ensemble de ses documents
class Author:
    # Question 2.1
    # Constructeur : on crée l'auteur avec son nom, sans aucun document pour l'instant
    def __init__(self, name):
        self.name = name        # nom de l'auteur
        self.ndoc = 0           # nombre de documents écrits par cet auteur
        self.production = {}    # dictionnaire id -> Document : les documents de l'auteur

    # Question 2.2
    # Ajoute un document à la production de l'auteur
    def add(self, id, doc):
        self.ndoc += 1              # un document de plus
        self.production[id] = doc   # on range le document sous son identifiant

    # Représentation de l'auteur, utilisée par print(auteur)
    def __str__(self):
        # On récupère les titres de tous ses documents et on les joint par des virgules
        titres = ', '.join([doc.titre for doc in self.production.values()])
        return f"Auteur(s) : {self.name}\nNombre de documents : {self.ndoc}\nProductions : {titres}"

    # Question 2.4
    # Renvoie (return) une phrase indiquant la taille moyenne des documents de l'auteur, en caractères
    # Elle ne fait pas de print : c'est l'appelant qui affiche le résultat
    def taille_moyenne_doc(self):
        # "if self.ndoc" est vrai quand ndoc != 0 : on évite ainsi une division par zéro
        if self.ndoc:
            # Somme des longueurs (en caractères) des textes de tous ses documents
            somme = sum(len(doc.texte) for doc in self.production.values())
            # // est la division entière : la moyenne est arrondie à l'entier inférieur
            return f"Taille moyenne des documents : {somme//self.ndoc} caractères"
        else:
            # Cas où l'auteur n'a aucun document
            return f"Aucun document n'est écrit par cet auteur"
