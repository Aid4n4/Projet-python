import urllib.parse as urlp
import urllib.request as urlr
import json
import html

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

for i in range(len(docs)):
    print(f"{i+1} - {docs[i]}")