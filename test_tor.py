import requests

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

ip = requests.get("http://httpbin.org/ip", proxies=proxies).json()
print("Your IP through Tor is:", ip)

