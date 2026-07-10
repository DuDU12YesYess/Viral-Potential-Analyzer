import pandas as pd


class DataLoader:
    def __init__(self, data_folder="data"):
        self.data_folder = data_folder

    def load_content_types(self):
        return pd.read_csv(f"{self.data_folder}/content_types.csv")

    def load_hashtags(self):
        return pd.read_csv(f"{self.data_folder}/hashtags.csv")

    def load_audio(self):
        return pd.read_csv(f"{self.data_folder}/audio.csv")

    def load_length_rules(self):
        return pd.read_csv(f"{self.data_folder}/length_rules.csv")

    def load_time_rules(self):
        return pd.read_csv(f"{self.data_folder}/time_rules.csv")