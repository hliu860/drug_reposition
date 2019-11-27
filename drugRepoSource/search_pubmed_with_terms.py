import pandas as pd

# from drugRepoSource.pubmed_search import PubMedBiopython
from drugRepoSource.pubmed_search_local import PubmedLocal


class SearchMultipleTerms:
    def __init__(self, terms, retmax, pubmed_local_path):
        self.search_terms = terms
        self.retmax = retmax
        self.abs_n_keep = 1
        self.pubmed_local_path = pubmed_local_path

    def search_pubmed(self):
        search_terms = self.search_terms
        drug_name = search_terms[0]
        indication = search_terms[1]

        drug_name_search_field = [item + " " + "[TIAB]" for item in drug_name]
        indi_search_field = [item + " " + "[TIAB]" for item in indication]

        drug_indi = list(zip(drug_name_search_field, indi_search_field))
        drug_indi_terms = [" ".join(item) for item in drug_indi]

        drug_abstract_all = pd.DataFrame()
        for index, search_term in enumerate(drug_indi_terms):

            print(search_term, " ", index + 1, " | ", len(drug_indi_terms))

            # article_pd = PubMedBiopython(search_term, retmax=self.retmax).search_pubmed()

            # Search local pubmed archive
            article_pd = PubmedLocal(pubmed_local_path=self.pubmed_local_path, query_term=search_term,
                                     retmax=self.retmax).run()
            # print(article_pd)

            if not article_pd.empty:
                sentences = article_pd.abstract.tolist()
                sentences_combine = " ".join(sentences)   # take first 10 abstracts.

                drug_keep = search_term.split(" [TIAB] ")[0]
                indi_keep = search_term.split(" [TIAB] ")[1].split(" [TIAB]")[0]
                term_abstract = pd.Series({"Drug-indication-search": search_term,
                                           "Abstract": sentences_combine,
                                           "Abs_n": int(len(sentences)),
                                           "Drug": drug_keep,
                                           "Indication": indi_keep,
                                           "Drug-Indi": drug_keep + " " + indi_keep})

                drug_abstract_all = drug_abstract_all.append(term_abstract, ignore_index=True)
            else:
                term_abstract = pd.Series({"Drug-indication-search": "no_return",
                                           "Abstract": "no_return",
                                           "Abs_n": 0,
                                           "Drug": 'no_return',
                                           "Indication": "no_return",
                                           "Drug-Indi": 'no_return'})
                drug_abstract_all = drug_abstract_all.append(term_abstract, ignore_index=True)

        # Filter abstract
        print("Filter pubmed search results, discard if return less than ", self.abs_n_keep, " abs.")
        print("and discard if pubmed has no return using search term.")
        print("Search term is drug [TIAB] indication [TIAB]")
        abs_keep = [item is not "no_return" for item in drug_abstract_all["Abstract"]]
        abs_n_keep = [item > self.abs_n_keep for item in drug_abstract_all["Abs_n"]]
        abs_filter = [x and y for x, y in zip(abs_keep, abs_n_keep)]

        drug_abstract_all = drug_abstract_all[abs_filter]
        drug_abstract_all.reset_index(inplace=True)

        # print(drug_abstract_all)
        return drug_abstract_all
