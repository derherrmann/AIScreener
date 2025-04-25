import yaml
from pydantic import BaseModel, create_model
from typing import Any


def type_parser(type_str: str) -> Any:
    """
    Parse the type string to a Python type.
    Supported types: str, int, float, list[str], str | None.
    :param type_str: Type string from YAML
    :return: Python type
    """
    types = {
        'str': str,
        'int': int,
        'float': float,
        'list[str]': list[str],
        'str | None': str | None,
    }
    return types.get(type_str, Any)


def read_yaml(path: str) -> dict:
    """
    Read a YAML file and return its content as a dictionary.
    :param path:
    :return:
    """
    with open(path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)


def build_model_from_dict(data: dict) -> BaseModel:
    """
    Build a pydantic model from a dictionary.
    :param data:
    :return:
    """
    model_name = data.get('model_name', 'CustomModel')
    description = data.get('description', 'Custom pydantic model.')
    columns = data.get('columns', [])

    model_columns = dict()
    for column in columns:
        column_name = column['name']
        column_type = type_parser(column['type'])
        # required = column.get('required', True)
        #
        # if not required:
        #     model_columns[column_name] = (column_type, None)
        # else:
        #     model_columns[column_name] = (column_type, ...)
        model_columns[column_name] = (column_type, ...)

    model = create_model(model_name, __doc__=description, **model_columns)
    return model


def get_model(path: str) -> BaseModel:
    """
    Get a pydantic model from a YAML file.
    :param path: Path to the YAML file.
    :return: Pydantic model.
    """
    data = read_yaml(path)
    model = build_model_from_dict(data)
    return model


class Test(BaseModel):
    """
    Metadata of a scientific paper.
    """
    title: str
    authors: list[str]
    year: int
    publisher: str | None
    summary: str | None
