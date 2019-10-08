
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


class ReadDrugInfo:
    def __init__(self, drug_info_file):
        self.drug_info = drug_info_file

    def read_clean(self):
        info_data = pd.read_csv(self.drug_info, sep="\t", index_col=0)
        
        # remove drugs without indication.
        drug_indi = info_data["Indications-DrugBank"].tolist()
        info_data = info_data.loc[[str(x) != "nan" for x in drug_indi]]
        
        # remove drug with name
        drug_name = info_data["Name"].tolist()
        info_data = info_data.loc[[str(x) != "nan" for x in drug_name]]
        
        # remove drugs without description
        drug_des = info_data["Description"]
        info_data = info_data.loc[[str(x) != 'nan' for x in drug_des]]
        info_data.reset_index(drop=True, inplace=True)

        return info_data


class DeepModel:
    def __init__(self, drug_info_data):
        self.drug_info_data = drug_info_data
        self.embedding_dim = 100
        self.max_length = 200
        self.trunc_type = 'post'
        self.padding_type = 'post'
        self.oov_tok = '<OOV>'
        self.sample_n = self.drug_info_data.shape[0]
        self.training_size = int(self.sample_n * 0.6)   # 0.6 for train and 0.4 for test.
        self.dev_porting = 0.3   # within train, 0.3 for dev.
        # So 0.36 for train, 0.24 for dev and 0.4 for test.

    def make_label(self):
        """Label is the condition that drug can treat."""
        corpus = self.drug_info_data.copy()

        indications = [item.split("/") for item in corpus["Indications-DrugBank"]]
        # print(indications)
        mlb = MultiLabelBinarizer()
        indications_binary = mlb.fit_transform(indications)
        # print(*list(mlb.classes_), sep="\n")
        # print(len(list(mlb.classes_)))

        corpus["label"] = indications_binary.tolist()

        # total number of indications
        # how many classes means how many indications.
        global class_n
        class_n = len(indications_binary[0])

        # print(len(indications_binary))
        # print(len(indications_binary[0]))
        # print(corpus)

        return corpus

    def prepare_text(self):     
        corpus = self.make_label()

        # Get sentences and labels
        sentences = []
        labels = []
        corpus = corpus.sample(frac=1, random_state=1).reset_index(drop=True)

        # print(corpus)

        for i in range(self.training_size):
            sentences.append(corpus.loc[i, "Description"])
            labels.append(corpus.loc[i, "label"])
        
        # Tokenize
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(sentences)
        word_index = tokenizer.word_index

        global vocab_size
        vocab_size = len(word_index)
        
        # Make text to sequence
        sequences = tokenizer.texts_to_sequences(sentences)
        
        # Padding
        padded = pad_sequences(sequences, maxlen=self.max_length,
                               padding=self.padding_type, truncating=self.trunc_type)

        # Split training data into train and dev.
        split = int(self.dev_porting * self.training_size)
        dev_sequences = padded[0:split]
        training_sequences = padded[split:self.training_size]

        dev_labels = labels[0:split]
        dev_labels = np.array(dev_labels)
        training_labels = labels[split:self.training_size]
        training_labels = np.array(training_labels)

        return training_sequences, training_labels, dev_sequences, dev_labels

    def model_build(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Embedding(vocab_size+1, self.embedding_dim, input_length=self.max_length))
        model.add(tf.keras.layers.Dropout(0.1))
        model.add(tf.keras.layers.Conv1D(64, 5, activation="relu"))
        model.add(tf.keras.layers.MaxPooling1D(pool_size=4))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)))
        model.add(tf.keras.layers.Dense(64, activation="relu"))
        model.add(tf.keras.layers.Dropout(0.1))

        # multi-label classification with class_n labels.
        model.add(tf.keras.layers.Dense(class_n, activation="sigmoid"))

        model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
        print(model.summary())
        return model

    def model_run(self):
        training_sequences, training_labels, dev_sequences, dev_labels = self.prepare_text()
        model = self.model_build()

        num_epochs = 50
        history = model.fit(training_sequences, training_labels, epochs=num_epochs,
                            validation_data=(dev_sequences, dev_labels), verbose=2)
        print("Training done.")
        return history

    @staticmethod
    def plot_history(history):
        history = history

        # -----------------------------------------------------------
        # Retrieve a list of list results on training and test data
        # sets for each training epoch
        # -----------------------------------------------------------
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        loss = history.history['loss']
        val_loss = history.history['val_loss']

        epochs = range(len(acc))  # Get number of epochs

        with PdfPages("./model_res.pdf") as pdf:

            # ------------------------------------------------
            # Plot training and validation accuracy per epoch
            # ------------------------------------------------
            plt.figure(figsize=(10, 10))
            plt.plot(epochs, acc, 'r')
            plt.plot(epochs, val_acc, 'b')
            plt.title('Training and validation accuracy')
            plt.xlabel("Epochs")
            plt.ylabel("Accuracy")
            plt.legend(["Accuracy", "Validation Accuracy"])

            pdf.savefig()
            plt.close()

            # ------------------------------------------------
            # Plot training and validation loss per epoch
            # ------------------------------------------------
            plt.figure(figsize=(10, 10))
            plt.plot(epochs, loss, 'r')
            plt.plot(epochs, val_loss, 'b')
            plt.title('Training and validation loss')
            plt.xlabel("Epochs")
            plt.ylabel("Loss")
            plt.legend(["Loss", "Validation Loss"])

            pdf.savefig()
            plt.close()
            #


def main():
    drug_info_file = "../drug_info_all.txt"
    drug_info_data = ReadDrugInfo(drug_info_file).read_clean()
    history = DeepModel(drug_info_data).model_run()
    DeepModel(drug_info_data).plot_history(history)


if __name__ == '__main__':
    main()
