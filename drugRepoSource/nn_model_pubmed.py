import pandas as pd
import numpy as np
import json
import tensorflow as tf
import csv
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.backends.backend_pdf import PdfPages
from sklearn.preprocessing import MultiLabelBinarizer

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from drugRepoSource.pubmed_search import PubMedBiopython
# import drugRepoSource.NN_model as drugbank_nn


# for debug
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 6000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(linewidth=300)





#
# def main():
#     drug_info_file = "../../drug_info_all.txt"
#     drug_info_data = ReadDrugInfo(drug_info_file).read_clean()
#     # print(drug_info_data.shape)
#     drug_info_data = drug_info_data[:20]
#
#     corpus = MakeLable(drug_info_data).make_label()
#     print("corpus shape", corpus.shape)
#
#     search_terms = drug_info_data.Name.tolist()
#     drug_abstract_all = SearchMultipleTerms(search_terms).search_pubmed()
#
#     labels = corpus.label.tolist()
#     history = DeepModel(drug_abstract_all, labels).model_run()
#     print(history)
#     DeepModel.plot_history(history)
#
#
# if __name__ == '__main__':
#     main()
