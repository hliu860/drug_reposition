from drugRepoSource.get_drug_info import GetDrugInfo
import drugRepoSource.NN_model as drugbank_nn
import drugRepoSource.nn_model_pubmed as nn_pubmed

# for debug
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 6000)
# pd.set_option('display.max_colwidth', -1)
# np.set_printoptions(linewidth=300)


def main():
<<<<<<< HEAD
    GetDrugInfo("./drugbank_vocabulary.csv").get_drug_info()
    drug_info_file = "./drug_info_all.txt"
    drug_info_data = drugbank_nn.ReadDrugInfo(drug_info_file).read_clean()
    # print(drug_info_data.shape)
    drug_info_data = drug_info_data[:20]

    corpus = drugbank_nn.DeepModel(drug_info_data).make_label()
    print("corpus shape", corpus.shape)

    search_terms = drug_info_data.Name.tolist()
    abstract_all_padded = nn_pubmed.SearchMultipleTerms(search_terms).pre_process()

    labels = corpus.label.tolist()
    history = nn_pubmed.DeepModel(abstract_all_padded, labels).model_run()
    print(history)
    nn_pubmed.DeepModel.plot_history(history)
=======
    connect_to_drugbank_web = False  # This only needs to run once.
    process_drug_n = 1000    # max is

    if connect_to_drugbank_web:
        # Get DrugBank ID.
        drug_ids = GetDrugBankID("./drugbank_vocabulary.csv").read_file()
        drug_ids = drug_ids.tolist()
        drug_ids = drug_ids[:process_drug_n]
        # print(drug_ids)

        # Get drug info.
        drug_info_all = pd.DataFrame()
        counter = 0
        for drug_id in drug_ids:
            counter += 1
            if counter % 10 == 0:
                print(counter)
            drug_name, drug_indi, drug_des = GetConditionFromDrugBank(drug_id).get_info()
            drug_indi = "/".join(drug_indi)
            drug_info_one = pd.DataFrame({"Drug_id": drug_id,
                                          "Name": drug_name,
                                          "Indications-DrugBank": drug_indi,
                                          "Description": drug_des},
                                         index=range(1))
            drug_info_all = drug_info_all.append(drug_info_one, ignore_index=True)
        drug_info_all.to_csv("../drug_info_all.txt", sep="\t")
        # print(drug_info_all)

    # Run NN model
    drug_info_file = "../drug_info_all.txt"
    drug_info_data = ReadDrugInfo(drug_info_file).read_clean()
    history = DeepModel(drug_info_data).model_run()
    DeepModel(drug_info_data).plot_history(history)
>>>>>>> 5322ed4ad6b8e9a9a8c0ce386ec9ec60431ea07a


if __name__ == '__main__':
    main()
