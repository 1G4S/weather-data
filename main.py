from dotenv import load_dotenv
import os
from extract import (save_raw_data_to_csv, save_data_to_json_file, get_raw_data,
                     normalize_csv_to_dataframe, rename_columns, merge_json_files)

load_dotenv()

API_KEY_PARIS = os.getenv('PARIS_API_KEY')
CHANNEL_ID_PARIS = os.getenv('PARIS_CHANNEL_ID')

API_KEY_ROME = os.getenv('ROME_API_KEY')
CHANNEL_ID_ROME = os.getenv('ROME_CHANNEL_ID')

API_KEY_MADRID = os.getenv('MADRID_API_KEY')
CHANNEL_ID_MADRID = os.getenv('MADRID_CHANNEL_ID')

API_KEY_WARSAW = os.getenv('WARSAW_API_KEY')
CHANNEL_ID_WARSAW = os.getenv('WARSAW_CHANNEL_ID')

columns = {"created_at": "timestamp",
           "field1": "PM2.5",
           "field2": "PM10",
           "field3": "temperature",
           "field4": "humidity",
           "field5": "PM2.5_norm",
           "field6": "PM10_norm",
           "field7": "city"}

files = ["./data/paris-weather.json", "./data/rome-weather.json", "./data/madrid-weather.json",
         "./data/warsaw-weather.json"]

###################### PARIS ##########################
raw_data = get_raw_data(channel_id=CHANNEL_ID_PARIS, api_key=API_KEY_PARIS)
save_raw_data_to_csv(raw_data=raw_data, filename="paris.csv")
paris_df = normalize_csv_to_dataframe('./raw_data/paris.csv')
paris_ready_df = rename_columns(paris_df, columns=columns)
save_data_to_json_file(paris_ready_df, filename="paris-weather.json")

###################### ROME ##########################
raw_data = get_raw_data(channel_id=CHANNEL_ID_ROME, api_key=API_KEY_ROME)
save_raw_data_to_csv(raw_data=raw_data, filename="rome.csv")
rome_df = normalize_csv_to_dataframe('./raw_data/rome.csv')
rome_ready_df = rename_columns(rome_df, columns=columns)
save_data_to_json_file(rome_ready_df, filename="rome-weather.json")

###################### MADRID ##########################
raw_data = get_raw_data(channel_id=CHANNEL_ID_MADRID, api_key=API_KEY_MADRID)
save_raw_data_to_csv(raw_data=raw_data, filename="madrid.csv")
madrid_df = normalize_csv_to_dataframe('./raw_data/madrid.csv')
madrid_ready_df = rename_columns(madrid_df, columns=columns)
save_data_to_json_file(madrid_ready_df, filename="madrid-weather.json")

###################### WARSAW ##########################
raw_data = get_raw_data(channel_id=CHANNEL_ID_WARSAW, api_key=API_KEY_WARSAW)
save_raw_data_to_csv(raw_data=raw_data, filename="warsaw.csv")
warsaw_df = normalize_csv_to_dataframe('./raw_data/warsaw.csv')
warsaw_ready_df = rename_columns(warsaw_df, columns=columns)
save_data_to_json_file(warsaw_ready_df, filename="warsaw-weather.json")

###################### FINAL DATA ######################
merge_json_files(files, "weather-data.json")
