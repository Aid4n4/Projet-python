import urllib.parse as urlp
import urllib.request as urlr
import json
import html
import xmltodict
import pandas as pd

'''# PARTIE 1
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

#print(type(data["hits"])) # -> liste des publications

#print(len(data["hits"])) # -> nombre de publications

for article in data["hits"]:
    if article.get("story_text"):
        article["story_text"] = article["story_text"].replace("<p>", " ")
        article["story_text"] = html.unescape(article["story_text"])
        docs_hacker_news.append(article["story_text"])
    else:
        docs_hacker_news.append(article["title"])

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

#print(type(data["feed"]["entry"])) # -> liste des publications

#print(len(data["feed"]["entry"])) # -> nombre de publications

for article in data["feed"]["entry"]:
    if article.get("summary"):
        article["summary"] = article["summary"].replace("\n", " ")
        docs_arxiv.append(article["summary"])
    else:
        docs_arxiv.append(article["title"])

print("Liste des articles :")
for i in range(len(docs_arxiv)):
    print(f"{i+1} - {docs_arxiv[i]}")

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
df.to_csv("corpus.csv", sep='\t', index=False)'''

# Question 2.3
df = pd.read_csv("corpus.csv", sep='\t')

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
        print(f"Document {i} : {mots} mots, {phrases} phrase")

print(f"Le nombre de mots dans le texte est de : {mots}")
print(f"Le nombre de phrases dans le texte est de : {phrases}")
