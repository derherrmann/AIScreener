import os
import pymupdf
import pymupdf4llm

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
PDF_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scpaper1.pdf')


def get_pdf_md(pdf_path: str) -> str:
    """
    Convert PDF to markdown using pymupdf4llm.
    :param pdf_path:
    :return:
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    with open(os.path.join(os.path.dirname(pdf_path), os.path.basename(pdf_path) + '.md'), 'wb') as f:
        f.write(md_text.encode())
    return md_text


def get_pdf_text(pdf_path: str) -> str:
    """
    Convert PDF to text using pymupdf.
    :param pdf_path:
    :return:
    """
    pages = list()
    text = str()
    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            pages.append(page.get_text())  # get plain text encoded as UTF-8
            text += page.get_text()
    with open(os.path.join(os.path.dirname(pdf_path), os.path.basename(pdf_path) + '.txt'), 'w', encoding='utf-8') as f:
        f.write(text)
    return pages


# DEBUG
# def main():
#     md = get_pdf_md(PDF_PATH)
#     txt = get_pdf_text(PDF_PATH)
#     breakpoint()
#
# if __name__ == '__main__':
#     main()
