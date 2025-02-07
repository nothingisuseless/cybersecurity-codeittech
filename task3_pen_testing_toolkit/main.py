import sys
from modules.port_scanner import scan_target
from modules.brute_forcer import brute_force_ssh
from modules.web_crawler import crawl
from utils.helpers import parse_arguments

def main():
    args = parse_arguments()

    if args.module == "port_scanner":
        target_ip = args.target
        ports = range(1, 65535)
        print(f"Scanning {target_ip} for open ports...")
        scan_target(target_ip, ports)

    elif args.module == "brute_forcer":
        target_ip = args.target
        username = input("Enter SSH username: ")
        print(f"Attempting brute force on {target_ip}...")
        passwords = ['password1', '1234', 'letmein']  # Password list for testing
        brute_force_ssh(target_ip, username, passwords)

    elif args.module == "web_crawler":
        target_url = args.target
        print(f"Crawling website {target_url}...")
        crawl(target_url)
    else:
        print("Invalid module selected. Choose from: port_scanner, brute_forcer, web_crawler.")
        sys.exit(1)

if __name__ == "__main__":
    main()
