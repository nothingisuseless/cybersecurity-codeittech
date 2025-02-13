import streamlit as st
from modules.port_scanner import scan_target
from modules.brute_forcer import brute_force_ssh
from modules.web_crawler import crawl

# Streamlit app
def main():
    st.title("Security Tools")

    # Select module
    option = st.selectbox(
        "Choose an option",
        ["Port Scanner", "Brute Force SSH", "Web Crawler"]
    )

    # If the user selects "Port Scanner"
    if option == "Port Scanner":
        target_ip = st.text_input("Enter Target IP Address:")
        if target_ip:
            if st.button("Start Port Scan"):
                st.write(f"Scanning {target_ip} for open ports...")
                ports = range(1, 1024)
                lis = scan_target(target_ip, ports)
                st.write("\n\n\n".join([i for i in lis]))
                st.write("Scanning has been completed!!!")
                exit(0)
                #print(lis)
                

    # If the user selects "Brute Force SSH"
    elif option == "Brute Force SSH":
        target_ip = st.text_input("Enter Target IP Address:")
        username = st.text_input("Enter SSH Username:")
        if target_ip and username:
            passwords = ['password1', '1234', 'letmein']  # Password list for testing
            if st.button("Start Brute Force Attack"):
                st.write(f"Attempting brute force on {target_ip}...")
                brute_force_ssh(target_ip, username, passwords)

    # If the user selects "Web Crawler"
    elif option == "Web Crawler":
        target_url = st.text_input("Enter Target URL:")
        if target_url:
            if st.button("Start Crawling"):
                st.write(f"Crawling website {target_url}...")
                crawl(target_url,st)

if __name__ == "__main__":
    main()
