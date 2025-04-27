import pandas as pd

class DataLoader:
    def __init__(self):
        pass

    def load_csv(self, filepath: str) -> pd.DataFrame:
        return pd.read_csv(filepath)

    def load_excel(self, filepath: str) -> pd.DataFrame:
        return pd.read_excel(filepath)

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df.dropna()
        df = df.drop_duplicates()
        return df

    def load_data(self, filepath: str, file_type: str) -> pd.DataFrame:
        if file_type == 'csv':
            df = self.load_csv(filepath)
        elif file_type == 'excel':
            df = self.load_excel(filepath)
        else:
            raise ValueError("Unsupported file type. Please use 'csv' or 'excel'.")
        
        return self.clean_data(df)