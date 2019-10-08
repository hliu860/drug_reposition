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
        print(data)


def main():
    GetDrugBankID("../drugbank_vocabulary.csv").read_file()


if __name__ == '__main__':
    main()
