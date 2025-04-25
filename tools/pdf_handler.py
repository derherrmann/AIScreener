import os
import pymupdf
import pymupdf4llm


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


def get_pdf_md(pdf_path: str, save: bool = None) -> str:
    """
    Convert PDF to markdown using pymupdf4llm.
    :param save:
    :param pdf_path:
    :return:
    """
    md_text = pymupdf4llm.to_markdown(pdf_path)
    if save:
        with open(os.path.join(os.path.dirname(pdf_path), os.path.basename(pdf_path) + '.md'), 'w',
                  encoding='utf-8') as f:
            f.write(md_text)
    return md_text


def get_pdf_text(pdf_path: str, save: bool = None) -> list:
    """
    Convert PDF to text using pymupdf.
    :param save:
    :param pdf_path:
    :return:
    """
    pages = list()
    text = str()
    with pymupdf.open(pdf_path) as pdf:
        for page in pdf:
            pages.append(page.get_text())  # get plain text encoded as UTF-8
            text += page.get_text()
    if save:
        with open(os.path.join(os.path.dirname(pdf_path), os.path.basename(pdf_path) + '.txt'), 'w',
                  encoding='utf-8') as f:
            f.write(text)
    return pages

# DEBUG
# def main():
#     DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')
#     PDF_PATH = os.path.join(os.path.dirname(__file__), 'data', 'scpaper1.pdf')
#     md = get_pdf_md(PDF_PATH)
#     txt = get_pdf_text(PDF_PATH)
#     breakpoint()
#
# if __name__ == '__main__':
#     main()
