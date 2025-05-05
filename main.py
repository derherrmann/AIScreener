import os

import pandas as pd

from pydantic import ValidationError

from apis.ollama_api import build_response
from tools.dataframe_handler import write_df, convert_list2str, read_df
from tools.helper import CLRS, remove_invalid_chars, logging, ct
from tools.prompt_handler import read_prompt
from tools.class_parser import get_model, Test
from tools.pdf_handler import get_pdf_text, get_pdfs

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
PROMPT_PATH = os.path.join(os.path.dirname(__file__), 'config', 'prompt.txt')
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'config', 'model.yaml')


def main():
    """
    Main function to extract metadata from PDF files.
    :return:
    """
    loaded_metadata = read_df(os.path.join(DATA_PATH, 'metadata.csv'))
    prompt = read_prompt(PROMPT_PATH)
    model = get_model(MODEL_PATH)
    # test_model = Test
    pdfs = get_pdfs(DATA_PATH)
    titles = list()

    if not loaded_metadata.empty:
        loaded_metadata['title'] = loaded_metadata['title'].apply(lambda x: remove_invalid_chars(x))
        titles = loaded_metadata['title'].tolist()

    big_data = list()
    for pdf in pdfs:
        filename = os.path.splitext(os.path.basename(pdf))[0]
        if filename in titles:
            logging.info(f'{ct()}{CLRS.WARNING}{filename} already processed. Skipping.{CLRS.ENDC}')
            continue
        logging.info(f'{ct()}{CLRS.OKGREEN}Processing PDF: {pdf}{CLRS.ENDC}')
        pages = get_pdf_text(pdf)
        response_txt = build_response(prompt, pages[0], model)
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
                logging.error(f'{ct()}{CLRS.FAIL}File {cleaned_title}.pdf already exists. Skipping rename.{CLRS.ENDC}')
            tmp_df = pd.DataFrame(big_data)
            df = pd.concat([loaded_metadata, convert_list2str(tmp_df, 'authors')], ignore_index=True).drop_duplicates(
                subset=['title'])
            write_df(DATA_PATH, df)
        except ValidationError as e:
            logging.error(f'{ct()}{CLRS.FAIL}Parsing error: {e}{CLRS.ENDC}')


if __name__ == '__main__':
    main()
