import pandas as pd
import os


def save_data_to_json_file(data: pd.DataFrame, filename: str) -> None:
    """
        Function that saves given data to json file in raw_data directory.

    :param data: pd.Dataframe, data to be saved to file
    :param filename: Name of the file with .json ending, that will be created if not exists, or will be overwrite
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