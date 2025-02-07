# Penetration Testing Toolkit

## Description
This toolkit includes various penetration testing modules such as port scanning, brute-forcing, and web crawling. Each module can be run individually, and the toolkit is designed to be easily extendable.

## Modules
1. **Port Scanner**
   - Scans open ports on a target system.
   
2. **Brute Forcer**
   - Attempts to brute-force login credentials for SSH.

3. **Web Crawler**
   - Crawls a website and extracts links from the homepage.

## Usage
```bash
python main.py -m port_scanner -t <target_ip>
python main.py -m brute_forcer -t <target_ip>
python main.py -m web_crawler -t <target_url>