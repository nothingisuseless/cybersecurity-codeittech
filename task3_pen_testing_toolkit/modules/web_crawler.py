import requests
from bs4 import BeautifulSoup

def crawl(url,st):
    response = requests.get(url)
    if response.status_code == 200:
        st.write(f"Successfully connected to {url}")
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            st.write(f"Found link: {link['href']}")
    else:
        st.write(f"Failed to connect to {url}")
