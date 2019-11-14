import pandas as pd
from pymetamap import MetaMap
import subprocess
import re
import os
import sys
import string


"""
Under conda env tf14.

  Run this first to start metamap
        skrmedpostctl start
        wsdserverctl start

        to stop
        skrmedpostctl stop
        wsdserverctl stop
"""


class RunMetaMap:
    def __init__(self, term):
        self.term = term
        if sys.platform == "darwin":
            self.metamap_bin = "/Users/hl/Documents/metamap/public_mm/bin/metamap"
        elif sys.platform == "linux":
            self.metamap_bin = '/home/lhp/Documents/public_mm/bin/metamap'

    def run_metamap(self):
        mm = MetaMap.get_instance(self.metamap_bin)
        sentence = self.term
        printable = set(string.printable)
        sent_filtered = ["".join(filter(lambda x: x in printable, item)) for item in sentence]
        sentence = sent_filtered

        concepts, error = mm.extract_concepts(
            sentences=sentence, compute_all_mappings=False,
            prefer_multiple_concepts=False,
            mm_data_version="USAbase", term_processing=True,
            word_sense_disambiguation=True, silent=True)

        concept_term = pd.DataFrame({"name": None, "cui": None, "score": None, "semtypes": None}, index=range(0))
        for index, concept in enumerate(concepts):
            # print()
            # print(index)
            # print(concept)
            if type(concept).__name__ is "ConceptMMI":
                # print(type(concept).__name__)
                # print(concept.preferred_name)
                concept_series = pd.Series({"name": concept.preferred_name, "cui": concept.cui,
                                            "score": concept.score, "semtypes": concept.semtypes})
                # print(concept_series)
                concept_term = concept_term.append(concept_series, ignore_index=True)
                # print(concept_term)
                # print()

        concept_term.score = [float(item) for item in concept_term.score]   # make score float.
        concept_term.sort_values(by="score", ascending=False, inplace=True)  # sort by score.

        return concept_term


def main():
    term = ['Cystic Fibrosis (CF)']
    # term = ["heart attack"]
    # term = ["Metastatic Colorectal Cancers"]
    # term = ["Metastatic Squamous Cell Carcinoma of the Head and Neck"]
    # term = ["Advanced squamous cell carcinoma of the head and neck"]
    # term = ["Advanced Head and Neck Squamous Cell Carcinoma"]
    # term = ["Cutaneous T-Cell Lymphoma (CTCL)"]
    # term = ["Acute Coronary Syndromes (ACS)"]
    # term = ["Thrombotic events"]
    # term = ["Juvenile Idiopathic Arthritis (JIA)"]
    # term = ["Anemias"]
    # term = ["Chronic Hepatitis C Virus (HCV) Infection"]
    # term = ["Melanoma"]
    # term = ["Acute Lymphoblastic Leukaemias (ALL)"]
    # term = ["Thyroid Cancers"]  # cancers needs to be changed to cancer
    concept_term = RunMetaMap(term=term).run_metamap()
    print("\n\nFinal")
    print(concept_term)


if __name__ == '__main__':
    main()
