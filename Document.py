# PARTIE 1
# Classe qui représente un document du corpus (un article Hacker News ou arXiv)
class Document:
    # Question 1.1
    # Constructeur : appelé automatiquement à la création d'un objet Document(...)
    # "self" désigne l'objet en cours de création
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre      # titre du document
        self.auteur = auteur    # auteur(s) : chaîne de caractères (plusieurs auteurs séparés par des virgules)
        self.date = date        # date de publication (chaîne telle que renvoyée par l'API)
        self.url = url          # adresse du document en ligne
        self.texte = texte      # contenu textuel (ou titre si le document n'a pas de texte)
        self.type = self.getType()  # type de document : Document, HackerNewsDocument ou ArxivDocument
    # Question 1.2
    # Affiche toutes les informations du document, un champ par ligne ("\n" = retour à la ligne)
    # Cette méthode affiche directement à l'écran : elle ne renvoie rien (None)
    def afficher(self):
        print(f"Titre : {self.titre}\nAuteur : {self.auteur}\nDate : {self.date}\nUrl : {self.url}\nTexte : {self.texte}\n")

    # Méthode spéciale appelée par print(objet) ou str(objet)
    # Elle doit renvoyer (return) une chaîne, et non l'afficher
    # Ici, on ne montre que le titre pour avoir une représentation courte
    def __str__(self):
        return f"Titre : {self.titre}"

    def getType(self):
            return "Document"

#doc = Document('Chat', 'Miatthew', '02/06/2005', 'URL', 'Les chats domineront le monde.') # -> Instance de test

#doc.afficher()

#print(doc)

#TD 5 : PARTIE 1

#Question 1.1
class HackerNewsDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, score, nb_commentaires):
        super().__init__(titre, auteur, date, url, texte) #la mère s'occupe des 5 champs communs
        self.score = score
        self.nb_commentaires = nb_commentaires

    #accesseurs (get) : renvoient la valeur
    def get_score(self):
        return self.score

    def get_nb_commentaires(self):
        return self.nb_commentaires

    def getType(self):
        return "HackerNewsDocument"

    #Mutateurs (set) : modifient la valeur
    def set_score(self, score):
        self.score = score

    def set_nb_commentaires(self, nb_commentaires):
        self.nb_commentaires = nb_commentaires

    def afficher(self):
        super().afficher()
        print(f"Score : {self.score}\nNombre de commentaires : {self.nb_commentaires}\n")

    def __str__(self):
        return f"Titre : {self.titre}, Score : {self.score}, Nombre de commentaires : {self.nb_commentaires}"


#Partie 2
#question 2.1
class ArxivDocument(Document):
    def __init__(self, titre, auteur, date, url, texte, co_auteurs):
        super().__init__(titre, auteur, date, url, texte)
        self.co_auteurs = co_auteurs #liste de noms

    def get_co_auteurs(self):
        return self.co_auteurs

    def getType(self):
        return "ArxivDocument"

    def set_co_auteurs(self, co_auteurs):
        self.co_auteurs = co_auteurs

    def afficher(self):
        super().afficher()
        print(f"Co-auteurs : {', '.join(self.co_auteurs)}\n")

    def __str__(self):
        return f"Titre : {self.titre}, Co-auteurs : {', '.join(self.co_auteurs)}"