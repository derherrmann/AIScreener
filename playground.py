"""
Copy of main.py for testing purposes.
"""

import os
import pandas as pd

from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel, ValidationError

from tools.pdf_reader import get_pdf_md, get_pdf_text

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')


class PDFMetadata(BaseModel):
    """
    Metadata of a scientific paper.
    """
    title: str
    authors: list[str]
    year: int
    publisher: str | None = None


# def get_pdfs(path: str) -> list[str]:
#     """
#     Get a list of PDF files in the given flat directory.
#     :param path:
#     :return:
#     """
#     return [os.path.join(path, file) for file in os.listdir(path) if file.endswith('.pdf')]

def get_pdfs(path: str) -> list[str]:
    """
    Recursively gets a list of PDF files in the given directory and its subdirectories.
    :param path: path to the directory with PDF files
    :return: list of PDF files with full paths
    """
    pdfs = [
        os.path.join(root, file)
        for root, _, files in os.walk(path)
        for file in files
        if file.endswith('.pdf')
    ]
    if not pdfs:
        raise FileNotFoundError(f'No PDF files found in directory: {path}')
    return pdfs


prompt = (
    "You are an intelligent assistant extracting metadata from scientific articles. "
    "Given the following content from the first page of a scientific PDF, extract the metadata.\n\n"
    "Required fields:\n"
    '- "title": The *title of the paper*, not the journal.\n'
    '- "authors": A list of full author names.\n'
    '- "year": Year of publication.\n'
    '- "publisher": Publisher name (e.g. Elsevier, Springer, IEEE).\n\n'
    "Output JSON only, no explanations. Example format:\n"
    '{\n'
    '  "title": "string",\n'
    '  "authors": ["string", "string", ...],\n'
    '  "year": int,\n'
    '  "publisher": "string"\n'
    '}'
)


def build_response(text: str) -> ChatResponse:
    response: ChatResponse = chat(
        model='gemma3:12b',
        messages=[
            {
                'role': 'system',
                'content': prompt
            },
            {
                'role': 'user',
                'content': f'--- PDF Page 1 Content ---'
                           f'{text}'
            }
        ],
        format=PDFMetadata.model_json_schema(),
        options={'temperature': 0},
    )
    return response


def main():
    """
    Main function to extract metadata from PDF files.
    :return:
    """
    pdfs = get_pdfs(DATA_PATH)
    big_data = list()

    for pdf in pdfs:
        print(f'Processing PDF: {pdf}')
        pages = get_pdf_text(pdf)
        response_txt = build_response(pages[0])
        try:
            metadata = PDFMetadata.model_validate_json(response_txt['message']['content'])
            print(metadata)
            data = metadata.model_dump()
            big_data.append(data)
        except ValidationError as e:
            print(f'Parsing error: {e}')

    df = pd.DataFrame(big_data)
    df['authors'] = df['authors'].apply(lambda x: ', '.join(x))
    df.to_csv(os.path.join(DATA_PATH, 'metadata.csv'), index=False)


if __name__ == '__main__':
    main()
