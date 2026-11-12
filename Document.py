# PARTIE 1
class Document:
    # Question 1.1
    def __init__(self, titre, auteur, date, url, texte):
        self.titre = titre
        self.auteur = auteur
        self.date = date
        self.url = url
        self.texte = texte

    # Question 1.2
    def afficher(self):
        print(f"Titre : {self.titre}\nAuteur : {self.auteur}\nDate : {self.date}\nUrl : {self.url}\nTexte : {self.texte}\n")

    def __str__(self):
        return f"Titre : {self.titre}"

#doc = Document('Chat', 'Miatthew', '02/06/2005', 'URL', 'Les chats domineront le monde.') # -> Instance de test

#doc.afficher()

#print(doc)

    
