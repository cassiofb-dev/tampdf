import pandas as pd
from tampdf.core.dataset import Dataset


class HappyDataset(Dataset):
  def __init__(
    self,
    name: str,
    urls: list[str],
    validation_urls: list[str] = [],
    generate_plots=True,
    generate_profiles=True,
    generate_tables=True
  ) -> None:
      super().__init__(name, urls, validation_urls, generate_plots, generate_profiles, generate_tables)

  def generic_dataset_to_dataframe(self, generic_path: str) -> pd.DataFrame:
    return pd.read_csv(
      generic_path,
      comment="#",
      delim_whitespace=True,
      header="infer",
      index_col=False
    )