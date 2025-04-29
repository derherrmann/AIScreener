import os

import pandas as pd

from tools.helper import CLRS, logging, ct


def read_df(path: str) -> pd.DataFrame | None:
    """
    Read a CSV file into a DataFrame.
    :param path: Path to the CSV file.
    :return: DataFrame containing the data from the CSV file.
    """
    try:
        df = pd.read_csv(path, sep=';')
        return df
    except FileNotFoundError:
        logging.error(f'{ct()}{CLRS.FAIL}File {path} not found.{CLRS.ENDC}')
        return None
    except PermissionError:
        logging.error(f'{ct()}{CLRS.FAIL}Permission denied for file {path}.{CLRS.ENDC}')
        exit(1)
    except Exception:
        logging.error(f'{ct()}{CLRS.FAIL}Error reading file {path}.{CLRS.ENDC}')
        exit(1)


def write_df(path: str, df: pd.DataFrame) -> None:
    """
    Write a DataFrame to a CSV file.
    :param df: DataFrame to write.
    :param path: Path to the CSV file.
    """
    full_path = os.path.join(path, 'metadata.csv')
    try:
        df.to_csv(full_path, sep=';', index=False)
        logging.info(f'{ct()}:{CLRS.OKGREEN}File {path} written successfully.{CLRS.ENDC}')
    except PermissionError:
        logging.error(f'{ct()}:{CLRS.FAIL}Permission denied for file {full_path}.\n'
                      f'Retrying with different naming.{CLRS.ENDC}')
        try:
            df.to_csv(path + ct() + '.csv', sep=';', index=False)
        except Exception:
            logging.error(f'{ct()}:{CLRS.FAIL}Error writing file {full_path}.{CLRS.ENDC}')
            exit(1)


def convert_list2str(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Convert a list in a DataFrame column to a string.
    :param df: DataFrame containing the data.
    :param column: Column name to convert.
    :return: DataFrame with the specified column converted to a string.
    """
    df[column] = df[column].apply(lambda x: ', '.join(x))
    return df


def convert_str2list(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """
    Convert a string in a DataFrame column to a list.
    :param df: DataFrame containing the data.
    :param column: Column name to convert.
    :return: DataFrame with the specified column converted to a list.
    """
    df[column] = df[column].apply(lambda x: x.split(', '))
    return df

# def main():
#     # Example usage
#     df = read_df('data/metadata.csv')
#     if df is not None:
#         print(df.head())
#         write_df(df, 'data/metadata_copy.csv')
#         df = convert_list2str(df, 'authors')
#         print(df.head())
#         df = convert_str2list(df, 'authors')
#         print(df.head())
#
#
# if __name__ == '__main__':
#     main()
