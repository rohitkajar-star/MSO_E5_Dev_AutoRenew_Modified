# -*- coding: UTF-8 -*-

import requests as req
import json
import sys
import time
import os

# GitHub Secrets
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
        "refresh_token": refresh_token,
        "client_id": id,
        "client_secret": secret,
        "redirect_uri": "http://localhost:53682/"
    }

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

    with open(path, "r") as fo:
        refresh_token = fo.read().strip()

    localtime = time.asctime(time.localtime(time.time()))

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
        "https://graph.microsoft.com/v1.0/me/messages",
        "https://graph.microsoft.com/v1.0/me/mailFolders/inbox/messageRules",
        "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages/delta",
        "https://graph.microsoft.com/v1.0/me/drive/root/children",
        "https://api.powerbi.com/v1.0/myorg/apps",
        "https://graph.microsoft.com/v1.0/me/mailFolders",
        "https://graph.microsoft.com/v1.0/me/outlook/masterCategories"
    ]

    try:
        for i, url in enumerate(urls, start=1):
            r = req.get(url, headers=headers)

            print(f"API {i}: {r.status_code}")

            if r.status_code == 200:
                num1 += 1

        print("Success count:", num1)
        print("Run time:", localtime)

    except Exception as e:
        print("ERROR:", str(e))


for _ in range(5):
    main()
