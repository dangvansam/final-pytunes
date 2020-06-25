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
        #print(t2.split("-"))
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
    
    # new_keys2 = []
    # for e in new_keys:
    #     if "-" in e:
    #         for e2 in e.split("-"):
    #             e2 = e2.strip()
    #             if e2 not in new_keys2:
    #                 new_keys2.append(e2)
    random.shuffle(new_keys)
    print(new_keys)
    next_key = random.choice(exts) + " " + random.choice(new_keys)
    #print(next_key)
    return next_key

#next_keyword(list_title)