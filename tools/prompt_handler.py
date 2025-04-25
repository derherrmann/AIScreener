def read_prompt(path: str) -> str:
    """
    :return: read prompt from file
    """
    with open(path, 'r') as f:
        prompt = f.read()
    return prompt
