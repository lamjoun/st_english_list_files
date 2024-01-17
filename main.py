import os
import time
import streamlit as st
from st_english_list_files_functions import save_uploaded_file, read_file, delete_all_files, delete_file, rename_file


# Directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploaded_files'


# Basic login
def login(username, password):
    correct_username = st.secrets["username"]
    correct_password = st.secrets["password"]
    return username == correct_username and password == correct_password

# Streamlit app layout
def main():
   # Initialize session state for login status
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    st.sidebar.title("Login/Logout")

    # User is not logged in
    if not st.session_state.logged_in:
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if login(username, password):
                st.session_state.logged_in = True
                #st.experimental_rerun()
                st.rerun()
            else:
                st.sidebar.error("Incorrect username or password")

    # User is logged in
    if st.session_state.logged_in:
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            #st.experimental_rerun()
            st.rerun()

    # File uploader
    files = os.listdir(UPLOAD_FOLDER)
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        uploaded_file_name = save_uploaded_file(UPLOAD_FOLDER,uploaded_file)
        st.sidebar.success("Saved file: {}".format(uploaded_file_name))
        files = os.listdir(UPLOAD_FOLDER)
        selected_file = st.sidebar.selectbox("Select a file", files, index=files.index(uploaded_file_name))
    else:
        if os.path.exists(UPLOAD_FOLDER):
            selected_file = st.sidebar.selectbox("Select a file", files)
    
    new_file_name = st.sidebar.text_input("New filename for selected file:", value=selected_file)          
          
    if new_file_name and new_file_name!=selected_file:
        selected_file_path = os.path.join(UPLOAD_FOLDER,selected_file)
        #
        #print(selected_file," ",new_file_name)
        #print('**********')
        #
        st.sidebar.write(new_file_name)
        success, message = rename_file(selected_file_path, new_file_name)
        if success:
            st.sidebar.success(message)
            files = os.listdir(UPLOAD_FOLDER)
            selected_file = new_file_name
            #st.experimental_rerun()
            st.rerun()
        else:
            st.sidebar.error(message)

    #========== Delete operation  =========== 
    if st.sidebar.button("Delete Selected File"):
        if delete_file(UPLOAD_FOLDER, selected_file):
            st.success(f"Deleted file: {selected_file}")
        else:
            st.error("File could not be deleted")
        #st.experimental_rerun()
        st.rerun()

    if st.sidebar.button("Delete All Files"):
        delete_all_files(UPLOAD_FOLDER)
        st.sidebar.success("All files deleted")
        #st.sidebar.experimental_rerun()
        st.rerun()
    #========== End Delete operation  ===========
        
    # Display file content
    if st.button("Show File Content"):
        if selected_file:
            file_path = os.path.join(UPLOAD_FOLDER, selected_file)
            content = read_file(file_path)
            st.write(content)


def main2():
    st.title("Append 'rrrrr' to Text")

    # Create a text input widget
    user_input = st.text_input("Enter some text",'ttttttttt')

    # Append 'rrrrr' to the user input
    modified_text = user_input + 'rrrrr'

    # Display the modified text
    if user_input:  # Only display after the user has entered something
        st.write("Your modified text: ", modified_text)


if __name__ == "__main__":
    main()
