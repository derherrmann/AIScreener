from ollama import chat
from ollama import ChatResponse
from pydantic import BaseModel


def build_response(prompt: str, text: str, metadata: BaseModel) -> ChatResponse:
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
            },
            {
                'role': 'user', }
        ],
        format=metadata.model_json_schema(),
        options={'temperature': 0},
    )
    return response
