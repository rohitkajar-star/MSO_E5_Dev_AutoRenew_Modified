# -*- coding: UTF-8 -*-

import os

id = os.environ.get("CONFIG_ID")
secret = os.environ.get("CONFIG_KEY")

print("CLIENT ID LENGTH:", len(id) if id else 0)
print("CLIENT ID REPR:", repr(id))

print("SECRET LENGTH:", len(secret) if secret else 0)
print("SECRET REPR:", repr(secret))

print("CLIENT ID ASCII:")
for c in id:
    print(ord(c), end=" ")

print("\nSECRET ASCII:")
for c in secret:
    print(ord(c), end=" ")
