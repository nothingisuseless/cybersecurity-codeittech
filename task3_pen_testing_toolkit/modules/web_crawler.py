import requests
from bs4 import BeautifulSoup

def crawl(url):
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Successfully connected to {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            print(f"Found link: {link['href']}")
    else:
        print(f"Failed to connect to {url}")

if __name__ == '__main__':
    target_url = input("Enter target URL: ")
    crawl(target_url)
