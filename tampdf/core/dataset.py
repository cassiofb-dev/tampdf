import os
import numpy as np
import pandas as pd
import seaborn as sns

from scipy import stats
from urllib import request
from pandas_profiling import ProfileReport

sns.set_theme()


class Dataset:
  def __init__(
    self,
    url: str,
    name: str,
    generate_plots=True,
    generate_tables=True,
    generate_profiles=True,
    z_score_outlier_threshold: float = None,
  ) -> None:
    self.url = url
    self.name = name
    self.generate_plots = generate_plots
    self.generate_tables = generate_tables
    self.generate_profiles = generate_profiles
    self.z_score_outlier_threshold = z_score_outlier_threshold

    self.initDataset()

  def initDataset(self):
    self.download_dataset()
    self.process_dataset()
    self.save_dataset()

  def download_dataset(self):
    os.makedirs(Dataset.get_raw_path(), exist_ok=True)

    DATASET_NAME = self.name + ".data"
    DATASET_PATH = os.path.join(Dataset.get_raw_path(), DATASET_NAME)

    self.path = DATASET_PATH

    if os.path.isfile(DATASET_PATH) == False:
      request.urlretrieve(self.url, DATASET_PATH)

  def dataset_to_dataframe(self, path: str) -> pd.DataFrame:
    raise "Not Implemented!"

  def process_dataset(self) -> pd.DataFrame:
    dataframe = self.dataset_to_dataframe(self.path)

    no_duplicate_df = dataframe.drop_duplicates()

    if self.z_score_outlier_threshold == None:
      self.dataframe = no_duplicate_df
      return

    outlier_mask = (np.abs(stats.zscore(no_duplicate_df)) < 3).all(axis=1)

    no_outlier_df = no_duplicate_df[outlier_mask]

    self.dataframe = no_outlier_df
    self.raw_dataframe = dataframe

  def save_dataset(self):
    os.makedirs(Dataset.get_processed_path(), exist_ok=True)

    FILENAME = self.name + ".csv"
    PROCESSED_DATAPATH = os.path.join(Dataset.get_processed_path(), FILENAME)

    if os.path.exists(PROCESSED_DATAPATH) == False:
      self.dataframe.to_csv(PROCESSED_DATAPATH)

    self.dataframe_path = PROCESSED_DATAPATH

  def analyse(self):
    if self.generate_plots: self.init_plot_analysis()
    if self.generate_tables: self.init_plot_analysis()
    if self.generate_profiles: self.init_plot_analysis()

  def init_plot_analysis(self):
    pass

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
    RAW_PATH = "data/datasets/raw"
    FULL_PATH = os.path.join(CURRENT_PATH, RAW_PATH)

    return FULL_PATH

  @staticmethod
  def get_processed_path():
    CURRENT_PATH = os.getcwd()
    PROCESSED_PATH = "data/datasets/processed"
    FULL_PATH = os.path.join(CURRENT_PATH, PROCESSED_PATH)

    return FULL_PATH

  @staticmethod
  def get_plots_path():
    CURRENT_PATH = os.getcwd()
    PLOTS_PATH = "data/analysis/plots"
    FULL_PATH = os.path.join(CURRENT_PATH, PLOTS_PATH)

    return FULL_PATH

  @staticmethod
  def get_tables_path():
    CURRENT_PATH = os.getcwd()
    TABLES_PATH = "data/analysis/tables"
    FULL_PATH = os.path.join(CURRENT_PATH, TABLES_PATH)

    return FULL_PATH

  @staticmethod
  def get_profiles_path():
    CURRENT_PATH = os.getcwd()
    PROFILES_PATH = "data/analysis/profiles"
    FULL_PATH = os.path.join(CURRENT_PATH, PROFILES_PATH)

    return FULL_PATH