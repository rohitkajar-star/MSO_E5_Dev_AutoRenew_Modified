# -*- coding: UTF-8 -*-

import requests as req
import json
import sys
import time
import os

id = os.environ.get("CONFIG_ID")
secret = os.environ.get("CONFIG_KEY")

path = sys.path[0] + "/Secret.txt"
num1 = 0


def gettoken(refresh_token):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token.strip(),
        "client_id": id.strip(),
        "client_secret": secret.strip(),
        "redirect_uri": "http://localhost:53682/"
    }

    print("========== DEBUG ==========")
    print("CLIENT ID:", id)
    print("CLIENT ID LENGTH:", len(id))
    print("SECRET EXISTS:", secret is not None)

    if secret:
        print("SECRET LENGTH:", len(secret))
        print("SECRET PREFIX:", secret[:5])
        print("SECRET LAST 5:", secret[-5:])

    print("REFRESH TOKEN LENGTH:", len(refresh_token))
    print("REFRESH TOKEN PREFIX:", refresh_token[:20])
    print("REDIRECT URI:", data["redirect_uri"])
    print("===========================")

    html = req.post(
        "https://login.microsoftonline.com/common/oauth2/v2.0/token",
        data=data,
        headers=headers
    )

    print("========== TOKEN RESPONSE ==========")
    print("Status:", html.status_code)
    print("Response:", html.text)
    print("====================================")

    jsontxt = json.loads(html.text)

    if "refresh_token" not in jsontxt:
        raise Exception(str(jsontxt))

    refresh_token = jsontxt["refresh_token"]
    access_token = jsontxt["access_token"]

    with open(path, "w") as f:
        f.write(refresh_token)

    return access_token


def main():
    global num1

    with open(path, "r") as f:
        refresh_token = f.read().strip()

    access_token = gettoken(refresh_token)

    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }

    urls = [
        "https://graph.microsoft.com/v1.0/me/drive/root",
        "https://graph.microsoft.com/v1.0/me/drive",
        "https://graph.microsoft.com/v1.0/drive/root",
        "https://graph.microsoft.com/v1.0/users",
        "https://graph.microsoft.com/v1.0/me/messages"
    ]

    for url in urls:
        try:
            r = req.get(url, headers=headers)
            print(url, r.status_code)

            if r.status_code == 200:
                num1 += 1

        except Exception as e:
            print("API ERROR:", str(e))

    print("Success count:", num1)
    print("Run time:", time.asctime())


if __name__ == "__main__":
    main()
