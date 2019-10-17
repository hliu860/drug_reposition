from drugRepoSource.get_drug_info_from_drugbank import GetDrugInfoFromDrugBank

from drugRepoSource.read_drug_info_and_clean import ReadDrugInfoAndClean
from drugRepoSource.make_label import MakeLable
from drugRepoSource.search_pubmed_with_terms import SearchMultipleTerms
from drugRepoSource.deep_nn_model import DeepModel
from drugRepoSource.plot_history import PlotHistory


def main():
    # Search Drugbank.com and get drug info, name indication and description.
    GetDrugInfoFromDrugBank("./drugbank_vocabulary.csv").get_drug_info()
    drug_info_file = "./drug_info_all.txt"

    # Read drug info and clean it (remove drug without name, indication, description.)
    drug_info_data = ReadDrugInfoAndClean(drug_info_file).read_clean()
    print("Search drugbank.com returned ", drug_info_data.shape[0], ' drugs, with shape ', drug_info_data.shape)
    drug_test_n = 20
    print("Take ", drug_test_n, ' drugs for test.')
    drug_info_data = drug_info_data[:drug_test_n]
    # print(drug_info_data)

    # Make label for each drug, label is multi-hot indications.
    corpus = MakeLable(drug_info_data).make_label()
    print("corpus with labels shape", corpus.shape)
    # print(corpus)

    # Search drug name to PubMed. Return abstracts,
    print("Search drug name to Pubmed for abstracts.")
    search_terms = drug_info_data.Name.tolist()
    drug_abstract_all = SearchMultipleTerms(search_terms).search_pubmed()
    print(drug_abstract_all.shape)

    # Input abstracts and labels (for each drug) to NN model.
    # pre-process by tokenize and padding.
    labels = corpus.label.tolist()
    print("Input abstract and label to NN model.")
    history = DeepModel(drug_abstract_all, labels).model_run()
    PlotHistory(history).plot_history()
    print('Plot results pdf done.')


if __name__ == '__main__':
    main()
