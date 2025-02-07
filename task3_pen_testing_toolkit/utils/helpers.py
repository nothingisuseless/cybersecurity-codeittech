import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Penetration Testing Toolkit")
    parser.add_argument("-m", "--module", required=True, help="Module to run: port_scanner, brute_forcer, etc.")
    parser.add_argument("-t", "--target", required=True, help="Target IP/URL")
    return parser.parse_args()
