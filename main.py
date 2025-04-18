"""
Extract metadata from scientific articles in PDF format using Ollama's model.
"""
import os
import pandas as pd

from pydantic import ValidationError

from apis.ollama_api import build_response
from tools.class_parser import PDFMetadata
from tools.pdf_handler import get_pdf_text, DATA_PATH, get_pdfs

# DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
DATA_PATH = r"E:\OneDrive\Desktop\Literaturrecherche"


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
            data.update({'pages': len(pages)})
            data.update({'filename': os.path.basename(pdf)})
            big_data.append(data)
        except ValidationError as e:
            print(f'Parsing error: {e}')

    df = pd.DataFrame(big_data)
    df['authors'] = df['authors'].apply(lambda x: ', '.join(x))
    df.to_csv(os.path.join(DATA_PATH, 'metadata.csv'), sep=';', index=False)


if __name__ == '__main__':
    main()
