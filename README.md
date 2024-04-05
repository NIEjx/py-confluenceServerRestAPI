# py-confluenceServerRestAPI
a python lib for accessing confluence server with rest api

- create, update, get contents
- get page views of content with confanalytics api <br>
your can access analytics for confluence data by using this api

Notice:
- rest/getUserDetails will return 403 because of the xsrf check, you can set host and origin to avoid it.

- be careful when updating the page which contains macro, you can refer to createRetroPage.py


