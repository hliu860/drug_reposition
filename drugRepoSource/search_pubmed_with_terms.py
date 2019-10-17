import pandas as pd

from drugRepoSource.pubmed_search import PubMedBiopython


class SearchMultipleTerms:
    def __init__(self, terms):
        self.search_terms = terms
        self.get_abstract_n = 10
        self.padding_length = 4000

    def search_pubmed(self):
        drug_abstract_all = pd.DataFrame()
        for search_term in self.search_terms:
            print()
            print(search_term)
            article_pd = PubMedBiopython(search_term).search_pubmed()
            print(article_pd.shape)
            print("Only take ", self.get_abstract_n, " abstracts for test.")

            sentences = article_pd.abstract.tolist()
            sentences_combine = " ".join(sentences[:self.get_abstract_n])   # take first 10 abstracts.
            term_abstract = pd.Series({"Drug": search_term, "Abstract": sentences_combine})

            drug_abstract_all = drug_abstract_all.append(term_abstract, ignore_index=True)

        return drug_abstract_all
