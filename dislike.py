from os.path import exists
from modules.auth import AuthClient
from modules.dbcontroller import localDB
from modules.yt_api import YTApi

API_KEY = ""
CLIENT_ID = ""
CLIENT_SECRET = ""
DB_FILE = "db/db.sqlite"

def mainLoop(videos, api, db):
    for video in videos:
        id = video["videoID"]

        # Cena 1 jednotka
        stats = api.getVideoStatistics(id)["items"][0]["statistics"]
        db.saveVideoCache(id, stats)

        dislikeCount = stats["dislikeCount"]

        if video["action_comment"]: # Cena 50 jednotek
            comment = "Toto video má {} disliků".format(dislikeCount)
            api.updateComment(video["conf_comment_id"], comment)

        if video["action_title"]: # Cena 51 jednotek
            title = video["conf_title_format"] % dislikeCount
            api.changeVideoTitle(id, title)

if __name__ == "__main__":
    auth = AuthClient(CLIENT_ID, CLIENT_SECRET)

    if not exists("token.json"):
        auth.auth_user()

    else:
        auth.load_token()
        if not auth.validate_token():
            auth.refresh_token()

    if auth.token is None:
        print("Autorizace selhala!")
        exit()
    
    api = YTApi(auth, API_KEY)
    db = localDB(DB_FILE)

    if(auth.validate_token()):
        print("Konám!")
        videos = db.getTrackedVideos()["videos"]
        mainLoop(videos, api, db)
    else:
        auth.refresh_token()