import os
import PyPDF2
import shutil
from docx import Document


def ensure_folder_exists(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        
# Function to save uploaded files
def save_uploaded_file(i_UPLOAD_FOLDER, uploaded_file):
    if not os.path.exists(i_UPLOAD_FOLDER):
        os.makedirs(i_UPLOAD_FOLDER)
    with open(os.path.join(i_UPLOAD_FOLDER, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return (uploaded_file.name)

# Function to read file content
def read_file(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        with open(file_path, "r") as file:
            return file.read()
    elif ext == ".pdf":
        content = ""
        with open(file_path, "rb") as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in range(len(pdf_reader.pages)):
                content += pdf_reader.pages[page].extract_text()
        return content
    elif ext == ".docx":
        content = ""
        doc = Document(file_path)
        for para in doc.paragraphs:
            content += para.text + '\n'
        return content
    else:
        return "Unsupported file format"

def delete_file(i_UPLOAD_FOLDER,file_name):
    file_path = os.path.join(i_UPLOAD_FOLDER, file_name)
    if os.path.exists(file_path):
        os.remove(file_path)
        return True
    return False

def delete_all_files(i_UPLOAD_FOLDER):
    if os.path.exists(i_UPLOAD_FOLDER):
        shutil.rmtree(i_UPLOAD_FOLDER)
        os.makedirs(i_UPLOAD_FOLDER)

def rename_file(original_path, new_name):
    if not os.path.exists(original_path):
        return False, "Original file does not exist."

    new_path = os.path.join(os.path.dirname(original_path), new_name)
    if os.path.exists(new_path):
        return False, "File with the new name already exists."

    os.rename(original_path, new_path)
    return True, "File renamed successfully."

# Rest of your app code


