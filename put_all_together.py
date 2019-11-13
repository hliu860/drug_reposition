import pickle

from drugRepoSource.get_drug_info_from_drugbank import GetDrugInfoFromDrugBank

from drugRepoSource.read_drug_info_and_clean import ReadDrugInfoAndClean
from drugRepoSource.make_label import MakeLable
from drugRepoSource.search_pubmed_with_terms import SearchMultipleTerms
from drugRepoSource.deep_nn_model import DeepModel
from drugRepoSource.plot_history import PlotHistory


class AllTogether:
    def __init__(self, already_have_data, process_drug_n, pubmed_search_ret_max, num_epochs):
        self.already_have_data = already_have_data
        self.process_drug_n = process_drug_n
        self.pubmed_search_ret_max = pubmed_search_ret_max
        self.num_epochs = num_epochs

    def run_all_together(self):

        if not self.already_have_data:
            print("Dont have data, start from ground...")

            # Search Drugbank.com and get drug info, name indication and description.
            connect_to_drugbank_web = True
            drugbank_vocabulary = "./drugbank_vocabulary.csv"
            # to produce drug_info_all.txt if already exist, skip this.
            GetDrugInfoFromDrugBank(drugbank_vocabulary=drugbank_vocabulary,
                                    process_drug_n=self.process_drug_n,
                                    connect_to_drugbank_web=connect_to_drugbank_web).get_drug_info()

            # If drug_info_all.txt already exist, jump here.
            drug_info_file = "./drug_info_all.txt"

            # Read drug info and clean it (remove drug without name, indication, description.)
            drug_info_data = ReadDrugInfoAndClean(drug_info_file).read_clean()
            print("Cleaning drugs returned ", drug_info_data.shape[0], ' drugs that have name, indication and desciption')
            print("It has shape ", drug_info_data.shape)

            # Make label for each drug, label is multi-hot indications.
            corpus = MakeLable(drug_info_data).make_label()
            print("Make label returned corpus with labels it has shape ", corpus.shape)
            print("corpus has the label with length", len(corpus.label[0]), " it means this many classes.")
            # Save corpus
            pickle_out = open("./corpus.pickle", 'wb')
            pickle.dump(corpus, pickle_out)
            pickle_out.close()
            print("Saved corpus.")
            # Read in
            pickle_in = open("./corpus.pickle", 'rb')
            corpus = pickle.load(pickle_in)
            print("Read in corpus.")

            # Search drug name to PubMed. Return abstracts,
            print()
            print("Search drug name to Pubmed for abstracts.")
            search_terms = drug_info_data.Name.tolist()
            print("Search Pubmed will return ", self.pubmed_search_ret_max, ' PMIDs.')
            print("Some drug name will not have enough PMID, so the actual PMID will be smaller.")
            print("Some PMID does not have abstract so the actual abstract will be smaller.")
            drug_abstract_all = SearchMultipleTerms(search_terms, retmax=self.pubmed_search_ret_max).search_pubmed()
            print("drug_abstract_all has shape ", drug_abstract_all.shape)
            # Save out.
            pickle_out = open("./drug_abstract_all.pickle", 'wb')
            pickle.dump(drug_abstract_all, pickle_out)
            pickle_out.close()
            print("Saved drug_abstract_all")
            # Read in
            pickle_in = open("./drug_abstract_all.pickle", "rb")
            drug_abstract_all = pickle.load(pickle_in)
            print("Read in drug_abstract_all")

            # Input abstracts and labels (for each drug) to NN model.
            # pre-process by tokenize and padding.
            print()
            print("Input abstracts and labels to NN model.")
            labels = corpus.label.tolist()
            # Save
            pickle_out = open("./labels.pickle", 'wb')
            pickle.dump(labels, pickle_out)
            pickle_out.close()
            print("Saved labels.")
            # Read in
            pickle_in = open("./labels.pickle", 'rb')
            labels = pickle.load(pickle_in)
            print("Read in labels.")
            print("labels length is ", len(labels))

            # Run deep model.
            history = DeepModel(drug_abstract_all, labels, num_epochs=self.num_epochs).model_run()
            PlotHistory(history).plot_history()
            print('Plot results pdf done.')

        elif self.already_have_data:
            print("Already have data, run deep model directly...")
            # Read in drug_abstract_all
            pickle_in = open("./drug_abstract_all.pickle", "rb")
            drug_abstract_all = pickle.load(pickle_in)

            # Read in labels
            pickle_in = open("./labels.pickle", 'rb')
            labels = pickle.load(pickle_in)

            # Run deep model.
            history = DeepModel(drug_abstract_all, labels, num_epochs=self.num_epochs).model_run()
            PlotHistory(history).plot_history()
            print('Plot results pdf done.')


def main():

    AllTogether(already_have_data=False, process_drug_n=5000, pubmed_search_ret_max=20, num_epochs=200).run_all_together()


if __name__ == '__main__':
    main()
