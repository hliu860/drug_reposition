import pickle
import warnings

from drugRepoSource.get_drug_info_from_drugbank import GetDrugInfoFromDrugBank

from drugRepoSource.read_drug_info_and_clean import ReadDrugInfoAndClean
from drugRepoSource.make_label import MakeLable
from drugRepoSource.search_pubmed_with_terms import SearchMultipleTerms
from drugRepoSource.deep_nn_model import DeepModel
from drugRepoSource.plot_history import PlotHistory
from drugRepoSource.metamap_indication_to_umls import IndiToUMLS


class AllTogether:
    def __init__(self, already_have_data, process_drug_n, pubmed_search_ret_max, num_epochs):
        self.already_have_data = already_have_data
        self.process_drug_n = process_drug_n
        self.pubmed_search_ret_max = pubmed_search_ret_max
        self.num_epochs = num_epochs

    def run_all_together(self):

        if not self.already_have_data:
            print("Dont have data, start from ground...")

            # Search Drugbank.com and get drug info, name, indication and description.
            connect_to_drugbank_web = True
            drugbank_vocabulary = "./drugbank_vocabulary.csv"
            GetDrugInfoFromDrugBank(drugbank_vocabulary=drugbank_vocabulary,
                                    process_drug_n=self.process_drug_n,
                                    connect_to_drugbank_web=connect_to_drugbank_web).get_drug_info()
            drug_info_file = "./drug_info_all.txt"

            # Read drug info and clean it (remove drug without name, indication.)
            drug_info_data = ReadDrugInfoAndClean(drug_info_file).run()
            print("Cleaning drugs returned ", drug_info_data.shape[0], ' drug-indication relations.')
            print("It has shape ", drug_info_data.shape)
            drug_info_data.to_csv("drug_info_data.txt", sep='\t')

            # print(drug_info_data)

            # Metamap indication to UMLS concept.
            print("Metamap indication to UMLS concept.")
            drug_info_data_umls = IndiToUMLS(drug_info_data).run()
            print("Metamap DONE.")
            drug_info_data_umls.to_csv("drug_info_data_map_to_umls.txt", sep="\t")
            print("drug_info_data_umls has shape ", drug_info_data_umls.shape)

            # Search drug name to PubMed. Return abstracts,
            print("Search drug name and indication name together to Pubmed for abstracts.")
            print("Search Pubmed will return ", self.pubmed_search_ret_max, ' PMIDs.')
            print("Some drug name will not have enough PMID, so the actual PMID will be smaller.")
            print("Some PMID does not have abstract so the actual abstract will be smaller.")
            search_terms = [drug_info_data_umls["Drug_name"], drug_info_data_umls["Indi_UMLS_concept"]]
            drug_abstract_all = SearchMultipleTerms(search_terms, retmax=self.pubmed_search_ret_max).search_pubmed()
            print("drug_abstract_all has shape ", drug_abstract_all.shape)

            # Make label for each drug, label is one-hot indications.
            corpus = MakeLable(drug_abstract_all).make_label()
            print("Make label returned corpus with shape ", corpus.shape)
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

            """
               Run deep model.
            """
            # Input abstracts and labels  to NN model, pre-process by tokenize and padding.
            print("Input abstracts and labels to NN model.")
            abstracts = corpus.Abstract.tolist()
            labels = corpus.label.tolist()
            history = DeepModel(input_data_text=abstracts, labels=labels, num_epochs=self.num_epochs).model_run()
            PlotHistory(history).plot_history()
            print('Plot results pdf done.')

        elif self.already_have_data:
            print("Already have data, run deep model directly...")
            # Read in corpus
            pickle_in = open("./corpus.pickle", 'rb')
            corpus = pickle.load(pickle_in)
            abstracts = corpus.Abstract.tolist()
            labels = corpus.label.tolist()
            history = DeepModel(input_data_text=abstracts, labels=labels, num_epochs=self.num_epochs).model_run()
            PlotHistory(history).plot_history()
            print('Plot results pdf done.')


def main():
    warnings.filterwarnings("ignore", category=FutureWarning)
    AllTogether(already_have_data=False, process_drug_n=5, pubmed_search_ret_max=10, num_epochs=10).run_all_together()


if __name__ == '__main__':
    main()
