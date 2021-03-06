import sys
import getopt as go
from modules.dbcontroller import localDB
import msvcrt
import requests

API_URL = "https://youtube.googleapis.com/youtube/v3/"
API_KEY = "" # Insert your own API key
DB_FILE = "db/db.sqlite"

def main(argv):
    try:
        opts, args = go.getopt(argv, "hla:r:c:v:",["list","add-video=", "remove-video=", "get-comment=", "video-comments="])
    except go.GetoptError:
        print("Unknown arguments!")
        sys.exit(2)
    global db
    db = localDB(DB_FILE)
    for opt, arg in opts:
        if opt == "-h":
            showHelp()
        elif opt in ("-l", "--list"):
            listVids()
        elif opt in ("-a", "--add-video"):
            addTrackedVideo(arg)
        elif opt in ("-r", "--remove-video"):
            db.untrackVideo(arg)
        elif opt in ("-c", "--get-comment"):
            print(getCommentByID(arg))
        elif opt in ("-v", "--video-comments"):
            print(getCommentsOnVideo(arg))

def showHelp() -> None:
    print("-l,--list=\tList videos")
    print("-a,--add-video=\tTrack video <Video ID>")
    print("-r,--remove-video=\tUntrack video <Video ID>")
    print("-c,--get-comment=\tGet comment by ID <Comment ID>")
    print("-v,--video-comments=\tGet last comment on video <Video ID>")

def listVids() -> None:
    videos = db.getTrackedVideos()["videos"]
    print("Video ID\tAction comment\tAction title\tComment ID")
    print("================================================================")
    for video in videos:
        print("{}\t{}\t\t{}\t\t{}".format(video["videoID"], video["action_comment"], video["action_title"], video["conf_comment_id"]))

def addTrackedVideo(videoID):
    print("Do comment action? [y/n]")
    k = msvcrt.getch()
    ac = 0
    cc = None
    if k in (b'y', b'Y'):
        ac = 1
        print("Insert comment ID:")
        cc = input()
    print("Do title action? [y/n]")
    at = 0
    ct = None
    k = msvcrt.getch()
    if k in (b'y', b'Y'):
        at = 1
        print("Insert title format:")
        ct = input()
    db.trackVideo(videoID, ac, at, cc, ct)

def apiQuery(request, params):
    headers = {
        "Accept": "application/json"
    }
    params["key"] = API_KEY
    req = requests.get(url=API_URL+request, params=params, headers=headers)
    return req.json()

def getCommentsOnVideo(videoID):
    p = {
        "part": "snippet,id",
        "videoId": videoID,
        "maxResults": 1
    }
    return apiQuery("commentThreads", p)

def getCommentByID(commentID):
    p = {
        "part": "snippet",
        "id": commentID
    }
    return apiQuery("comments", p)

def invalidInput() -> None:
    print("Invalid input!")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])