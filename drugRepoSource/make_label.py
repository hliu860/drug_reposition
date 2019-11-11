from sklearn.preprocessing import MultiLabelBinarizer


class MakeLable:
    def __init__(self, drug_abstract_all):
        self.drug_abstract_all = drug_abstract_all

    def make_label(self):
        """Label is the condition that drug can treat."""
        corpus = self.drug_abstract_all.copy()
        # print(corpus)

        cui = [item.split("/") for item in corpus["Indication"]]   # Though it uses multilabel, it is in fact one hot encoding.
        # print(cui)
        # cui = corpus["cui"]
        mlb = MultiLabelBinarizer()
        indications_binary = mlb.fit_transform(cui)

        corpus["label"] = indications_binary.tolist()
        # print(corpus)
        return corpus
