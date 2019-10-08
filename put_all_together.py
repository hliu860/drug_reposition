import pandas as pd
import numpy as np

from drugRepoSource.parse_drugbank_web import GetDrugBankID, GetConditionFromDrugBank
from drugRepoSource.NN_model import ReadDrugInfo, DeepModel

# for debug
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 6000)
# pd.set_option('display.max_colwidth', -1)
# np.set_printoptions(linewidth=300)


def main():
    connect_to_drugbank_web = False  # This only needs to run once.
    process_drug_n = 1000    # max is

    if connect_to_drugbank_web:
        # Get DrugBank ID.
        drug_ids = GetDrugBankID("./drugbank_vocabulary.csv").read_file()
        drug_ids = drug_ids.tolist()
        drug_ids = drug_ids[:process_drug_n]
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
        drug_info_all.to_csv("../drug_info_all.txt", sep="\t")
        # print(drug_info_all)

    # Run NN model
    drug_info_file = "../drug_info_all.txt"
    drug_info_data = ReadDrugInfo(drug_info_file).read_clean()
    history = DeepModel(drug_info_data).model_run()
    DeepModel(drug_info_data).plot_history(history)


if __name__ == '__main__':
    main()
