import requests
from requests.auth import HTTPBasicAuth
import json
import datetime
from time import gmtime, strftime
import utils

class Confluence:
    authParam = HTTPBasicAuth("id","pwd")
    authType = "httpBasic"
    serverUrl = "https://your.server"

    def content_endpoint(self, id):
        return self.serverUrl + "/confluence/rest/api/content/" + str(id)
    
    def content_history_endpoint(self, id):
        return self.content_endpoint(id) + "/history"
    
    def child_content_endpoint(self, id):
        return self.content_endpoint(id) + "/child/page"
    
    def content_label_endpoint(self, id):
        return self.content_endpoint(id) + "/label"
        
    def user_endpoint(self, id):
        return self.serverUrl + "/confluence/rest/api/user?key="+str(id)

    def page_viewsByUser_endpoint(self, id):
        return self.serverUrl + "/confluence/rest/confanalytics/1.0/content/viewsByUser?contentId="+str(id)+"&contentType=page"

    def page_viewsByDate_endpoint(self, id, fromDate, toDate, timeZone):
        # fromDate=2024-01-02T15%3A00%3A00.000Z & toDate=2024-04-02T15%3A00%3A00.000Z & timezone=GMT%2B09%3A00
        return self.serverUrl + "/confluence/rest/confanalytics/1.0/content/viewsBydate?contentId="+str(id)+"&contentType=page&fromDate="+fromDate+"&toDate="+toDate+"&type=total&period=week&timezone="+timeZone
    
    def content_attachmentViews_endpoint(self, id):
        return self.serverUrl + "/confluence/rest/confanalytics/1.0/content/attachments/views?contentId="+str(id)
    
    def userDetails_endpoint(self):
        return self.serverUrl + "/confluence/rest/confanalytics/1.0/rest/getUserDetails"
    
    def __init__(self, url):
        self.serverUrl = url
    
    def HTTPBasicAuth(self, id, pw):
        self.authParam = HTTPBasicAuth(id,pw)
        self.authType = "httpBasicAuth"

    ## raw api call
    # confluence rest api
    def getContentById(self, pageId):
        res = requests.get(url=self.content_endpoint(pageId), auth=self.authParam)
        return res.status_code, res.text
    
    def getContentStorage(self, pageId):
        res = requests.get(url=self.content_endpoint(pageId)+"?expand=body.storage", auth=self.authParam)
        return res.status_code, res.text
    
    def getChildPage(self, pageId):
        res = requests.get(url=self.child_content_endpoint(pageId), auth=self.authParam)
        return res.status_code, res.text
    
    def getUserById(self, userId):
        res = requests.get(url=self.user_endpoint(userId), auth=self.authParam)
        return res.status_code, res.text
    
    def createPage(self, title, spaceKey, content):
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = '''{"type":"page","title":"'''+title+'''","space":{"key":"'''+spaceKey+'''"},"body":{"storage":{"value":"'''+content+'''","representation":"storage"}}}'''
        res = requests.post(url=self.content_endpoint(""), auth=self.authParam, headers=header,data=payload.encode('utf-8'))
        return res.status_code, res.text
    
    # code, res = server.createChildPage(183730160, "test page 12345", "AABB", "empty page")
    def createChildPage(self, parentPageId, title, spaceKey, content):
        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = '''{"type":"page","title":"'''+title+'''","ancestors":[{"id":'''+str(parentPageId)+'''}],"space":{"key":"'''+spaceKey+'''"},"body":{"storage":{"value":"'''+content+'''","representation":"storage"}}}'''
        res = requests.post(url=self.content_endpoint(""), auth=self.authParam, headers=header,data=payload.encode('utf-8'))
        return res.status_code, res.text
    
    def updatePage(self, pageId, content, title=None, spaceKey=None, version=None):
        if title == None or spaceKey == None or version == None:
            code, res = self.getContentById(pageId)
            if code == requests.codes.ok:
                resDict = json.loads(str(res))
                if title == None:
                    if resDict.get('title') != None:
                        title = resDict.get('title')
                    else:
                        return requests.codes.bad, "title is empty"
                if spaceKey == None:
                    space = resDict.get('space')
                    if space != None:
                        if space.get('key') != None:
                            spaceKey = space.get('key')
                        else:
                            return requests.codes.bad, "spacekey is empty"
                    else:
                        return requests.codes.bad, "spacekey is empty"
                if version ==None:
                    value = resDict.get('version')
                    if value != None:
                        if value.get('number') != None:
                            # increase version 
                            version = value.get('number') + 1
                        else:
                            return requests.codes.bad, "version is empty"
                    else:
                        return requests.codes.bad, "version is empty"
            else:
                return requests.codes.bad, "title or spacekey or version is empty"


        header = {"Content-Type": "application/json; charset=utf-8"}
        payload = '''{"id":'''+str(pageId)+''',"type":"page","title":"'''+title+'''","space":{"key":"'''+spaceKey+'''"},"body":{"storage":{"value":"'''+content+'''","representation":"storage"}},"version":{"number":'''+str(version)+'''}}'''
        res = requests.put(url=self.content_endpoint(pageId), auth=self.authParam, headers=header,data=payload.encode('utf-8'))
        return res.status_code, res.text
    

    # analytics rest api
    def getPageViewsByUsers(self, pageId):
        res = requests.get(url=self.page_viewsByUser_endpoint(pageId),auth=self.authParam)
        return res.status_code, res.text
    
    def getUsersDetails(self, idList:list):
        payload = '''{"accountIds":["'''+ '","'.join(idList)+'''"],"ignoreIncreasedPrivacyMode":false}'''
        print(payload)
        # add host and origin to pass xsrf check
        host = self.serverUrl.replace("https://", "").repalce("http://", "")
        header = {"Content-Type": "application/json",
                  "X-Atlassian-Token":"no-check",
                  "Host":host,
                  "Origin":self.serverUrl,
                  "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
                  "accept": "application/json"}
        res = requests.post(url=self.userDetails_endpoint(),auth=self.authParam, data=payload, headers=header)
        return res.status_code, res.text
        pass
    
    def getPageViewsByDate(self, pageId, fromDate, toDate, timeZone):
        if fromDate == None or toDate == None or timeZone == None:
            return requests.codes.bad, ""
        res = requests.get(url=self.page_viewsByDate_endpoint(pageId, fromDate, toDate, timeZone),auth=self.authParam)
        return res.status_code, res.text
    
    ## utility============================================
    def getPageViews(self, pageId):
        # get viewsby user
        viewsByUser_status_code, viewsByUser_res_detail = self.getPageViewsByUsers(pageId)
        if viewsByUser_status_code == requests.codes.ok:
            viewsByUserDict = json.loads(str(viewsByUser_res_detail))
            index = 0
            for item in viewsByUserDict.get('viewsByUser'):
                userId = item.get('userId')
                if userId != None:
                    userName_status_code, userName_res_detail = self.getUserById(userId)
                    if userName_status_code == requests.codes.ok:
                        userInfoDict = json.loads(str(userName_res_detail))
                        userName = userInfoDict.get('displayName')
                        if userName != None:
                            viewsByUserDict['viewsByUser'][index]['userId'] = userName
                index = index + 1
            utils.saveTextFile(json.dumps(viewsByUserDict),"viewsByUser_"+str(pageId)+".json")
        
        # use userDetail to replace userid with displayname
        # viewsByUser_status_code, viewsByUser_res_detail = self.getPageViewsByUsers(pageId)
        # if viewsByUser_status_code == requests.codes.ok:
        #     viewsByUserDict = json.loads(str(viewsByUser_res_detail))
        #     userList = []
        #     index = 0
        #     for item in viewsByUserDict.get('viewsByUser'):
        #         userId = item.get('userId')
        #         if userId != None:
        #             userList.append(userId)
        #     userList = list(set(userList))
        #     code, detail = self.getUsersDetails(userList)
        

        # get viewsbyDate(from createdDate to now)               
        page_status_code, page_res_detail = self.getPage(pageId)
        if page_status_code == requests.codes.ok:
            pageDetailDict = json.loads(str(page_res_detail))
            fromDate = None
            toDate = None
            timeZone = None
            history = pageDetailDict.get('history')
            if history != None:
                createdDate = history.get('createdDate')
                if createdDate != None:
                    fromDate = createdDate[0:23]+"Z"
                    fromDate = str(fromDate).replace(':','%3A')
                    toDate = datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[0:23]+"Z"
                    toDate = toDate.replace(':', '%3A')
                    tz = strftime("%z", gmtime())
                    timeZone = "GMT"+tz[0:3]+":"+tz[3:]
                    timeZone = timeZone.replace('+', '%2B').replace(':','%3A')
                    viewsByDate_status_code, viewsByDate_res_detail = self.getPageViewsByDate(pageId, fromDate, toDate, timeZone)
                    utils.saveTextFile(viewsByDate_res_detail,"viewsByDate_"+str(pageId)+".json")
    

