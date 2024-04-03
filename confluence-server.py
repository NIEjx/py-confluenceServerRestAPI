import requests
from requests.auth import HTTPBasicAuth
import json

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
    
    def content_history_endpoint(self, id):
        return self.content_endpoint(id) + "/history"
    
    def page_viewsByUser_endpoint(self, id):
        return self.serverUrl + "/confluence/rest/confanalytics/1.0/content/viewsByUser?contentId="+str(id)+"&contentType=page"

    def page_viewsByDate_endpoint(self, id, fromDate, toDate, timeZone):
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
    def