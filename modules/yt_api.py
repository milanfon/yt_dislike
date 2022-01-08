import requests

API_URL = "https://youtube.googleapis.com/youtube/v3/"

class YTApi:
    def __init__(self, client, api_key):
        self.client = client
        self.api_key = api_key
    
    def query(self, request, params):
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer "+self.client.token["access_token"]
        }
        params["key"] = self.api_key
        req = requests.get(url=API_URL+request, params=params, headers=headers)
        return req.json()

    def apiPut(self, request, params, data):
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer "+self.client.token["access_token"]
        }
        params["key"] = self.api_key
        req = requests.put(url=API_URL+request, params=params, json=data, headers=headers)
        return req.json()

    def showChannelVideos(self, channelID, maxResult = 5):
        if maxResult > 50:
            maxResult = 50
        request = "search"
        params = {
            "part": "snippet, id",
            "order": "date",
            "maxResults": maxResult,
            "channelId": channelID
        }
        return self.query(request, params)
        
    def myChannelInfo(self):
        p = {
            "part": "snippet,contentDetails,statistics",
            "mine": "true"
        }
        return self.query("channels", p)

    def getVideoStatistics(self, videoID):
        p = {
            "part": "statistics",
            "id": videoID
        }
        return self.query("videos", p)

    def getCommentsOnVideo(self, videoID):
        p = {
            "part": "snippet,id",
            "videoId": videoID,
            "maxResults": 1
        }
        return self.query("commentThreads", p)

    def getCommentByID(self, commentID):
        p = {
            "part": "snippet",
            "id": commentID
        }
        return self.query("comments", p)

    def updateComment(self, commentID, text):
        data = {
            "id": commentID,
            "snippet": {
                "textOriginal": text
            }
        }
        p = {
            "part": "snippet"
        }
        return self.apiPut("comments", p, data)

    def getVideoData(self, videoID):
        p = {
            "part": "snippet",
            "id": videoID
        }
        return self.query("videos", p)

    def changeVideoTitle(self, videoID, text):
        p_data = self.getVideoData(videoID)
        snippet = p_data["items"][0]["snippet"]
        snippet["title"] = text
        data = {
            "id": videoID,
            "snippet": snippet
        }
        p = {
            "part": "snippet"
        }
        return self.apiPut("videos",p,data)