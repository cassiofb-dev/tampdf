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

    self.analyse_dataset()

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
    self.raw_dataframe = dataframe

    no_duplicate_df = dataframe.drop_duplicates()

    if self.z_score_outlier_threshold == None:
      self.dataframe = no_duplicate_df
      return

    outlier_mask = (np.abs(stats.zscore(no_duplicate_df)) < self.z_score_outlier_threshold).all(axis=1)

    no_outlier_df = no_duplicate_df[outlier_mask]

    self.dataframe = no_outlier_df

  def save_dataset(self):
    os.makedirs(Dataset.get_processed_path(), exist_ok=True)

    FILENAME = self.name + ".csv"
    PROCESSED_DATAPATH = os.path.join(Dataset.get_processed_path(), FILENAME)

    if os.path.exists(PROCESSED_DATAPATH) == False:
      self.dataframe.to_csv(PROCESSED_DATAPATH)

    self.dataframe_path = PROCESSED_DATAPATH

  def analyse_dataset(self):
    if self.generate_plots: self.run_plot_analysis()
    if self.generate_tables: self.run_table_analysis()
    if self.generate_profiles: self.run_profile_analysis()

  def run_plot_analysis(self):
    os.makedirs(Dataset.get_plots_path(), exist_ok=True)

    for x_column, y_column in zip(Dataset.get_bands(), Dataset.get_errors()):
      Dataset.generate_regplot(
        x_column=x_column,
        y_column=y_column,
        filepath=os.path.join(Dataset.get_plots_path(), f"{self.name}_{x_column}_vs_{y_column}_regplot_raw.png"),
        dataframe=self.raw_dataframe,
      )

      Dataset.generate_regplot(
        x_column=x_column,
        y_column=y_column,
        filepath=os.path.join(Dataset.get_plots_path(), f"{self.name}_{x_column}_vs_{y_column}_regplot_processed.png"),
        dataframe=self.dataframe,
      )

    sns.set_theme(font_scale=2)

    self.generate_raw_pairplots()
    self.generate_processed_pairplots()

  def generate_raw_pairplots(self):
    sns.pairplot(
      self.raw_dataframe,
      x_vars=Dataset.get_bands(),
      y_vars=Dataset.get_bands(),
    ).savefig(os.path.join(Dataset.get_plots_path(), f"{self.name}_bands_vs_bands_raw.png"))

    sns.pairplot(
      self.raw_dataframe,
      x_vars=Dataset.get_bands(),
      y_vars=Dataset.get_errors(),
    ).savefig(os.path.join(Dataset.get_plots_path(), f"{self.name}_bands_vs_errors_raw.png"))

    sns.pairplot(
      self.raw_dataframe,
      x_vars=Dataset.get_errors(),
      y_vars=Dataset.get_errors(),
    ).savefig(os.path.join(Dataset.get_plots_path(), f"{self.name}_errors_vs_errors_raw.png"))

  def generate_processed_pairplots(self):
    sns.pairplot(
      self.dataframe,
      x_vars=Dataset.get_bands(),
      y_vars=Dataset.get_bands(),
    ).savefig(os.path.join(Dataset.get_plots_path(), f"{self.name}_bands_vs_bands_raw.png"))

    sns.pairplot(
      self.dataframe,
      x_vars=Dataset.get_bands(),
      y_vars=Dataset.get_errors(),
    ).savefig(os.path.join(Dataset.get_plots_path(), f"{self.name}_bands_vs_errors_raw.png"))

    sns.pairplot(
      self.dataframe,
      x_vars=Dataset.get_errors(),
      y_vars=Dataset.get_errors(),
    ).savefig(os.path.join(Dataset.get_plots_path(), f"{self.name}_errors_vs_errors_raw.png"))

  def run_table_analysis(self):
    pass

  def run_profile_analysis(self):
    os.makedirs(Dataset.get_profiles_path(), exist_ok=True)

    raw_profile_name = self.name + "_raw_profile"
    raw_profile = ProfileReport(
      df=self.raw_dataframe.drop("ID", axis=1),
      title=raw_profile_name,
      explorative=True,
    )

    raw_profile.to_file(os.path.join(Dataset.get_profiles_path(), raw_profile_name + ".html"))

    processed_profile_name = self.name + "_processed_profile"
    raw_profile = ProfileReport(
      df=self.dataframe.drop("ID", axis=1),
      title=processed_profile_name,
      explorative=True,
    )

    raw_profile.to_file(os.path.join(Dataset.get_profiles_path(), processed_profile_name + ".html"))

  @staticmethod
  def generate_regplot(x_column, y_column, filepath, dataframe):
      regplot_figure = sns.regplot(
        data=dataframe,
        x=x_column,
        y=y_column,
        line_kws={"color": "black"},
      ).get_figure()

      regplot_figure.savefig(filepath)
      regplot_figure.clf()

  @staticmethod
  def get_bands():
    return [letter for letter in "ugriz"]

  @staticmethod
  def get_errors():
    return [column_name + 'Err' for column_name in Dataset.get_bands()]

  @staticmethod
  def get_column_names():
    return ["ID", *Dataset.get_bands(), *Dataset.get_errors(), "photo-z"]

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