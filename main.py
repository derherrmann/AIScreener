"""
Extract metadata from scientific articles in PDF format using Ollama's model.
"""
import os
import re

import pandas as pd

from pydantic import ValidationError

from apis.ollama_api import build_response
from tools.prompt_handler import read_prompt
from tools.class_parser import get_model, Test
from tools.pdf_handler import get_pdf_text, get_pdfs

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
PROMPT_PATH = os.path.join(os.path.dirname(__file__), 'config', 'prompt.txt')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'config', 'model.yaml')


def remove_invalid_chars(s):
    return re.sub(r'[<>:"/\\|?*]', '', s)


def main():
    """
    Main function to extract metadata from PDF files.
    :return:
    """
    prompt = read_prompt(PROMPT_PATH)
    model = get_model(MODEL_PATH)
    test_model = Test
    pdfs = get_pdfs(DATA_PATH)

    big_data = list()
    for pdf in pdfs:
        print(f'Processing PDF: {pdf}')
        pages = get_pdf_text(pdf)
        response_txt = build_response(prompt, pages[0], test_model)
        try:
            metadata = model.model_validate_json(response_txt['message']['content'])
            print(metadata)
            data = metadata.model_dump()
            data.update({'pages': len(pages)})
            big_data.append(data)
            cleaned_title = remove_invalid_chars(data['title'])
            try:
                os.rename(pdf, os.path.join(DATA_PATH, cleaned_title + '.pdf'))
            except FileExistsError:
                print(f'File {cleaned_title}.pdf already exists. Skipping rename.')
        except ValidationError as e:
            print(f'Parsing error: {e}')

    df = pd.DataFrame(big_data)
    df['authors'] = df['authors'].apply(lambda x: ', '.join(x))
    df.to_csv(os.path.join(DATA_PATH, 'metadata.csv'), sep=';', index=False)


if __name__ == '__main__':
    main()
