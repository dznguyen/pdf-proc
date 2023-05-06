# pdf-proc

## Intro

Main usage: split a PDF file into smallers consecutive files with sizes under the limit of free service such as Notion.

## Installation
Install the required package as specified in the *requirements.txt*, either via **pip install** or **conda install**

You can run the app by ```streamlit run app.py```

OR, you can deploy it to Streamlit Cloud, HuggingFace, or Heroku etc. for more public usages.

## Version
+ ***ver 0.1***: Provide the core feature
    - Upload pdf file
    - Split the uploaded pdf to smaller chunks, by streaming pages of the original (without saving splitted files in server).
    - Allow user to download the splits as smaller pdf

## Links
+ Streamlit, especially the Download Button: https://docs.streamlit.io/library/api-reference/widgets/st.download_button
+ pypdf: https://pypdf.readthedocs.io/en/stable/index.html
