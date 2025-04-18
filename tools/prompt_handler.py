# prompt = (
#     "You are an intelligent assistant extracting metadata from scientific articles. "
#     "Given the following content from the first page of a scientific PDF, extract the metadata.\n\n"
#     "Required fields:\n"
#     '- "title": The *title of the paper*, not the journal.\n'
#     '- "authors": A list of full author names.\n'
#     '- "year": Year of publication.\n'
#     '- "publisher": Publisher name (e.g. Elsevier, Springer, IEEE).\n'
#     '- "summary": A short summary of the Abstract and Introduction if provided.\n\n'
#     "Output JSON only, no explanations. Example format:\n"
#     '{\n'
#     '  "title": "string",\n'
#     '  "authors": ["string", "string", ...],\n'
#     '  "year": int,\n'
#     '  "publisher": "string"\n'
#     '  "summary": "string"\n'
#     '}'
# )


def read_prompt(path: str) -> str:
    """
    :return: read prompt from file
    """
    with open(path, 'r') as f:
        prompt = f.read()
    return prompt
