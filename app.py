import streamlit as st
import os
import zipfile
import shutil
from io import BytesIO

# Function to rename files
def rename_file(file, new_name, to_replace_with):
    if to_replace_with in file:
        new_filename = file.replace(to_replace_with, new_name)
        return new_filename
    return file

# Streamlit app
def main():
    st.title("File Renaming Tool Inside Zip")
    
    # Input for new name and the name to replace
    new_name = st.text_input("Enter the new name (e.g., Piyush49): ")
    to_replace_with = st.text_input("Enter the name to replace (e.g., Durvesh20): ")
    
    # File uploader for zip files
    zip_file = st.file_uploader("Upload a zip file:", type=["zip"])
    
    if zip_file is not None and new_name and to_replace_with:
        # Create a temporary directory to extract files
        extract_dir = 'extracted_files'
        if not os.path.exists(extract_dir):
            os.makedirs(extract_dir)

        # Extract the zip file
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)
            st.success("Files extracted successfully.")
        
        # Rename files after extraction
        renamed_files = []
        for root, dirs, files in os.walk(extract_dir):
            for file in files:
                old_file_path = os.path.join(root, file)
                new_filename = rename_file(file, new_name, to_replace_with)
                new_file_path = os.path.join(root, new_filename)
                
                if old_file_path != new_file_path:
                    os.rename(old_file_path, new_file_path)
                    renamed_files.append((new_file_path, new_filename))
        
        # Display renamed files with individual download buttons
        if renamed_files:
            st.write("Renamed files:")
            for file_path, filename in renamed_files:
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                st.download_button(
                    label=f"Download {filename}",
                    data=file_data,
                    file_name=filename,
                    mime="application/octet-stream"
                )
        
        # Create a new zip file for renamed files
        new_zip_io = BytesIO()
        with zipfile.ZipFile(new_zip_io, 'w') as new_zip:
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, extract_dir)
                    new_zip.write(file_path, arcname)
        
        # Clean up extracted files
        shutil.rmtree(extract_dir)
        
        # Allow the user to download the renamed zip file
        st.download_button(
            label="Download renamed zip",
            data=new_zip_io.getvalue(),
            file_name="renamed_files.zip",
            mime="application/zip"
        )

if __name__ == "__main__":
    main()
