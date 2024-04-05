from confluence import Confluence
import requests
import utils as utils
import json
import time

id = "id"
pw = "pw"

def retroPageStrReplace(srcStr, dstStr, pageId):
    server = Confluence("https://yourserver")
    server.HTTPBasicAuth(id, pw)

    status, detail = server.getContentStorage(pageId)
    if status == requests.codes.ok:
        contentDict = json.loads(str(detail))
        body = contentDict.get('body')
        if body != None:
            storage = body.get('storage')
            if storage != None:
                content = storage.get('value')
                if content != None:
                    if content.count(srcStr) >0:
                        content = content.replace(srcStr, dstStr)
                        # jira macro will be downloaded as [\"], when we upload [\"]as it is, we will get http 500 error
                        # we have to replae [\"] to [\\\"] before we upload
                        content = content.replace("\"", "\\\"")
                        title = contentDict.get('title')
                        status, detail = server.updatePage(pageId=pageId, content=content, title=title)
                    else:
                        print(srcStr + " is not found in page content.")

if __name__ == '__main__':
    start = time.time()
    retroPageStrReplace("old", "new", 244374587)
    print('処理時間:', time.time()-start)