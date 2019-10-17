import pandas as pd


class ReadDrugInfoAndClean:
    def __init__(self, drug_info_file):
        self.drug_info = drug_info_file

    def read_clean(self):
        info_data = pd.read_csv(self.drug_info, sep="\t", index_col=0)

        # remove drugs without indication.
        drug_indi = info_data["Indications-DrugBank"].tolist()
        info_data = info_data.loc[[str(x) != "nan" for x in drug_indi]]

        # remove drugs without name
        drug_name = info_data["Name"].tolist()
        info_data = info_data.loc[[str(x) != "nan" for x in drug_name]]

        # remove drugs without description
        drug_des = info_data["Description"]
        info_data = info_data.loc[[str(x) != 'nan' for x in drug_des]]
        info_data.reset_index(drop=True, inplace=True)

        return info_data
