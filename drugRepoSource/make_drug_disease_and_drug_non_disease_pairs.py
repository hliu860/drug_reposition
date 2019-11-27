import pandas as pd
import numpy as np
import os
import sys
import random

# # for debug
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 6000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(linewidth=300)


class DrugDiseaseDrugNonDiseasePairs:
    def __init__(self, data):
        self.data = data
        self.non_disease_n = 10

    def make_drug_non_disease_pair(self):
        non_disease_pair = self.data.copy()
        non_disease_pair["Disease_or_not"] = 1
        # print(non_disease_pair)
        drug_names = non_disease_pair["Drug_name"].unique()
        # print(drug_names)
        indi_umls_concepts = non_disease_pair["Indi_UMLS_concept"].unique()

        drug_indi_known = non_disease_pair["Drug-Indication"]

        # print(indi_umls_concepts)

        # Pick drug and indi and see if it is true relation,
        # if yes discard, if no, keep as non-disease as 0.
        random_seed = 1
        for drug_name in drug_names:
            random_seed += 12
            # print()
            # print(drug_name)
            # print(random_seed)

            non_disease_n = 0
            # while non_disease_n < 3:
            random.seed(random_seed)
            random.shuffle(indi_umls_concepts)
            for indi_random in indi_umls_concepts:
                # print(indi_random)
                drug_indi = drug_name + " " + indi_random
                # print(drug_indi)
                if drug_indi not in drug_indi_known.to_list():
                    # print(drug_indi)
                    # print(drug_indi in drug_indi_known)
                    non_disease_n += 1
                    # print(non_disease_n)
                    # print(drug_indi)
                    non_disease_pair_add = pd.Series({"Drug_name": drug_name,
                                                      "Indi_UMLS_concept": indi_random,
                                                      "Drug-Indication": drug_indi,
                                                      "Disease_or_not": 0})
                    non_disease_pair = non_disease_pair.append(non_disease_pair_add, ignore_index=True)
                    # print(non_disease_pair)
                    if non_disease_n >= self.non_disease_n:
                        break
        # print()
        # print(non_disease_pair)
        return non_disease_pair

    def run(self):
        return self.make_drug_non_disease_pair()


def main():
    # print(os.listdir())
    os.chdir("../")
    # print(os.listdir())

    data = pd.read_csv("./drug_info_data_map_to_umls.txt", sep="\t")
    DrugDiseaseDrugNonDiseasePairs(data=data).run()


if __name__ == '__main__':
    main()
