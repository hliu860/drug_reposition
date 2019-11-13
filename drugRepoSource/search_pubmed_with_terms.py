import pandas as pd

from drugRepoSource.pubmed_search import PubMedBiopython


class SearchMultipleTerms:
    def __init__(self, terms, retmax):
        self.search_terms = terms
        self.retmax = retmax
        self.abs_n_keep = 5

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
            # drug_search = drug_name[index]
            # indi_search = indication[index]

            # print()
            # print(search_term)
            article_pd = PubMedBiopython(search_term, retmax=self.retmax).search_pubmed()
            # print(article_pd.shape)

            sentences = article_pd.abstract.tolist()
            sentences_combine = " ".join(sentences)   # take first 10 abstracts.

            term_abstract = pd.Series({"Drug-indication-search": search_term,
                                       "Abstract": sentences_combine,
                                       "Abs_n": int(len(sentences)),
                                       "Drug": search_term.split("[TIAB]")[0],
                                       "Indication": search_term.split("[TIAB]")[1]})

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
