import pandas as pd               # pour sauvegarder/charger le corpus sous forme de tableau (CSV)
from Document import Document, HackerNewsDocument, ArxivDocument     # pour recréer des objets Document lors du chargement
from Author import Author         # pour recréer des objets Author lors du chargement

# PARTIE 3
# Classe qui représente l'ensemble des documents et des auteurs
class Corpus:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, nom, authors=None, id2doc=None):
        if not hasattr(self, '_initialise'):
            self.nom = nom
            self.authors = authors if authors is not None else {}
            self.id2doc = id2doc if id2doc is not None else {}
            self.ndoc = len(self.id2doc)
            self.naut = len(self.authors)
            self._initialise = True

    # Question 3.2
    # Affiche les ndoc premiers documents triés par date croissante
    def afficher_par_date(self, ndoc):
        # sorted() trie la liste des Document ; key indique sur quoi trier (ici l'attribut date)
        # Les dates sont au format ISO (AAAA-MM-JJ...), donc l'ordre alphabétique = l'ordre chronologique
        documents = sorted(self.id2doc.values(), key=lambda doc: doc.date)
        # [:ndoc] ne garde que les ndoc premiers ; enumerate donne le numéro d'affichage
        for i, doc in enumerate(documents[:ndoc]):
            # f"{doc}" appelle la méthode __str__ de Document (affiche le titre)
            print(f"{i+1} - [{doc.getType()}] {doc}")

    # Même principe, mais trié par ordre alphabétique des titres
    def afficher_par_titre(self, ndoc):
        documents = sorted(self.id2doc.values(), key=lambda doc: doc.titre)
        for i, doc in enumerate(documents[:ndoc]):
            print(f"{i+1} - [{doc.getType()}] {doc}")

    # Représentation du corpus, utilisée par print(corpus)
    # (Corpus n'a pas de __str__, Python se rabat donc sur __repr__)
    def __repr__(self):
        return f"Nom : {self.nom}\nNombre de documents : {self.ndoc}\nNombre d'auteurs : {self.naut}"

    # Question 3.3
    # Sauvegarde le corpus dans un fichier "<nom>.csv"
    def save(self):
        # On construit une liste de dictionnaires : un dictionnaire par document
        donnees = []
        for id, doc in self.id2doc.items():
            ligne = {
                "id": id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte,
                "type": doc.getType()
            }
            if isinstance(doc, HackerNewsDocument):
                ligne["score"] = doc.score
                ligne["nb_commentaires"] = doc.nb_commentaires
            elif isinstance(doc, ArxivDocument):
                ligne["co_auteurs"] = ','.join(doc.co_auteurs)
            donnees.append(ligne)
        # Chaque dictionnaire devient une ligne du DataFrame, chaque clef une colonne
        df = pd.DataFrame(donnees)
        # Séparateur tabulation (comme dans le script principal), sans écrire l'index de pandas
        df.to_csv(f"{self.nom}.csv", sep='\t', index=False)

    # Recharge un corpus depuis un fichier CSV créé par save()
    def load(self, fichier):
        df = pd.read_csv(fichier, sep='\t')
        # Reconstruction du dictionnaire id -> Document
        id2doc = {}
        # iterrows() parcourt le DataFrame ligne par ligne ; "_" est l'index, qu'on n'utilise pas
        for _, ligne in df.iterrows():
            id = int(ligne['id'])   # pandas peut renvoyer un type numpy : on convertit en int Python
            titre = ligne['titre']
            auteur = ligne['auteur']
            date = ligne['date']
            url = ligne['url']
            texte = ligne['texte']
            # Vérifier si le document est un document Hacker News ou arXiv
            if ligne['type'] == "HackerNewsDocument":
                id2doc[id] = HackerNewsDocument(titre, auteur, date, url, texte, int(ligne['score']), int(ligne['nb_commentaires']))
            elif ligne['type'] == "ArxivDocument":
                co_auteurs = [] if pd.isna(ligne['co_auteurs']) else ligne['co_auteurs'].split(',')
                id2doc[id] = ArxivDocument(titre, auteur, co_auteurs, date, url, texte)
            else:
                id2doc[id] = Document(titre, auteur, date, url, texte)

        # Reconstruction du dictionnaire nom d'auteur -> Author (même logique que dans le script principal)
        authors = {}

        for id, document in id2doc.items():
            auteurs = []

            if not pd.isna(document.auteur):
                auteurs.append(document.auteur)

            if isinstance(document, ArxivDocument):
                auteurs.extend(document.co_auteurs)

            for auteur in auteurs:
                if auteur in authors:
                    authors[auteur].add(id, document)
                else:
                    authors[auteur] = Author(auteur)
                    authors[auteur].add(id, document)

        # On met à jour l'objet courant avec les données chargées
        self.id2doc = id2doc
        self.authors = authors
        # Les compteurs doivent être recalculés, sinon ils garderaient les anciennes valeurs
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)
