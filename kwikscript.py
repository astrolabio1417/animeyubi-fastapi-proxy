import requests
import re


USER_AGENT = "Googlebot/2.1 (+http://www.google.com/bot.html)"


def get_host_url(url):
    return re.match(r"https?://[^/]+", url).group(0)


def get_string(content, s1, s2):
    CHARACTER_MAP = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    slice_2 = CHARACTER_MAP[0:s2]

    acc = 0
    for n, i in enumerate(content[::-1]):
        acc += int(i if i.isdigit() else 0) * s1**n

    k = ""
    while acc > 0:
        k = slice_2[int(acc % s2)] + k
        acc = (acc - (acc % s2)) / s2

    return k or "0"


def decrypt(full_string, key, v1, v2):
    v1, v2 = int(v1), int(v2)
    r = ""
    i = 0
    while i < len(full_string):
        s = ""
        while full_string[i] != key[v2]:
            s += full_string[i]
            i += 1
        j = 0
        while j < len(key):
            s = s.replace(key[j], str(j))
            j += 1
        r += chr(int(get_string(s, v2, 10)) - v1)
        i += 1
    return r


def parser(res):
    full_key, key, v1, v2 = re.search(
        r'\("(\w+)",\d+,"(\w+)",(\d+),(\d+),\d+\)', res.text
    ).groups()
    decrypted = decrypt(full_key, key, v1, v2)
    kwik_url = re.search(r'action="(.+?)"', decrypted).group(1)
    token = re.search(r'value="(.+?)"', decrypted).group(1)

    return (token, kwik_url)


def get_video(url):
    host = get_host_url(url)
    headers = {"referer": f"{host}/", "origin": host, "user-agent": USER_AGENT}

    session = requests.Session()

    f1 = session.get(url, headers=headers)
    key, url = parser(f1)

    f2 = session.post(
        url,
        data={"_token": key},
        headers={"Referer": url, "user-agent": USER_AGENT},
        allow_redirects=False,
    )

    return f2.headers.get("Location")
