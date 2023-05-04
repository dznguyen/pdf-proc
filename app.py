import streamlit as st
import pandas as pd
from io import StringIO
import os

# st.config.set_option("server.maxUploadSize", 20)

# uploaded_file = None
# file_in_server = ''
# split_option = 1
# col1, col2 = None, None

# def setup_layout():
# global uploaded_file
# global split_option
# global col1, col2 

def split_file(pdfname: str, n: int):
    import PyPDF2

    with open(pdfname, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfFileReader(pdf_file)

        N = len(pdf_reader.pages)
        sizes = [N//split_option]* (split_option)
        sizes[0] += N % split_option

        sizes = list(filter(lambda num: num != 0, sizes))
    
        # st.write(f'Number of Pages in PDF File is {pdf_reader.getNumPages()}')
        # st.write(f'Number of Pages in PDF File is {N}') 

        st.write(f'PDF Metadata is {pdf_reader.documentInfo}')
        st.write(f'PDF will be split into files with page sizes = {sizes}') 
        # print(f'PDF File Author is {pdf_reader.documentInfo["/Author"]}')
        # print(f'PDF File Creator is {pdf_reader.documentInfo["/Creator"]}')

        # import PyPDF2

        # with open(file_in_server, 'rb') as pdf_file:
        #     pdf_reader = PyPDF2.PdfFileReader(pdf_file)
        #     # st.write(f'Number of Pages in PDF File is {pdf_reader.getNumPages()}')
        #     st.write(f'Number of Pages in PDF File is {len(pdf_reader.pages)}') 
        #     st.write(f'PDF Metadata is {pdf_reader.documentInfo}')
        #     # print(f'PDF File Author is {pdf_reader.documentInfo["/Author"]}')
        #     # print(f'PDF File Creator is {pdf_reader.documentInfo["/Creator"]}')
    
    # TODO: split_file returns a list of files, for user to download.

    return []

#--- Layout setup ---

col1, col2 = st.columns(2)
uploaded_file = col1.file_uploader("Choose a file")
split_option = col2.selectbox(
    'How many splits?',
    (1, 2, 3))


successful_upload = False
if uploaded_file is not None and uploaded_file.type=='application/pdf':
    st.write(uploaded_file.name)
    st.write(uploaded_file.type)
    st.write(uploaded_file.size)

    file_in_server = os.path.join(".",uploaded_file.name)
    with open(file_in_server,"wb") as f: 
        f.write(uploaded_file.getbuffer())         
        st.success("Saved File")
        successful_upload = True

# st.write(successful_upload, uploaded_file)
if successful_upload:  
    if st.button('Process'):
        st.write('Button Clicked!')
        files_to_download = split_file(file_in_server ,split_option)

