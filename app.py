import streamlit as st
import pandas as pd
import numpy as np
from io import StringIO
import os

# st.config.set_option("server.maxUploadSize", 30)

def split_file(pdfname: str, 
               option: str,
               param: int = 1):
    import pypdf

    with open(pdfname, 'rb') as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)

        N = len(pdf_reader.pages)
        st.write(f"Processing {N} pages...")
        # st.write(f'PDF Metadata is {pdf_reader.metadata}') 

        file_stats = os.stat(pdfname)
        st.write(file_stats)
        global split_strings

        if option == split_strings[0]:
            # st.write('User chose option 1')
            n_splits = param
        elif option == split_strings[1]:
            # st.write('User chose option 2')
            n_splits = int(np.ceil(file_stats.st_size/param))
            # st.write("n_splits:", n_splits)

        pages = [N//n_splits]* (n_splits)
        pages[0] += N % n_splits
        pages = list(filter(lambda num: num != 0, pages))
        st.write(pages) 
        return pages
        
    return []

from typing import List
def serve_files(source: str,
                pages: List[int]):

    st.write(f'Serving {len(pages)} splits for {source}')

    from io import BytesIO
    from pypdf import PdfReader, PdfWriter

    # p_cumsum = np.append([0], np.cumsum(pages))
    p_cumsum = np.cumsum([0,] + pages) 

    # Prepare example
    with open(source, "rb") as fh:
        input_bytes_stream = BytesIO(fh.read())

    # Read from bytes_stream
    reader = PdfReader(input_bytes_stream)

    for i in range(len(pages)):
        writer = PdfWriter()
        for page in reader.pages[p_cumsum[i]: p_cumsum[i+1]]:
            writer.add_page(page)
        
        # Write to bytes_stream        
        with BytesIO() as output_bytes_stream:
            writer.write(output_bytes_stream)
            st.download_button(label=f'File {i}, #pages: {pages[i]}', 
                        data=output_bytes_stream,
                        file_name=f"file_{i}.pdf", 
                        mime='application/pdf')
        
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
    split_param = col2.selectbox('Number of files',np.arange(2, 11))
elif split_option == split_strings[1]:
    n_size = col2.number_input('File size (MB), roughly:',value=4.5, format="%.1f")
    split_param = int(n_size*1024*1024)
    # st.write(n_size, split_param)
    # print(n_size, split_param)
else:
    pass

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

import glob

file_history = glob.glob("./*.pdf")

with st.sidebar:
    st.title("Settings")
    selected_history_file = st.selectbox("**File History**", file_history)
    if st.button("**Load**"):
        if selected_history_file:
            st.session_state['file_uploaded'] = \
                {'successful':True, 
                 'filename': selected_history_file,
                 'pages': None}
            
            st.write(st.session_state.file_uploaded)

    st.divider()
    st.header(":red[Dangerous zone]")
    if st.button("Purge PDF history"):
        if file_history and len(file_history)>0:
            st.write("Delete all  PDFs found.") 
            for fi in file_history:
                os.remove(fi)