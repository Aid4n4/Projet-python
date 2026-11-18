import pandas as pd               # pour sauvegarder/charger le corpus sous forme de tableau (CSV)
from Document import Document     # pour recréer des objets Document lors du chargement
from Author import Author         # pour recréer des objets Author lors du chargement

# PARTIE 3
# Classe qui représente l'ensemble des documents et des auteurs
class Corpus:
    # Question 3.1
    # Constructeur : nom obligatoire, auteurs et documents optionnels (None par défaut)
    def __init__(self, nom, authors=None, id2doc=None):
        self.nom = nom
        # On évite d'utiliser {} comme valeur par défaut dans la signature (piège classique de Python :
        # le même dictionnaire serait partagé entre tous les objets). On crée donc un nouveau dict ici.
        self.authors = authors if authors is not None else {}
        self.id2doc = id2doc if id2doc is not None else {}
        # Nombre de documents et d'auteurs, calculés à la création
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)

    # Question 3.2
    # Affiche les ndoc premiers documents triés par date croissante
    def afficher_par_date(self, ndoc):
        # sorted() trie la liste des Document ; key indique sur quoi trier (ici l'attribut date)
        # Les dates sont au format ISO (AAAA-MM-JJ...), donc l'ordre alphabétique = l'ordre chronologique
        documents = sorted(self.id2doc.values(), key=lambda doc: doc.date)
        # [:ndoc] ne garde que les ndoc premiers ; enumerate donne le numéro d'affichage
        for i, doc in enumerate(documents[:ndoc]):
            # f"{doc}" appelle la méthode __str__ de Document (affiche le titre)
            print(f"{i+1} - {doc}")

    # Même principe, mais trié par ordre alphabétique des titres
    def afficher_par_titre(self, ndoc):
        documents = sorted(self.id2doc.values(), key=lambda doc: doc.titre)
        for i, doc in enumerate(documents[:ndoc]):
            print(f"{i+1} - {doc}")

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
            donnees.append({
                "id": id,
                "titre": doc.titre,
                "auteur": doc.auteur,
                "date": doc.date,
                "url": doc.url,
                "texte": doc.texte
            })
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
            id2doc[id] = Document(titre, auteur, date, url, texte)

        # Reconstruction du dictionnaire nom d'auteur -> Author (même logique que dans le script principal)
        authors = {}
        for id, document in id2doc.items():
            # Une valeur vide dans le CSV est relue comme NaN : pd.isna() la détecte
            # (le test "if not document.auteur" ne marcherait pas, car NaN est considéré comme vrai)
            if pd.isna(document.auteur):
                continue
            # Plusieurs auteurs possibles, séparés par des virgules
            auteurs = document.auteur.split(',')
            for auteur in auteurs:
                auteur = auteur.strip()
                if not auteur:
                    continue
                if auteur in authors:
                    # Auteur déjà connu : on ajoute le document
                    authors[auteur].add(id, document)
                else:
                    # Nouvel auteur : on crée l'objet Author puis on lui ajoute le document
                    authors[auteur] = Author(auteur)
                    authors[auteur].add(id, document)

        # On met à jour l'objet courant avec les données chargées
        self.id2doc = id2doc
        self.authors = authors
        # Les compteurs doivent être recalculés, sinon ils garderaient les anciennes valeurs
        self.ndoc = len(self.id2doc)
        self.naut = len(self.authors)
