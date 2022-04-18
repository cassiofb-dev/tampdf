import os, pandas as pd
import numpy as np
from urllib import request
from scipy import stats

class Dataset:
  def __init__(
    self,
    name: str,
    urls: list[str],
    validation_urls: list[str] = [],
    generate_plots=True,
    generate_profiles=True,
    generate_tables=True,
  ) -> None:
    self.name = name
    self.urls = urls
    self.validation_urls = validation_urls
    self.generate_plots = generate_plots
    self.generate_profiles = generate_profiles
    self.generate_tables = generate_tables
    self.generic_paths: list[str] = []
    self.validation_paths: list[str] = []
    self.column_names = Dataset.get_column_names()

    self.download_datasets()

    self.generic_dataframe: pd.DataFrame = self.get_processed_data()

    self.save_processed_data()

  def download_datasets(self):
    os.makedirs(Dataset.get_raw_path(), exist_ok=True)
    self.download_validation_or_generic_datasets(True, ".data")
    self.download_validation_or_generic_datasets(False, "_validation.data")

  def download_validation_or_generic_datasets(self, is_generic: bool, ends_with: str):
    for (index, dataset_url) in enumerate(self.urls if is_generic else self.validation_urls):
      DATASET_NAME = self.name + "_" + str(index) + ends_with
      DATASET_PATH = os.path.join(Dataset.get_raw_path(), DATASET_NAME)

      self.generic_paths.append(DATASET_PATH) if is_generic else self.validation_paths.append(DATASET_PATH)

      if os.path.isfile(DATASET_PATH) == False:
        request.urlretrieve(dataset_url, DATASET_PATH)

  def generic_dataset_to_dataframe(self, generic_path: str) -> pd.DataFrame:
    raise "Not Implemented!"

  def validation_dataset_to_dataframes(self, validation_path: str):
    raise "Not Implemented!"

  def generics_datasets_to_dataframes(self) -> list[pd.DataFrame]:
    generic_dataframes: list[pd.DataFrame] = []

    for generic_path in self.generic_paths:
      generic_dataframes.append(self.generic_dataset_to_dataframe(generic_path))

    return generic_dataframes

  def get_processed_data(self) -> pd.DataFrame:
    generics_dataframes = self.generics_datasets_to_dataframes()

    merged_generics_dataframes = pd.concat(generics_dataframes)

    no_duplicate_df = merged_generics_dataframes.drop_duplicates()

    outlier_mask = (np.abs(stats.zscore(no_duplicate_df)) < 3).all(axis=1)

    no_outlier_df = no_duplicate_df[outlier_mask]

    return no_outlier_df

  def save_processed_data(self):
    FILENAME = self.name + "_processed.csv"
    PROCESSED_DATAPATH = os.path.join(Dataset.get_processed_path(), FILENAME)

    self.generic_dataframe.to_csv(PROCESSED_DATAPATH)

  @staticmethod
  def get_ugriz_columns():
    return [letter for letter in "ugriz"]

  @staticmethod
  def get_ugriz_error_columns():
    return [column_name + 'Err' for column_name in Dataset.get_ugriz_columns()]

  @staticmethod
  def get_column_names():
    return ["ID", *Dataset.get_ugriz_columns(), *Dataset.get_ugriz_error_columns(), "photo-z"]

  @staticmethod
  def get_raw_path():
    CURRENT_PATH = os.getcwd()
    DATASET_PATH = "data/datasets/raws"
    FULL_PATH = os.path.join(CURRENT_PATH, DATASET_PATH)

    return FULL_PATH

  @staticmethod
  def get_processed_path():
    CURRENT_PATH = os.getcwd()
    DATASET_PATH = "data/datasets"
    FULL_PATH = os.path.join(CURRENT_PATH, DATASET_PATH)

    return FULL_PATH