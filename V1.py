import urllib.parse as urlp
import urllib.request as urlr
import json
import html
import xmltodict
import pandas as pd
from Document import Document
from Author import Author

id2doc = {}

# PARTIE 1
# Question 1.1
docs_hacker_news = []

URL = "https://hn.algolia.com/api/v1/search?"
params = {
    "query" : "cats",
    "tags" : "story",
    "hitsPerPage" : 50
}
URL += urlp.urlencode(params)
#print(URL)

reponse = urlr.urlopen(URL)
#print(reponse)

data = reponse.read()
#print(data)

data = json.loads(data)
#print(type(data))

#print(data.keys()) # -> champs disponibles

#article = data["hits"][0]
#print(article.keys()) # -> champs disponibles pour un article

#print(type(data["hits"])) # -> liste des publications

#print(len(data["hits"])) # -> nombre de publications

for i, article in enumerate(data["hits"]):
    titre = article.get("title")
    auteur = article.get("author")
    date = article.get("created_at")
    url = article.get("url")
    texte = article.get("story_text")
    if texte:
        texte = texte.replace("<p>", " ")
        texte = html.unescape(texte)
        docs_hacker_news.append(texte)
    else:
        texte = titre
        docs_hacker_news.append(titre)
    id2doc[i+1] = Document(titre, auteur, date, url, texte)

print("Liste des articles :")
for i in range(len(docs_hacker_news)):
    print(f"{i+1} - {docs_hacker_news[i]}")

# Question 1.2
docs_arxiv = []

URL = "https://export.arxiv.org/api/query?"
params = {
    "search_query" : "all:cats",
    "start" : 0,
    "max_results" : 50
}
URL += urlp.urlencode(params)
#print(URL)

reponse = urlr.urlopen(URL)
#print(reponse)

data = reponse.read()
#print(data)
#print(type(data))

data = xmltodict.parse(data)
#print(type(data))

#print(data["feed"].keys()) # -> champs disponibles

#article = data["feed"]["entry"][0]
#print(article.keys()) # -> champs disponibles pour un article

#print(type(data["feed"]["entry"])) # -> liste des publications

#print(len(data["feed"]["entry"])) # -> nombre de publications

decalage = len(id2doc)

for i, article in enumerate(data["feed"]["entry"]):
    titre = article.get("title")
    auteur = article.get("author")
    if auteur is None:
        auteur = ""
    elif isinstance(auteur, list):
        auteur = ", ".join([nom['name'] for nom in auteur])
    else:
        auteur = auteur['name']
    date = article.get("published")
    url = article.get("id")
    texte = article.get("summary")
    if texte:
        texte = texte.replace("\n", " ")
        docs_arxiv.append(texte)
    else:
        texte = titre
        docs_arxiv.append(titre)
    id2doc[i + decalage + 1] = Document(titre, auteur, date, url, texte)

print("Liste des articles :")
for i in range(len(docs_arxiv)):
    print(f"{i+1} - {docs_arxiv[i]}")

print("Nombre de documents :", len(id2doc))
print("Premier document :", id2doc[1])
print("Dernier document :", id2doc[len(id2doc)])

# PARTIE 2
# Question 2.1
texte = docs_hacker_news + docs_arxiv
identifiant = [i+1 for i in range(len(texte))]
origine = []

for article in docs_hacker_news:
    origine.append("hackernews")

for article in docs_arxiv:
    origine.append("arxiv")

df = pd.DataFrame({"id":identifiant, "texte":texte, "origine":origine})

#print(df)

# Question 2.2
df.to_csv("corpus.csv", sep='\t', index=False)

# Question 2.3
df = pd.read_csv("corpus.csv", sep='\t')
#print(df)

# PARTIE 3
# Question 3.1
print(f"Le nombre de documents du corpus est de : {df.shape[0]}")

# Question 3.2
for i, ligne in enumerate(df["texte"]):
    mots = 0
    phrases = 0
    if "." in ligne:
        ligne = ligne.split(".")
        for phrase in ligne:
            if phrase.strip():
                phrases += 1
                phrase = phrase.split()
                mots += len(phrase)
        print(f"Document {i+1} : {mots} mots, {phrases} phrases")
    else:
        ligne = ligne.split()
        mots += len(ligne)
        phrases += 1
        print(f"Document {i+1} : {mots} mots, {phrases} phrase")

# Question 3.3
df = df[df["texte"].str.len() >= 20]
#print(df.shape[0])

# Question 3.4
corpus = " ".join(df["texte"])
#print(corpus)

# TD4
# PARTIE 2
# Question 2.3
id2aut = {}

for id, document in id2doc.items():
    if not document.auteur:
        continue
    auteurs = document.auteur.split(',')
    for auteur in auteurs:
        auteur = auteur.strip()
        if not auteur:
            continue
        if auteur in id2aut:
            id2aut[auteur].add(id, document)
        else:
            id2aut[auteur] = Author(auteur)
            id2aut[auteur].add(id, document)

#print("Nombre d'auteurs :", len(id2aut)) # -> Nombre d'auteurs
#print(id2aut[list(id2aut.keys())[0]]) # -> Premier objet auteur

# Question 2.4
auteur = input("Veuillez saisir le nom d'un auteur : ")
if auteur in id2aut:
    print(f"Nombre de documents : {id2aut[auteur].ndoc}\n{id2aut[auteur].taille_moyenne_doc()}")
else:
    print("Auteur inexistant")
