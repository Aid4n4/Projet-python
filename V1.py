import urllib.parse as urlp
import urllib.request as urlr
import json
import html
import xmltodict

# Question 1.1
docs = []

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
        docs.append(article["story_text"])
    else:
        docs.append(article["title"])

# Question 1.2
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
        docs.append(article["summary"])
    else:
        docs.append(article["title"])

print("Liste des articles :")
for i in range(len(docs)):
    print(f"{i+1} - {docs[i]}")
