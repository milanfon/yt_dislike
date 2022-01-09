import sys
import getopt as go
from modules.dbcontroller import localDB
import msvcrt

DB_FILE = "db/db.sqlite"

def main(argv):
    try:
        opts, args = go.getopt(argv, "hla:r:",["list","add-video=", "remove-video="])
    except go.GetoptError:
        print("Unknown arguments!")
        sys.exit(2)
    global db
    db = localDB(DB_FILE)
    for opt, arg in opts:
        if opt == "-h":
            print("-l,--list\tList videos")
        elif opt in ("-l", "--list"):
            listVids()
        elif opt in ("-a", "--add-video"):
            addTrackedVideo(arg)
        elif opt in ("-r", "--remove-video"):
            db.untrackVideo(arg)

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

def invalidInput() -> None:
    print("Invalid input!")
    sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])