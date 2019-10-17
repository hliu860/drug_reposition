import pandas as pd

from drugRepoSource.parse_drugbank_web import GetDrugBankID, GetConditionFromDrugBank


class GetDrugInfoFromDrugBank:
    def __init__(self, db_voca):
        self.connect_to_drugbank_web = True
        self.process_drug_n = 50
        self.db_voca = db_voca

    def get_drug_info(self):
        if self.connect_to_drugbank_web:
            # Get DrugBank ID.
            drug_ids = GetDrugBankID(self.db_voca).read_file()
            drug_ids = drug_ids.tolist()
            drug_ids = drug_ids[:self.process_drug_n]
            print("Search drugbank.com for ", self.process_drug_n, ' drugs')
            print("It will take a while...")

            # Get drug info.
            drug_info_all = pd.DataFrame()
            counter = 0
            for drug_id in drug_ids:
                counter += 1
                if counter % 50 == 0:
                    print(counter, " / ", self.process_drug_n)

                drug_name, drug_indi, drug_des = GetConditionFromDrugBank(drug_id).get_info()
                drug_indi = "/".join(drug_indi)
                drug_info_one = pd.DataFrame({"Drug_id": drug_id,
                                              "Name": drug_name,
                                              "Indications-DrugBank": drug_indi,
                                              "Description": drug_des},
                                             index=range(1))
                drug_info_all = drug_info_all.append(drug_info_one, ignore_index=True)
            drug_info_all.to_csv("./drug_info_all.txt", sep="\t")
            return drug_info_all


def main():
    GetDrugInfoFromDrugBank("../drugbank_vocabulary.csv").get_drug_info()


if __name__ == '__main__':
    main()
