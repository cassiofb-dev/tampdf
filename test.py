from tampdf.datasets.happy import HappyDataset


happy_dataset = HappyDataset(
  name="happy",
  urls=["https://raw.githubusercontent.com/COINtoolbox/photoz_catalogues/master/Teddy/forTemplateBased/teddyT_A.cat"],
)

print(happy_dataset.generic_dataframe.head())