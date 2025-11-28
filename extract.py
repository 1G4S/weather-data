import json

import pandas as pd
import os
import requests


def get_raw_data(channel_id: str, api_key: str) -> str:
    """
    Get raw data from thingspeak cloud.

    :param channel_id: ID of channel to connect
    :param api_key: Key to connect to this channel
    :return: raw_data from channel
    """
    if not isinstance(channel_id, str) or not isinstance(api_key, str):
        raise TypeError(
            f'Incorrect argument types.'
        )

    if api_key.strip() == "":
        raise ValueError(
            f'Incorrect value of api_key: {api_key}'
        )

    url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.csv"

    params = {
        'api_key': api_key,
        'results': 8000
    }

    try:
        raw_data = requests.get(url, params=params, timeout=(5, 10))

    except TimeoutError as e:
        raise TimeoutError(
            f'TimeoutError'
        ) from e

    except Exception as e:
        raise Exception(
            f'{e}'
        )

    return raw_data.text


def save_raw_data_to_csv(raw_data: str, filename: str) -> None:
    """
    Function that saves raw data to csv file in raw_data directory.

    :param raw_data: raw_data as a string
    :param filename: Name of the file with .csv ending, that will be created if not exists, or will be overwritten
                    if exists.
    :return: None
    """
    if not isinstance(raw_data, str) or not isinstance(filename, str):
        raise TypeError(
            f'Incorrect type of arguments. Current type: Data: "{type(raw_data)}", Filename: "{type(filename)}"')

    if filename.strip() == '' or filename[-4:] != '.csv':
        raise ValueError(
            f'Incorrect value of arguments. Filename: "{filename}"')

    try:
        if not os.path.exists('./raw_data'):
            os.makedirs('./raw_data')

    except PermissionError as e:
        raise PermissionError(
            f'No credentials for creating this directory.'
        ) from e

    except OSError as e:
        raise OSError(
            f'Cannot create a directory.'
        ) from e

    file_path = './raw_data/' + filename

    try:
        with open(file_path, 'w') as file:
            file.write(raw_data)

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f'Path to file is wrong: {file_path}'
        ) from e

    except PermissionError as e:
        raise PermissionError(
            f'No credentials for this catalog: {file_path}'
        ) from e


def normalize_csv_to_dataframe(file_path: str) -> pd.DataFrame:
    """
    Convert csv to dataframe and rename columns.

    :param file_path: path to file that should be converted to pd.DataFrame
    :return: prepared pd.DataFrame to be saved to json file
    """
    if not isinstance(file_path, str):
        raise TypeError(
            f'Incorrect type of argument: {type(file_path)}'
        )

    if file_path.strip() == "":
        raise ValueError(
            f'Incorrect value of file path: {file_path}'
        )

    data = pd.read_csv(file_path)

    return data


def rename_columns(data: pd.DataFrame, columns: dict) -> pd.DataFrame:
    """
    Change name of headers.

    :param data: dataframe with raw_data and raw headers
    :param columns: dict, old headers with as keys and new headers as values
    :return: dataframe with new headers
    """
    if not isinstance(columns, dict):
        raise TypeError(
            f'Incorrect type of argument: {type(columns)}'
        )
    try:
        prepared_data = data.rename(columns=columns)
    except Exception as e:
        raise Exception(
            f'Exception happened: {e}'
        ) from e

    return prepared_data


def save_data_to_json_file(data: pd.DataFrame, filename: str) -> None:
    """
    Function that saves given data to json file in data directory.

    :param data: pd.Dataframe, data to be saved to file
    :param filename: Name of the file with .json ending, that will be created if not exists, or will be overwritten
                    if exists.
    :return: None
    """
    if not isinstance(data, pd.DataFrame) or not isinstance(filename, str):
        raise TypeError(
            f'Incorrect type of arguments. Current type: Data: "{type(data)}", Filename: "{type(filename)}"')

    if filename.strip() == '' or filename[-5:] != '.json':
        raise ValueError(
            f'Incorrect value of arguments. Filename: "{filename}"')

    try:
        if not os.path.exists('./data'):
            os.makedirs('./data')

    except PermissionError as e:
        raise PermissionError(
            f'No credentials for creating this directory.'
        ) from e

    except OSError as e:
        raise OSError(
            f'Cannot create a directory.'
        ) from e

    file_path = './data/' + filename
    json_data = data.to_json(orient='records', indent=4)

    try:
        with open(file_path, 'w') as file:
            file.write(json_data)

    except FileNotFoundError as e:
        raise FileNotFoundError(
            f'Path to file is wrong: {file_path}'
        ) from e

    except PermissionError as e:
        raise PermissionError(
            f'No credentials for this catalog: {file_path}'
        ) from e


def merge_json_files(paths_files: list, filename: str) -> None:
    """
    Merge json files into one json, and save it to gold_data directory.

    :param paths_files: list of paths to json files.
    :param filename: name of file that data will be saved.
    :return: None
    """
    if not isinstance(paths_files, list) and not isinstance(filename, str):
        raise TypeError(
            f'Incorrect types of arguments'
        )

    if filename.strip() == '' or filename[-5:] != '.json':
        raise ValueError(
            f'Incorrect value of arguments. Filename: "{filename}"')

    try:
        if not os.path.exists('./gold_data'):
            os.makedirs('./gold_data')

    except PermissionError as e:
        raise PermissionError(
            f'No credentials for creating this directory.'
        ) from e

    except OSError as e:
        raise OSError(
            f'Cannot create a directory.'
        ) from e

    merged_json = []

    try:
        for file in paths_files:
            with open(file, 'r') as f:
                data = json.load(f)
                merged_json.extend(data)
    except Exception as e:
        raise Exception(
            f'Exception happened: {e}'
        ) from e

    output_path = './gold_data/' + filename

    try:
        with open(output_path, 'w') as f:
            json.dump(merged_json, f, indent=4)
    except Exception as e:
        raise Exception(
            f'Exception happened: {e}'
        ) from e
