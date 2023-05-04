import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import os

# st.config.set_option("server.maxUploadSize", 20)

# uploaded_file = None
# file_in_server = ''
# split_option = 1
# col1, col2 = None, None


def split_file(pdfname: str, 
               option: str,
               param: int = 1):
    import pypdf

    with open(pdfname, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfFileReader(pdf_file)

        N = len(pdf_reader.pages)
        st.write(f"Processing {N} pages...")
        # st.write(f'PDF Metadata is {pdf_reader.metadata}') 

        file_stats = os.stat(pdfname)

        global split_strings

        if option == split_strings[0]:
            st.write('User chose option 1')
            n_splits = param
        elif option == split_strings[1]:
            st.write('User chose option 2')
            n_splits = int(np.ceil(file_stats.st_size/param))
            st.write("n_splits:", n_splits)
            # pages = [param] * N//param + [N % param]

        pages = [N//n_splits]* (n_splits)
        pages[0] += N % n_splits
        pages = list(filter(lambda num: num != 0, pages))
    
        return pages
        

    return []

from typing import List
def serve_files(source: str,
                pages: List[int]):

    st.write(f'Serving splits for {source}')
    # Fake content, for now!
    for i, p in enumerate(pages):
        st.download_button(label=f'File {i}, size {p}.', 
                        data=f"text_contents {i}: number of pages = {p}",
                        file_name=f"file_{i}.txt", 
                        mime='text/plain')

    # TODO: split file to multiple PDFs to serve. OR, even better, stream pages
    # from the source PDF in each download_button.


#--- Layout setup ---
# del st.session_state['file_uploaded']

col1, col2 = st.columns(2)
uploaded_file = col1.file_uploader("Choose a file")

split_strings = ['Split evenly','Split by size']
split_option = col2.selectbox(
    'How many splits?', split_strings
    )
split_param = 1

if split_option == split_strings[0]:
    split_param = col2.selectbox('Number of files',[1,2,3])
elif split_option == split_strings[1]:
    n_size = col2.number_input('File size (MB), roughly:',value=5)
    split_param = int(n_size*1024*1024)
else:
    pass

# if ('file_uploaded' in st.session_state):
    # st.write(st.session_state.file_uploaded)

if ('file_uploaded' not in st.session_state) or \
    st.session_state.file_uploaded['successful'] == False:

    # st.session_state['successful_upload'] = False
    if uploaded_file is not None and uploaded_file.type=='application/pdf':
        file_in_server = os.path.join(".",uploaded_file.name)
        with open(file_in_server,"wb") as f: 
            f.write(uploaded_file.getbuffer())         
            st.success(f"Saved File, {uploaded_file.size} bytes!")
            # successful_upload = True
            st.session_state['file_uploaded'] = \
                {'successful':True, 
                 'filename': file_in_server,
                 'pages': None}
    else:
        st.session_state['file_uploaded'] = {'successful':False, 
                                             'filename': None,
                                             'pages': None}

if st.session_state.file_uploaded['successful']:
    # if not st.session_state.file_uploaded['pages']:
    if st.button('Process'):
        file_pages = split_file( st.session_state.file_uploaded['filename'],
                                split_option,
                                split_param)

        if file_pages:
            st.session_state.file_uploaded['pages'] = file_pages
    
    if st.session_state.file_uploaded['pages']:
        serve_files(st.session_state.file_uploaded['filename'], 
                st.session_state.file_uploaded['pages'])

# else:
    # st.session_state['successful_upload'] = False

