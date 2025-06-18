import os
import time
import json
import random
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import subprocess

# Load environment variables if needed
load_dotenv()

# Configuration
seed_urls = ['https://kda-official.fandom.com/wiki/K/DA']
visited = set()
scraped_data = []
OUTPUT_FILE = 'scraped_data.json'

# OVERRIDE robots.txt — only for ethical testing
OVERRIDE_ROBOTS = True  # ⚠️ Set to False in production

# Rotating user agents
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/126.0",
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://www.google.com',
    }

# Default proxy (Tor)
TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Skip robots.txt if override is enabled
def is_allowed_by_robots(url):
    if OVERRIDE_ROBOTS:
        print(f"⚠️ Skipping robots.txt check for {url}")
        return True
    # If not overridden, check robots.txt (not used here)
    return True

def ask_llm_if_relevant(html, url):
        return True

def extract_clean_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    content = []

    toc = soup.find('div', class_='toc')  # Table of contents block
    if not toc:
        print("No TOC found; scraping all content.")
        return extract_all_paragraphs(soup)

    # Get section anchors from TOC
    section_ids = [a['href'][1:] for a in toc.find_all('a', href=True) if a['href'].startswith('#')]

    for sec_id in section_ids:
        section_header = soup.find(id=sec_id)
        if not section_header:
            continue

        section_title = section_header.get_text(strip=True)
        section_content = {"section": section_title, "paragraphs": [], "images": []}

        # Collect content until next header of same level
        for sibling in section_header.find_all_next():
            if sibling.name and sibling.name.startswith('h') and sibling.name <= section_header.name:
                break
            if sibling.name == 'p':
                text = sibling.get_text(strip=True)
                if text:
                    section_content["paragraphs"].append(text)
            if sibling.name == 'img':
                src = sibling.get('src')
                alt = sibling.get('alt') or sibling.get('title')
                if src:
                    section_content["images"].append({"src": src, "alt": alt or ""})

        if section_content["paragraphs"] or section_content["images"]:
            content.append(section_content)

    return {
        "title": soup.title.string.strip() if soup.title else "",
        "sections": content
    }

def extract_all_paragraphs(soup):
    """Fallback: Extract all content if TOC not found."""
    paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
    images = [{"src": img.get('src'), "alt": img.get('alt') or ""} for img in soup.find_all('img') if img.get('src')]
    return {
        "title": soup.title.string.strip() if soup.title else "",
        "paragraphs": paragraphs,
        "images": images,
    }


def crawl(url, depth=1, max_depth=2):
    print(f"[Crawling depth {depth}] Visiting: {url}")
    if url in visited or depth > max_depth:
        return
    visited.add(url)

    if not is_allowed_by_robots(url):
        return

    # Choose headers and proxy
    headers = get_headers()
    proxies = None if 'wikipedia.org' in url else TOR_PROXY

    try:
        response = requests.get(url, headers=headers, timeout=10, proxies=proxies)
        if response.status_code != 200:
            print(f"Failed to fetch {url} - Status: {response.status_code}")
            return

        html = response.text
        if not ask_llm_if_relevant(html, url):
            print(f"Skipped (not relevant): {url}")
            return

        print(f"Scraping: {url}")
        content = extract_clean_content(html)
        scraped_data.append({"url": url, **content})

        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a', href=True):
            child_url = urljoin(url, link['href'])
            if urlparse(child_url).netloc == urlparse(url).netloc:
                crawl(child_url, depth + 1, max_depth)

        time.sleep(random.uniform(2.5, 5.0))  # Polite delay

    except Exception as e:
        print(f"Error crawling {url}: {e}")

def main():
    if OVERRIDE_ROBOTS:
        print("⚠️  ROBOTS.TXT OVERRIDE IS ENABLED — TEST MODE ONLY ⚠️")
    for seed in seed_urls:
        crawl(seed)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(scraped_data, f, indent=2, ensure_ascii=False)

if __name__ == '__main__':
    main()
