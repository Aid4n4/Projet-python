import urllib.parse as urlp      # pour construire les URL (encodage des paramètres)
import urllib.request as urlr    # pour envoyer les requêtes HTTP vers les API
import json                      # pour décoder les réponses au format JSON (Hacker News)
import html                      # pour convertir les entités HTML (&amp;, &#x27;...) en vrais caractères
import xmltodict                 # pour convertir le XML renvoyé par arXiv en dictionnaire Python
import pandas as pd              # pour manipuler le corpus sous forme de tableau
from Document import Document, HackerNewsDocument, ArxivDocument    # classe maison représentant un document
from Author import Author        # classe maison représentant un auteur
from Corpus import Corpus        # classe maison représentant l'ensemble du corpus

# Dictionnaire qui associe un identifiant (entier) à chaque objet Document
id2doc = {}

# PARTIE 1
# Question 1.1
# Liste qui contiendra uniquement les textes des articles Hacker News
docs_hacker_news = []

# Construction de l'URL de la requête : adresse de l'API + paramètres
URL = "https://hn.algolia.com/api/v1/search?"
params = {
    "query" : "cats",        # mot-clef recherché
    "tags" : "story",        # on ne garde que les "stories" (pas les commentaires)
    "hitsPerPage" : 50       # nombre de résultats demandés
}
# urlencode transforme le dictionnaire en "query=cats&tags=story&hitsPerPage=50"
URL += urlp.urlencode(params)
#print(URL)

# Envoi de la requête HTTP
reponse = urlr.urlopen(URL)
#print(reponse)

# Lecture du contenu de la réponse (renvoyé sous forme d'octets)
data = reponse.read()
#print(data)

# Conversion du JSON (octets) en dictionnaire Python
data = json.loads(data)
#print(type(data))

#print(data.keys()) # -> champs disponibles

#article = data["hits"][0]
#print(article.keys()) # -> champs disponibles pour un article

#print(type(data["hits"])) # -> liste des publications

#print(len(data["hits"])) # -> nombre de publications

# Parcours des articles : i est la position, article est un dictionnaire
for i, article in enumerate(data["hits"]):
    # .get() renvoie None si la clef n'existe pas, au lieu de lever une KeyError
    titre = article.get("title")
    auteur = article.get("author")
    date = article.get("created_at")
    url = article.get("url")
    texte = article.get("story_text")
    score = article.get("points")
    nb_commentaires = article.get("num_comments")
    if texte:
        # Le texte contient du HTML : on remplace les balises <p> par des espaces
        texte = texte.replace("<p>", " ")
        # On convertit les entités HTML en caractères normaux
        texte = html.unescape(texte)
        docs_hacker_news.append(texte)
    else:
        # Beaucoup d'articles n'ont pas de texte : on utilise le titre à la place
        texte = titre
        docs_hacker_news.append(titre)
    # On crée le Document et on le range dans id2doc (ids à partir de 1)
    id2doc[i+1] = HackerNewsDocument(titre, auteur, date, url, texte, score, nb_commentaires)

# Affichage numéroté des textes récupérés
print("Liste des articles :")
for i in range(len(docs_hacker_news)):
    print(f"{i+1} - {docs_hacker_news[i]}")

# Question 1.2
# Liste qui contiendra uniquement les textes des articles arXiv
docs_arxiv = []

# Même démarche que pour Hacker News, avec l'API d'arXiv
URL = "https://export.arxiv.org/api/query?"
params = {
    "search_query" : "all:cats",   # recherche dans tous les champs
    "start" : 0,                   # index du premier résultat
    "max_results" : 50             # nombre de résultats demandés
}
URL += urlp.urlencode(params)
#print(URL)

reponse = urlr.urlopen(URL)
#print(reponse)

data = reponse.read()
#print(data)
#print(type(data))

# arXiv répond en XML (pas en JSON) : xmltodict le convertit en dictionnaire
data = xmltodict.parse(data)
#print(type(data))

#print(data["feed"].keys()) # -> champs disponibles

#article = data["feed"]["entry"][0]
#print(article.keys()) # -> champs disponibles pour un article

#print(type(data["feed"]["entry"])) # -> liste des publications

#print(len(data["feed"]["entry"])) # -> nombre de publications

# Nombre de documents déjà stockés (ceux de Hacker News) : sert à continuer la numérotation
decalage = len(id2doc)

for i, article in enumerate(data["feed"]["entry"]):
    titre = article.get("title")
    # Le champ "author" a trois formes possibles selon l'article :
    auteurs = article.get("author")
    if auteurs is None:
        auteurs = []
    elif not isinstance(auteurs, list):
        auteurs = [auteurs]
    noms_auteurs = [nom['name'] for nom in auteurs]
    if noms_auteurs:
        auteur = noms_auteurs[0]
        co_auteurs = noms_auteurs[1:]
    else:
        auteur = None
        co_auteurs = []
    date = article.get("published")
    url = article.get("id")
    texte = article.get("summary")
    if texte:
        # Le résumé contient des retours à la ligne : on les remplace par des espaces
        texte = texte.replace("\n", " ")
        docs_arxiv.append(texte)
    else:
        # Pas de résumé : on utilise le titre
        texte = titre
        docs_arxiv.append(titre)
    # Les ids continuent après ceux de Hacker News (decalage + 1, decalage + 2, ...)
    id2doc[i + decalage + 1] = ArxivDocument(titre, auteur, co_auteurs, date, url, texte)

print("Liste des articles :")
for i in range(len(docs_arxiv)):
    print(f"{i+1} - {docs_arxiv[i]}")

# Vérifications : taille totale, premier et dernier document
print("Nombre de documents :", len(id2doc))
print("Premier document :", id2doc[1])
print("Dernier document :", id2doc[len(id2doc)])

# PARTIE 2
# Question 2.1
# On regroupe les textes des deux sources dans une seule liste
texte = docs_hacker_news + docs_arxiv
# Identifiants de 1 à N, dans le même ordre que id2doc
identifiant = [i+1 for i in range(len(texte))]
# Liste de l'origine de chaque texte, dans le même ordre que "texte"
origine = []

for article in docs_hacker_news:
    origine.append("hackernews")

for article in docs_arxiv:
    origine.append("arxiv")

# Création du DataFrame : une colonne par liste, une ligne par document
df = pd.DataFrame({"id":identifiant, "texte":texte, "origine":origine})

#print(df)

# Question 2.2
# Sauvegarde en CSV avec tabulation comme séparateur (les textes contiennent des virgules)
# index=False : on n'écrit pas l'index de pandas dans le fichier
df.to_csv("corpus.csv", sep='\t', index=False)

# Question 2.3
# Rechargement du fichier : on vérifie que la sauvegarde est lisible
df = pd.read_csv("corpus.csv", sep='\t')
#print(df)

# PARTIE 3
# Question 3.1
# df.shape = (nombre de lignes, nombre de colonnes) ; [0] = nombre de documents
print(f"Le nombre de documents du corpus est de : {df.shape[0]}")

# Question 3.2
# Pour chaque texte : nombre de mots et de phrases
for i, ligne in enumerate(df["texte"]):
    mots = 0
    phrases = 0
    if "." in ligne:
        # On découpe le texte en phrases en coupant à chaque point
        ligne = ligne.split(".")
        for phrase in ligne:
            # strip() ignore les morceaux vides (ex. ce qui suit le dernier point)
            if phrase.strip():
                phrases += 1
                # split() sans argument découpe sur les espaces : on obtient la liste des mots
                phrase = phrase.split()
                mots += len(phrase)
        print(f"Document {i+1} : {mots} mots, {phrases} phrases")
    else:
        # Pas de point : on considère que le texte est une seule phrase
        ligne = ligne.split()
        mots += len(ligne)
        phrases += 1
        print(f"Document {i+1} : {mots} mots, {phrases} phrase")

# Question 3.3
# On ne garde que les documents d'au moins 20 caractères (masque booléen sur la colonne texte)
df = df[df["texte"].str.len() >= 20]
#print(df.shape[0])

# Question 3.4
# Concaténation de tous les textes en une seule chaîne, séparés par un espace
corpus = " ".join(df["texte"])
#print(corpus)

# TD4
# PARTIE 2
# Question 2.3
# Dictionnaire : nom d'un auteur -> objet Author (qui regroupe ses documents)
id2aut = {}

for id, document in id2doc.items():
    auteurs = []
    if document.auteur:
        auteurs.append(document.auteur)
    if isinstance(document, ArxivDocument):
        auteurs.extend(document.co_auteurs)
    for auteur in auteurs:
        if auteur in id2aut:
            id2aut[auteur].add(id, document)
        else:
            id2aut[auteur] = Author(auteur)
            id2aut[auteur].add(id, document)

# Question 2.4
# Interaction avec l'utilisateur : on demande un nom d'auteur
auteur = input("Veuillez saisir le nom d'un auteur : ")
if auteur in id2aut:
    # Affiche le nombre de documents de l'auteur et la taille moyenne de ses documents
    print(f"Nombre de documents : {id2aut[auteur].ndoc}\n{id2aut[auteur].taille_moyenne_doc()}")
else:
    print("Auteur inexistant")

# PARTIE 3
# Question 3.4
# Création du corpus à partir des auteurs et des documents
corpus_test = Corpus('Corpus_test', id2aut, id2doc)
# Affichage du corpus (appelle la méthode d'affichage de la classe Corpus)
print(corpus_test)
# Sauvegarde du corpus sur disque
corpus_test.save()

# Création d'un corpus vide, puis chargement depuis le fichier sauvegardé
corpus_charge = Corpus("Corpus_charge")
corpus_charge.load("Corpus_test.csv")
# Affichage pour vérifier que le corpus chargé est identique à celui sauvegardé
print(corpus_charge)
