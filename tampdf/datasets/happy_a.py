import pandas as pd
from tampdf.core.dataset import Dataset


class HappyA(Dataset):
  def __init__(
    self,
    url: str,
    name: str,
    generate_plots=True,
    generate_tables=True,
    generate_profiles=True,
    z_score_outlier_threshold: float = None,
  ) -> None:
    super().__init__(
      url,
      name,
      generate_plots,
      generate_tables,
      generate_profiles,
      z_score_outlier_threshold,
    )

  def dataset_to_dataframe(self, path: str) -> pd.DataFrame:
    return pd.read_csv(
      path,
      comment="#",
      header="infer",
      index_col=False,
      delim_whitespace=True,
      names=Dataset.get_column_names(),
    )