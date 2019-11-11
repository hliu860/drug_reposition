import pandas as pd

from drugRepoSource.parse_drugbank_web import GetDrugBankID, GetConditionFromDrugBank


class GetDrugInfoFromDrugBank:
    def __init__(self, drugbank_vocabulary, process_drug_n, connect_to_drugbank_web):
        self.connect_to_drugbank_web = connect_to_drugbank_web
        self.process_drug_n = process_drug_n
        self.db_voca = drugbank_vocabulary

    def get_drug_info(self):
        if self.connect_to_drugbank_web:
            print("Searching drugbank.com for ", self.process_drug_n, " drugs.")
            print("It will take a while.")
            # Get DrugBank ID.
            drug_ids = GetDrugBankID(self.db_voca).read_file()
            drug_ids = drug_ids.tolist()
            drug_ids = drug_ids[:self.process_drug_n]

            # Get drug info.
            drug_info_all = pd.DataFrame()
            counter = 0
            for drug_id in drug_ids:
                counter += 1
                if counter % 10 == 0:
                    print(counter, " / ", self.process_drug_n)

                drug_name, drug_indi, drug_des = GetConditionFromDrugBank(drug_id).get_info()
                drug_indi = "/".join(drug_indi)
                drug_info_one = pd.DataFrame({"Drug_id": drug_id,
                                              "Name": drug_name,
                                              "Indications-DrugBank": drug_indi
                                              # "Description": drug_des
                                              },
                                             index=range(1))
                drug_info_all = drug_info_all.append(drug_info_one, ignore_index=True)
            drug_info_all.to_csv("./drug_info_all.txt", sep="\t")

            print("Search drugbank.com returned ", drug_info_all.shape[0], ' drugs with shape ', drug_info_all.shape)
            # print("Saved ./drug_info_all.txt.")
            # print(drug_info_all)

            return drug_info_all


def main():
    GetDrugInfoFromDrugBank("../drugbank_vocabulary.csv", process_drug_n=15).get_drug_info()


if __name__ == '__main__':
    main()
