import requests
from bs4 import BeautifulSoup

proxy_user = "ljf8l07ggdti6ud"
proxy_pass = "vuc52o4ph9vx6fu"
proxy_host = "rp.scrapegw.com:6060"

proxies = {
    "http": f"http://{proxy_user}:{proxy_pass}@{proxy_host}",
    "https": f"http://{proxy_user}:{proxy_pass}@{proxy_host}"
}

url = "http://ip-api.com/json"

try:
    response = requests.get(url, proxies=proxies, timeout=20)
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup.title.string)
except Exception as e:
    print("Failed:", e)
