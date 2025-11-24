import pandas as pd
import os


def normalize_csv_to_dataframe_and_rename_columns(file_path: str) -> pd.DataFrame:
    if not isinstance(file_path, str):
        raise TypeError(
            f'Incorrect type of argument: {type(file_path)}'
        )

    if file_path.strip() == "":
        raise ValueError(
            f'Incorrect value of file path: {file_path}'
        )

    data = pd.read_csv(file_path)

    ready_data = data.rename(columns={"created_at": "timestamp",
                                      "field1": "PM2.5",
                                      "field2": "PM10",
                                      "field3": "temperature",
                                      "field4": "humidity",
                                      "field5": "PM2.5 norm",
                                      "field6": "PM10 norm",
                                      "field7": "city"})

    return ready_data


def save_data_to_json_file(data: pd.DataFrame, filename: str) -> None:
    """
    Function that saves given data to json file in raw_data directory.

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
