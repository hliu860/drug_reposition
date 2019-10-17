from sklearn.preprocessing import MultiLabelBinarizer


class MakeLable:
    def __init__(self, drug_info_data):
        self.drug_info_data = drug_info_data

    def make_label(self):
        """Label is the condition that drug can treat."""
        corpus = self.drug_info_data.copy()

        indications = [item.split("/") for item in corpus["Indications-DrugBank"]]
        mlb = MultiLabelBinarizer()
        indications_binary = mlb.fit_transform(indications)

        corpus["label"] = indications_binary.tolist()

        return corpus
