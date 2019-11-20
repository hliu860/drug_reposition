from sklearn.preprocessing import MultiLabelBinarizer
import pickle
import os
import sys
import pandas as pd
import numpy as np


# # for debug
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 6000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(linewidth=300)


class MakeLable:
    def __init__(self, drug_abstract_all, drug_info_data_with_non_disease):
        self.drug_abstract_all = drug_abstract_all
        self.drug_info_data_with_non_disease = drug_info_data_with_non_disease

    def make_label(self):
        """Label is the condition that drug can treat."""
        corpus = self.drug_abstract_all.copy()
        # print(self.drug_info_data_with_non_disease)
        # # print(corpus)
        #
        # cui = [item.split("/") for item in corpus["Indication"]]   # Though it uses multilabel, it is in fact one hot encoding.
        # # print(cui)
        # # cui = corpus["cui"]
        # mlb = MultiLabelBinarizer()
        # indications_binary = mlb.fit_transform(cui)
        #
        # corpus["label"] = indications_binary.tolist()
        corpus["label"] = 0
        # print(corpus)
        for index, drug_indi in enumerate(corpus["Drug-Indi"]):
            # print(index, drug_indi)
            # print(self.drug_info_data_with_non_disease["Drug-Indication"] == drug_indi)
            # corpus.loc[index, 'label'] =  \
            #     self.drug_info_data_with_non_disease.Disease_or_not[self.drug_info_data_with_non_disease["Drug-Indication"] == drug_indi]

            one_or_zero = self.drug_info_data_with_non_disease.Disease_or_not[
                self.drug_info_data_with_non_disease["Drug-Indication"] == drug_indi
                ]
            # print(int(one_or_zero))
            # print(corpus.loc[index, "label"])
            corpus.loc[index, "label"] = int(one_or_zero)
            # print()
            # corpus.loc[index, 'label'] = self.drug_info_data_with_non_disease.loc[
            #     self.drug_info_data_with_non_disease["Drug-Indication"] == drug_indi,
            #     "Disease_or_not"
            # ]

        # print(self.drug_info_data_with_non_disease["Drug-Indication"] == corpus.loc[0, 'Drug-Indi'])

        # print(corpus)

        return corpus


def main():
    # print(os.listdir())
    os.chdir("../")
    drug_abstract_all = pickle.load(open("drug_abstract_all.pickle", 'rb'))
    drug_info_data_with_non_disease = pickle.load(open("drug_info_data_with_non_disease.pickle", 'rb'))
    MakeLable(drug_abstract_all, drug_info_data_with_non_disease).make_label()


if __name__ == "__main__":
    main()
