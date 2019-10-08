import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


# # for debug
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 6000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(linewidth=300)


class GetDrugBankID:
    def __init__(self, input_file):
        self.input_file = input_file

    def read_file(self):
        data = pd.read_csv(self.input_file)
        # print(data)
        return data["DrugBank ID"]


class GetConditionFromDrugBank:
    def __init__(self, drug_id):
        self.drugID = drug_id
        self.url = "https://www.drugbank.ca/drugs/" + self.drugID

    def parse_url(self):
        """parse url for later use"""
        page = requests.get(self.url)
        soup = BeautifulSoup(page.text, "html.parser")
        return soup

    def get_info(self):
        """Get info"""
        soup = self.parse_url()

        list_unstypled = soup.find_all(class_='list-unstyled')

        # Get drug name.
        drug_name = soup.title.contents[0].split(" - ")[0]

        # get indications.
        drug_indi = []
        for item in list_unstypled:
            all_a = item.find_all("a")
            for each_a in all_a:
                if "indications" in each_a.get("href"):
                    drug_indi.append(each_a.contents[0])

        # Get description.
        for item in soup.head.find_all("meta"):
            if item.get("name") == "description":
                drug_des = item.get("content")

        return drug_name, drug_indi, drug_des


def main():
    drug_ids = GetDrugBankID("../drugbank_vocabulary.csv").read_file()
    print(drug_ids.__class__)
    print(drug_ids.tolist())
    drug_ids = drug_ids.tolist()
    drug_ids = drug_ids[:10]

    # drug_ids = ["DB00440", "DB00316", "DB01048",
    #             "DB00106", "DB05812", "DB08899",
    #             "DB11703", "DB00284", "DB13783",
    #             "DB03166", "DB00551", "DB01063",
    #             "DB00787", "DB00131", "DB08916",
    #             "DB06594", "DB00518", "DB06766"]

    drug_info_all = pd.DataFrame()

    for drug_id in drug_ids:
        drug_name, drug_indi, drug_des = GetConditionFromDrugBank(drug_id).get_info()
        drug_indi = "/".join(drug_indi)
        drug_info_one = pd.DataFrame({"Drug_id": drug_id,
                                      "Name": drug_name,
                                      "Indications-DrugBank": drug_indi,
                                      "Description": drug_des},
                                     index=range(1))

        drug_info_all = drug_info_all.append(drug_info_one, ignore_index=True)
    drug_info_all.to_csv("../drug_info_all.txt", sep="\t")
    print(drug_info_all)


if __name__ == '__main__':
    main()
