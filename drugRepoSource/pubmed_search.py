import xml.etree.cElementTree as ET
from Bio import Entrez
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


# for debug
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 6000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(linewidth=300)


class PubMedBiopython:
    def __init__(self, query_term, retmax):
        self.qeury_term = query_term
        self.retmax = retmax

    def search_pubmed(self):
        Entrez.email = 'hliu860@gmail.com'

        # Search term and retrieve Pubmed ID list
        e_search = Entrez.esearch(db="pubmed", retmax=self.retmax, term=self.qeury_term)
        res_search = Entrez.read(e_search)
        e_search.close()
        id_list = res_search["IdList"]
        # print("Search Pubmed returned ", len(id_list), ' PMIDs.')
        id_string = ", ".join(id_list)

        # Fetch data
        handle = Entrez.efetch(db='pubmed', id=id_string, retmode='xml')
        data = Entrez.read(handle)

        articles = data['PubmedArticle']
        article_pd = pd.DataFrame()
        for article in articles:
            medline_cit = article['MedlineCitation']
            """OtherAbstract has abstract of other language"""
            medline_art = medline_cit['Article']

            # make sure it has abstract
            if "Abstract" in medline_art.keys():
                # make sure date is available.
                # Collect info.
                art_pmid = medline_cit['PMID']
                # print(art_pmid)
                # art_lan = medline_art['Language'][0]
                art_title = medline_art['ArticleTitle']
                art_abstract = medline_art['Abstract']['AbstractText']
                art_abstract = ' '.join(art_abstract)
                # print(medline_art['ArticleDate'])
                # art_date = medline_art['ArticleDate'][0]

                art_series = pd.Series({
                    'pmid': art_pmid,
                    # 'Original_language': art_lan,
                    # 'year': art_date['Year'],
                    'title': art_title,
                    'abstract': art_abstract
                }
                )
                article_pd = article_pd.append(art_series, ignore_index=True)

                # if medline_art['ArticleDate']:  # means it is not empty list []

        # print(article_pd)

        handle.close()
        return article_pd


def main():
    # search_term = "Acetaminophen"
    search_term = "Interferon alfa-n3"
    article_pd = PubMedBiopython(search_term).search_pubmed()
    print(article_pd)
    print(article_pd.shape)


if __name__ == '__main__':
    main()


