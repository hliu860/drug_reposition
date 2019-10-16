from drugRepoSource.get_drug_info import GetDrugInfo
import drugRepoSource.NN_model as drugbank_nn
import drugRepoSource.nn_model_pubmed as nn_pubmed

# for debug
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 6000)
# pd.set_option('display.max_colwidth', -1)
# np.set_printoptions(linewidth=300)


def main():
    GetDrugInfo("./drugbank_vocabulary.csv").get_drug_info()
    drug_info_file = "./drug_info_all.txt"
    drug_info_data = drugbank_nn.ReadDrugInfo(drug_info_file).read_clean()
    # print(drug_info_data.shape)
    drug_info_data = drug_info_data[:20]

    corpus = drugbank_nn.DeepModel(drug_info_data).make_label()
    print("corpus shape", corpus.shape)

    search_terms = drug_info_data.Name.tolist()
    abstract_all_padded = nn_pubmed.SearchMultipleTerms(search_terms).pre_process()

    labels = corpus.label.tolist()
    history = nn_pubmed.DeepModel(abstract_all_padded, labels).model_run()
    print(history)
    nn_pubmed.DeepModel.plot_history(history)


if __name__ == '__main__':
    main()
