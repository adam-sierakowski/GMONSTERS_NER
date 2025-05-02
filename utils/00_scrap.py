import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

BASE_URL = 'https://www.themodders.org/'
OUTPUT_DIR = 'themodders_forum_all'
os.makedirs(OUTPUT_DIR, exist_ok=True)

visited = set()
to_visit = {BASE_URL}

def is_valid_forum_link(href):
    return (
        href and
        ('/topic,' in href or '/index.php?topic=' in href) and
        'action=' not in href
    )

def extract_text_and_save(url, idx):
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        texts = soup.get_text(separator='\n')
        with open(f'{OUTPUT_DIR}/page_{idx}.txt', 'w', encoding='utf-8') as f:
            f.write(texts)
    except Exception as e:
        print(f'Error fetching {url}: {e}')

def main():
    idx = 0
    while to_visit:
        current = to_visit.pop()
        if current in visited:
            continue
        visited.add(current)

        try:
            resp = requests.get(current, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
        except:
            continue

        extract_text_and_save(current, idx)
        idx += 1

        for a in soup.find_all('a', href=True):
            href = urljoin(current, a['href'])
            if is_valid_forum_link(href):
                netloc = urlparse(href).netloc
                if 'themodders.org' in netloc:
                    to_visit.add(href)

        time.sleep(1)  # be polite

if __name__ == "__main__":
    main()

