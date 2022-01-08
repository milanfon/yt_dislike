import json
import requests
import urllib

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
VALIDATE_URL = "https://www.googleapis.com/oauth2/v3/tokeninfo"
REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"

class AuthClient:
    token = None

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def save_token(self):
        f = open("token.json","w")
        f.write(json.dumps(self.token))
        f.close()

    def load_token(self):
        f = open("token.json", "r")
        self.token = json.loads(f.read())

    def show_auth_code_uri(self):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "scope": "https://www.googleapis.com/auth/youtube.force-ssl",
            "include_granted_scopes": "true",
            "state": "pass-through value",
            "redirect_uri": REDIRECT_URI,
            "access_type": "offline"
        }
        auth_uri = AUTH_URL+"?"+urllib.parse.urlencode(params)
        print(auth_uri)

    def request_token(self, auth_code):
        token = requests.post(url=TOKEN_URL, json={
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": REDIRECT_URI
        })
        return token.json()

    def refresh_token(self):
        ref_token = requests.post(url=TOKEN_URL,json={
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.token["refresh_token"]
        })
        t = ref_token.json()
        self.token["access_token"] = t["access_token"]
        self.token["expires_in"] = t["expires_in"]
        self.save_token()

    def validate_token(self):
        resp = requests.get(url=VALIDATE_URL+"?access_token="+self.token["access_token"])
        val = resp.json()
        if "expires_in" in val:
            if int(val["expires_in"]) > 100:
                return True
        return False

    def auth_user(self):
        print("Přejďěte na následující adresu a zkopírujte kód:")
        self.show_auth_code_uri()
        print("Zde vložte kód:")
        auth_code = input()
        t = self.request_token(auth_code)
        self.token = t
        self.save_token()