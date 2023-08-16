# import tempfile, os
# from fastapi import UploadFile

from typing import List, Dict, Any

from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.utils.constants import OpenAIConstants

from app.parsers import json, csv, docx, html, pdf, txt, youtube, sitemap, urls, nbic_json

FILE_PARSER = {
    ".json": json.parse_json,
    ".csv": csv.parse_csv,
    ".txt": txt.parse_txt,
    ".docx": docx.parse_docx,
    ".pdf": pdf.parse_pdf,
    ".html": html.parse_html,
    ".htm": html.parse_html,
}


URL_PARSERS = {
    "youtube": youtube.parse_youtube_video,
    "sitemap": sitemap.parse_sitemap,
    "webpage": urls.parse_url,
}

# TODO: movie this to file pydantic model in future
# def parse_file(
#     file: UploadFile, Loader_class: type, loader_params: Dict[str, Any]
# ) -> List[Document]:
#     """
#     Parse the uploaded file using the specified loader class with given parameters.

#     Args:
#         file (UploadFile): The uploaded file to parse.
#         Loader_class (type): The loader class to use for parsing the file.
#         loader_params (Dict[str, str]): Additional parameters to pass to the loader class.

#     Returns:
#         List[Document]: List of documents.
#     """

#     with tempfile.NamedTemporaryFile(delete=False, prefix=file.filename) as tmp_file:
#         tmp_file.write(file.file.read())
#         loader = Loader_class(file_path=tmp_file.name, **loader_params)
#         documents = loader.load()

#     os.remove(tmp_file.name)

#     return documents
