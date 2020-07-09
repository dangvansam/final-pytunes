
import json
from youtubesearchpython import searchYoutube
results = searchYoutube("long cao", offset = 2, mode = "json", max_results = 5).result()
results = json.loads(results)
results = results["search_result"]
print(results)