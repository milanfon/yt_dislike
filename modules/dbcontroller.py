import json
import sqlite3
from datetime import datetime

class localDB:
    def __init__(self, dbFile) -> None:
        self.con = sqlite3.connect(dbFile)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()

    def __del__(self) -> None:
        self.con.close()

    @staticmethod
    def row_to_dict(row) -> dict:
        return dict(zip(row.keys(),row))

    def getChannelList(self) -> dict:
        ex = self.cur.execute("SELECT * FROM channels")
        rows = []
        for row in ex:
            rows.append(self.row_to_dict(row))
        return {"channels": rows}

    def getTrackedVideos(self) -> dict:
        ex = self.cur.execute("SELECT * FROM tracked_videos")
        rows = []
        for row in ex:
            rows.append(self.row_to_dict(row))
        return {"videos": rows}

    def saveVideoCache(self, videoID, stats) -> None:
        now = datetime.now()
        self.cur.execute('''INSERT OR REPLACE INTO video_cache (videoID, data, updated) 
        VALUES (:id, :data, :updated)''', {
            "id": videoID,
            "data": json.dumps(stats),
            "updated": now.strftime("%d/%m/%Y %H:%M:%S")
        })
        self.con.commit()

    def trackVideo(self, videoID, action_comment, action_title, conf_comment, conf_title) -> None:
        self.cur.execute('''INSERT INTO tracked_videos (videoID, action_comment, action_title, conf_title_format, conf_comment_id)
        VALUES (:id, :ac, :at, :cc, :ct)''', {
            "id": videoID,
            "ac": action_comment,
            "at": action_title,
            "cc": conf_comment,
            "ct": conf_title
        })
        self.con.commit()