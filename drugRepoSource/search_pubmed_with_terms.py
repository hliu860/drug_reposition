import pandas as pd

from drugRepoSource.pubmed_search import PubMedBiopython


class SearchMultipleTerms:
    def __init__(self, terms, retmax):
        self.search_terms = terms
        self.retmax = retmax

    def search_pubmed(self):
        drug_abstract_all = pd.DataFrame()
        for search_term in self.search_terms:
            print()
            print(search_term)
            article_pd = PubMedBiopython(search_term, retmax=self.retmax).search_pubmed()
            print(article_pd.shape)

            sentences = article_pd.abstract.tolist()
            sentences_combine = " ".join(sentences)   # take first 10 abstracts.

            term_abstract = pd.Series({"Drug": search_term, "Abstract": sentences_combine})

            drug_abstract_all = drug_abstract_all.append(term_abstract, ignore_index=True)

        return drug_abstract_all
