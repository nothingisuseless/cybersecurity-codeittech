import streamlit as st
from Crypto.Cipher import AES, Blowfish
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from Crypto.Cipher import PKCS1_OAEP
import os

# Function to encrypt the file using AES-256
def encrypt_aes(file_path, password):
    iv = get_random_bytes(16)  # AES block size is 16 bytes
    key = (password.encode('utf-8')[:32]).ljust(32, b'\0')  # Ensure the key is 32 bytes (AES-256)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # Pad the data to make its length a multiple of AES block size
    padded_data = pad(file_data, AES.block_size)
    
    encrypted_data = cipher.encrypt(padded_data)
    
    encrypted_file_path = file_path + ".enc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(iv + encrypted_data)  # Store IV at the beginning of the file
    return encrypted_file_path

# Function to decrypt the file using AES-256
def decrypt_aes(file_path, password):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    iv = file_data[:16]  # The first 16 bytes are the IV
    encrypted_data = file_data[16:]
    
    key = (password.encode('utf-8')[:32]).ljust(32, b'\0')  # Ensure the key is 32 bytes (AES-256)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    
    decrypted_file_path = file_path.replace(".enc", "_decrypted")
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)
    return decrypted_file_path

# Function to encrypt the file using Blowfish
def encrypt_blowfish(file_path, password):
    key = password.encode('utf-8')[:56]  # Blowfish requires a key between 4 and 56 bytes
    cipher = Blowfish.new(key, Blowfish.MODE_CBC)
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # Pad the data to make its length a multiple of Blowfish block size
    padded_data = pad(file_data, Blowfish.block_size)
    
    encrypted_data = cipher.encrypt(padded_data)
    
    encrypted_file_path = file_path + ".bfenc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(cipher.iv + encrypted_data)  # Store IV at the beginning of the file
    return encrypted_file_path

# Function to decrypt the file using Blowfish
def decrypt_blowfish(file_path, password):
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    iv = file_data[:8]  # Blowfish block size is 8 bytes
    encrypted_data = file_data[8:]
    
    key = password.encode('utf-8')[:56]  # Blowfish key size between 4 and 56 bytes
    
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    
    # Decrypt and unpad the data
    decrypted_data = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
    
    decrypted_file_path = file_path.replace(".bfenc", "_decrypted")
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)
    return decrypted_file_path

# Function to encrypt the file using RSA (public key encryption)
def encrypt_rsa(file_path, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    encrypted_data = cipher.encrypt(file_data)
    
    encrypted_file_path = file_path + ".rsaenc"
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_data)
    return encrypted_file_path

# Function to decrypt the file using RSA (private key decryption)
def decrypt_rsa(file_path, private_key):
    with open(file_path, 'rb') as f:
        encrypted_data = f.read()
    
    cipher = PKCS1_OAEP.new(private_key)
    
    decrypted_data = cipher.decrypt(encrypted_data)
    
    decrypted_file_path = file_path.replace(".rsaenc", "_decrypted")
    with open(decrypted_file_path, 'wb') as f:
        f.write(decrypted_data)
    return decrypted_file_path

# Generate RSA keys
def generate_rsa_keys():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Streamlit app
def main():
    st.title("File Encryption and Decryption Tool")

    # Select the encryption algorithm
    option = st.selectbox("Select Operation", ["Encrypt File", "Decrypt File"])

    encryption_algorithm = st.selectbox("Choose Encryption Algorithm", ["AES-256", "Blowfish", "RSA"])

    password = st.text_input("Enter Encryption Key (Password):", type="password")
    
    # RSA keys generation (for demo purposes)
    private_key, public_key = generate_rsa_keys()
    
    if option == "Encrypt File":
        uploaded_file = st.file_uploader("Upload File to Encrypt", type=["txt", "jpg", "png", "pdf"])
        if uploaded_file and password:
            with open("temp_file", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if encryption_algorithm == "AES-256":
                if st.button("Encrypt File"):
                    encrypted_file = encrypt_aes("temp_file", password)
                    st.success(f"File successfully encrypted. Saved as: {encrypted_file}")
                    os.remove("temp_file")
            
            elif encryption_algorithm == "Blowfish":
                if st.button("Encrypt File"):
                    encrypted_file = encrypt_blowfish("temp_file", password)
                    st.success(f"File successfully encrypted. Saved as: {encrypted_file}")
                    os.remove("temp_file")
            
            elif encryption_algorithm == "RSA":
                if st.button("Encrypt File"):
                    # Encrypt using RSA with the public key
                    public_key_rsa = RSA.import_key(public_key)
                    encrypted_file = encrypt_rsa("temp_file", public_key_rsa)
                    st.success(f"File successfully encrypted. Saved as: {encrypted_file}")
                    os.remove("temp_file")
    
    elif option == "Decrypt File":
        uploaded_file = st.file_uploader("Upload Encrypted File", type=["enc", "bfenc", "rsaenc"])
        if uploaded_file and password:
            with open("temp_file.enc", "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            if encryption_algorithm == "AES-256":
                if st.button("Decrypt File"):
                    decrypted_file = decrypt_aes("temp_file.enc", password)
                    st.success(f"File successfully decrypted. Saved as: {decrypted_file}")
                    os.remove("temp_file.enc")
            
            elif encryption_algorithm == "Blowfish":
                if st.button("Decrypt File"):
                    decrypted_file = decrypt_blowfish("temp_file.enc", password)
                    st.success(f"File successfully decrypted. Saved as: {decrypted_file}")
                    os.remove("temp_file.enc")
            
            elif encryption_algorithm == "RSA":
                if st.button("Decrypt File"):
                    private_key_rsa = RSA.import_key(private_key)
                    decrypted_file = decrypt_rsa("temp_file.enc", private_key_rsa)
                    st.success(f"File successfully decrypted. Saved as: {decrypted_file}")
                    os.remove("temp_file.enc")

if __name__ == "__main__":
    main()
