import pandas as pd

from drugRepoSource.parse_drugbank_web import GetDrugBankID, GetConditionFromDrugBank
from drugRepoSource.NN_model import ReadDrugInfo, DeepModel


class GetDrugInfo:
    def __init__(self, db_voca):
        self.connect_to_drugbank_web = True
        self.process_drug_n = 100
        self.db_voca = db_voca

    def get_drug_info(self):
        if self.connect_to_drugbank_web:
            # Get DrugBank ID.
            drug_ids = GetDrugBankID(self.db_voca).read_file()
            drug_ids = drug_ids.tolist()
            drug_ids = drug_ids[:self.process_drug_n]
            # print(drug_ids)

            # Get drug info.
            drug_info_all = pd.DataFrame()
            counter = 0
            for drug_id in drug_ids:
                counter += 1
                if counter % 10 == 0:
                    print(counter)
                drug_name, drug_indi, drug_des = GetConditionFromDrugBank(drug_id).get_info()
                drug_indi = "/".join(drug_indi)
                drug_info_one = pd.DataFrame({"Drug_id": drug_id,
                                              "Name": drug_name,
                                              "Indications-DrugBank": drug_indi,
                                              "Description": drug_des},
                                             index=range(1))
                drug_info_all = drug_info_all.append(drug_info_one, ignore_index=True)
            drug_info_all.to_csv("./drug_info_all.txt", sep="\t")


def main():
    # Run NN model
    drug_info_file = "./drug_info_all.txt"
    drug_info_data = ReadDrugInfo(drug_info_file).read_clean()
    history = DeepModel(drug_info_data).model_run()
    DeepModel(drug_info_data).plot_history(history)


if __name__ == '__main__':
    main()
