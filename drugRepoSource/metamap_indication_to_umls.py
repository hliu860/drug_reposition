from drugRepoSource.metamap_map_term_to_UMLS import RunMetaMap
import os
import re
import subprocess


class IndiToUMLS:
    """
    metamap indication to UMLS
    """
    def __init__(self, drug_info_data):
        self.drug_info_data = drug_info_data
    #
    # @staticmethod
    # def check_if_metamap_server_run():
    #     ps_output = subprocess.Popen("ps", stdout=subprocess.PIPE)
    #     ps_output = str(ps_output.stdout.read())
    #
    #     if not re.search("taggerserver", ps_output):
    #         print("skrmedpostctl is not running, starting...")
    #         os.system("/Users/hl/Documents/metamap/public_mm/bin/skrmedpostctl start")
    #     else:
    #         print("taggerserver is running.")
    #
    #     if not re.search("disambServer", ps_output):
    #         print("wsdserverctl is not running, starting...")
    #         os.system("/Users/hl/Documents/metamap/public_mm/bin/wsdserverctl start")
    #     else:
    #         print("wsdserverctl is running.")

    def indi_to_umls_concept(self):
        # check if Metamap server running.
        # self.check_if_metamap_server_run()

        drug_info_data = self.drug_info_data.copy()

        indi_concept_mapped = []
        semtype_all = []
        cui_all = []
        counter = 0
        for indi in drug_info_data["Indication"]:
            counter += 1
            term = [indi]
            print(term, " ", counter, " | ", len(drug_info_data["Indication"]))

            # print(term)
            concept = RunMetaMap(term=term).run_metamap()

            # Pick concept, also look at the semtype.
            """
            "patf": Pathologic Function

            "dsyn": Disease or Syndrome

            "mobd": Mental or Behavioral Dysfunction
            "neop": Neoplastic Process
            
            "patf" -> "dsyn" -> ["neop", "mobd"]
             
             Only keep these 4 sematic types.
            """
            semtype_keep = [item in ["[patf]", "[dsyn]", "[neop]", "[mobd]"] for item in concept.semtypes]
            concept = concept[semtype_keep]
            concept.reset_index(inplace=True)

            if not concept.empty:
                indi_concept_mapped.append(concept.name[0])
                semtype_all.append(concept.semtypes[0])
                cui_all.append(concept.cui[0])
            else:
                indi_concept_mapped.append("no_disease_map")
                semtype_all.append("no_disease_map")
                cui_all.append("no_disease_map")

        drug_info_data["Indi_UMLS_concept"] = indi_concept_mapped
        drug_info_data["Semtype"] = semtype_all
        drug_info_data["cui"] = cui_all

        # remove no_disease_map
        drug_info_data = drug_info_data[[item is not "no_disease_map" for item in drug_info_data.cui]]

        # combine drug name and indication.
        drug_indi = list(zip(drug_info_data["Drug_name"], drug_info_data["Indi_UMLS_concept"]))
        drug_indi = [" ".join(item) for item in drug_indi]
        drug_info_data["Drug-Indication"] = drug_indi

        # remove duplicated drug-indi.
        drug_info_data.drop_duplicates('Drug-Indication', inplace=True)

        return drug_info_data

    def run(self):
        return self.indi_to_umls_concept()