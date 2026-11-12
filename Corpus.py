import pandas as pd
from Document import Document
from Author import Author

# PARTIE 3
class Corpus:
    # Question 3.1
    def __init__(self, nom, authors=None, id2doc=None):
        self.nom = nom
        self.authors = authors if authors is not None else {}
        self.id2doc = id2doc if id2doc is not None else {}
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

    # Question 3.2
    def afficher_par_date(self, ndoc):
        documents = sorted(self.id2doc.values(), key=lambda doc: doc.date)
        for i, doc in enumerate(documents[:ndoc]):
            print(f"{i+1} - {doc}")

    def afficher_par_titre(self, ndoc):
        documents = sorted(self.id2doc.values(), key=lambda doc: doc.titre)
        for i, doc in enumerate(documents[:ndoc]):
            print(f"{i+1} - {doc}")

    def __repr__(self):
        return f"Nom : {self.nom}\nNombre de documents : {self.ndoc}\nNombre d'auteurs : {self.naut}"

    # Question 3.3
    def save(self):
        donnees = []
        for id, doc in self.id2doc.items():
            donnees.append({
                "id": id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte
            })
        df = pd.DataFrame(donnees)
        df.to_csv(f"{self.nom}.csv", sep='\t', index=False)

    def load(self, fichier):
        df = pd.read_csv(fichier, sep='\t')
        id2doc = {}
        for _, ligne in df.iterrows():
            id = int(ligne['id'])
            titre = ligne['titre']
            auteur = ligne['auteur']
            date = ligne['date']
            url = ligne['url']
            texte = ligne['texte']
            id2doc[id] = Document(titre, auteur, date, url, texte)

        authors = {}
        for id, document in id2doc.items():
            if pd.isna(document.auteur):
                continue
            auteurs = document.auteur.split(',')
            for auteur in auteurs:
                auteur = auteur.strip()
                if not auteur:
                    continue
                if auteur in authors:
                    authors[auteur].add(id, document)
                else:
                    authors[auteur] = Author(auteur)
                    authors[auteur].add(id, document)

        self.id2doc = id2doc
        self.authors = authors
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)