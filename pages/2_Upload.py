import streamlit as st
import os
import db
import dataExtract

def save_uploaded_file(uploaded_file, save_path='uploads'):
    os.makedirs(save_path, exist_ok=True)
    file_path = os.path.join(save_path, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    """
    if not db.verifyLoginStatus():
        st.title(db.verifyLoginStatus())
        st.title("Please login.")
     """

    st.title("Receipt Uploader")

    uploaded_file = st.file_uploader("", type="jpg")

    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)
        st.write("")
        st.write("Classifying...")

        # Save the uploaded image
        saved_path = save_uploaded_file(uploaded_file)
        #st.write(f"Image saved at: {saved_path}")

        db.insertData(saved_path, 'test123@gmail.com')

        if st.button('Show Raw Text'):
            # Code to execute when the button is clicked
            st.write('Converted to Text')
            st.write(db.imgToText(saved_path))
            #db.addTrans(1,'1',1,'1',1)
        # You can perform additional tasks with the saved image path
        # For example, you can use a machine learning model to classify the image
if "user" not in st.experimental_get_query_params():
    st.experimental_set_query_params(user="no")
if st.experimental_get_query_params()["user"][0] == "no":
    st.title("Login to see this page")
else:
    main()

