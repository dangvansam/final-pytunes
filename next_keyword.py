from youtube_search import YoutubeSearch 
import json
import random
import string

# results = YoutubeSearch("im lang", max_results=5).to_json()
# results = json.loads(results)
# #print(results)
# results = results["videos"]
# print(results)
# list_title = [e["title"] for e in results]
# print(list_title)

def next_keyword(list_title):
    new_keys = []
    exts = ["nhạc", "cover", "music", "remix"]
    for t in list_title:
        t2 = t.translate(string.punctuation)
        if "|" in t2:
            for e in t2.split("|"):
                if len(e.split(" ")) > 1:
                    e = e.strip()
                    if e not in new_keys:
                        new_keys.append(e)
        else:
            for e in t2.split("-"):
                    e = e.strip()
                    if e not in new_keys:
                        new_keys.append(e)
    
    #random.shuffle(new_keys)
    #print(new_keys)
    next_key = random.choice(new_keys)
    next_key = next_key.replace('\\','')
    if len(next_key.split(" ")) < 3:
        next_key = random.choice(exts) + " " + next_key
    else:
        next_key = " ".join([w.strip() for w in next_key.split(" ")[:3]])
    return next_key

#next_keyword(list_title)