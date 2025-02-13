import hashlib
import streamlit as st

class File_Integrity_Check:
    def __init__(self, content, file_hash, hash_method, is_file=True):
        self.content = content
        self.file_hash = file_hash
        self.hash_method = hash_method
        self.is_file = is_file  # To differentiate between file and text input

    def check_integrity(self):
        # Compute hash based on content (file or text)
        if self.is_file:
            # File mode: open the file in binary read mode
            with open(self.content, 'rb') as file:
                byte_data = file.read()
        else:
            # Text mode: use entered text
            byte_data = self.content.encode()

        # Choose hashing algorithm based on user selection
        if self.hash_method == 'MD5':
            hash_object = hashlib.md5(byte_data)
        elif self.hash_method == 'SHA-1':
            hash_object = hashlib.sha1(byte_data)
        elif self.hash_method == 'SHA-256':
            hash_object = hashlib.sha256(byte_data)
        elif self.hash_method == 'SHA-512':
            hash_object = hashlib.sha512(byte_data)

        current_file_hash = hash_object.hexdigest()

        if current_file_hash == self.file_hash:
            result = "Integrity Check Passed!! Content is good to use...."
        else:
            result = "Content is tampered, please delete or modify!!!!"

        return current_file_hash, result

# Streamlit UI code
def main():
    st.title("File Integrity Check")

    # First, add the radio button for selecting the option to enter text or upload a file
    option = st.radio("Choose an option", ["Enter Text", "Upload File"])

    # Initialize variables for uploaded file and entered text
    uploaded_file = None
    input_text = ""

    # Conditional rendering based on the selected option
    if option == "Enter Text":
        # Text area for entering text if the user selects "Enter Text"
        input_text = st.text_area("Enter text:", "")
        # Then, add the dropdown for selecting the hashing method
        hash_method = st.selectbox(
            "Select Hashing Method",
            ["MD5", "SHA-1", "SHA-256", "SHA-512"]
        )
        # Ask for the expected hash
        file_hash = st.text_input("Enter expected hash (use the correct hash for the selected method):")

    elif option == "Upload File":
        # Upload file via Streamlit file uploader
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt", "jpg", "png", "docx"])
        # Then, add the dropdown for selecting the hashing method
        hash_method = st.selectbox(
            "Select Hashing Method",
            ["MD5", "SHA-1", "SHA-256", "SHA-512"]
        )
        # Ask for the expected hash
        file_hash = st.text_input("Enter expected hash (use the correct hash for the selected method):")

    # Create a submit button
    submit_button = st.button("Check Integrity")

    if submit_button:
        if option == "Upload File":
            if uploaded_file and file_hash:
                # Save the uploaded file to a temporary location
                with open("temp_file", "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Perform file integrity check with selected hashing method
                file_int_check = File_Integrity_Check("temp_file", file_hash, hash_method, is_file=True)
                current_hash, result = file_int_check.check_integrity()

                # Show the current hash and result
                st.write("### Current File Hash:")
                st.code(current_hash)  # Display hash in a code block for readability
                st.write("### Integrity Check Result:")
                st.write(result)
            
            elif not uploaded_file:
                st.warning("Please upload a file to proceed.")
            
            elif not file_hash:
                st.warning("Please enter the expected file hash to proceed.")

        elif option == "Enter Text":
            if input_text and file_hash:
                # Perform integrity check for the entered text
                file_int_check = File_Integrity_Check(input_text, file_hash, hash_method, is_file=False)
                current_hash, result = file_int_check.check_integrity()

                # Show the current hash and result for the entered text
                st.write("### Current Text Hash:")
                st.code(current_hash)  # Display hash in a code block for readability
                st.write("### Integrity Check Result:")
                st.write(result)
            
            elif not input_text:
                st.warning("Please enter some text to proceed.")
            
            elif not file_hash:
                st.warning("Please enter the expected file hash to proceed.")

if __name__ == "__main__":
    main()
