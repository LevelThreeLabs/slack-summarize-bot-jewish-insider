# test_proxy.py
import requests

username = "ljf8l07ggdti6ud"
password = "vuc52o4ph9vx6fu"
proxy = "rp.scrapegw.com:6060"
proxy_auth = f"{username}:{password}@{proxy}"

proxies = {
    "http": f"http://{proxy_auth}",
    "https": f"http://{proxy_auth}",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

url = "https://www.bloomberg.com/news/articles/2025-05-12/abu-dhabi-former-stanchart-dealmaker-sets-up-advisory-firm-elaeo"
r = requests.get(url, proxies=proxies, headers=headers)

print(r.status_code)
print(r.text[:1000])  # Print the first 1000 characters of the response
