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

#doc = Document('Chat', 'Miatthew', '02/06/2005', 'URL', 'Les chats domineront le monde.') # -> Instance de test

#doc.afficher()

#print(doc)
