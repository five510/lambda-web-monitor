import urllib.request
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def hander(event,context):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as res:
        body = res.read()
    return {}