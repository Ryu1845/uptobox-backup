import json
import requests

token1 = "" #uptobox token of the old account
token2 = "" #uptobox token of the new account

r = requests.get('https://uptobox.com/api/user/files?token=' + token1 + '&orderBy=file_name&dir=asc&offset=0&path=%2F%2F&limit=100')
loaded_json = json.loads(r.text)
page_counter = loaded_json["data"]["pageCount"]

for i in range(page_counter):
    try:
        r2 = requests.get('https://uptobox.com/api/user/files?token=' + token1 + '&orderBy=file_name&dir=asc&offset=' + str(i * 100) + '&path=%2F%2F&limit=100')
        loaded_json2 = json.loads(r2.text)
        for x in loaded_json2["data"]["files"]:
            print(x["file_name"] + " (https://uptobox.com/" + x["file_code"] + "/)")
            r3 = requests.get('https://uptobox.com/api/user/file/alias?token=' + token2 + '&file_code=' + x["file_code"])
    except:
        console = False
