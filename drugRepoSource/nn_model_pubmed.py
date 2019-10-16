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

from drugRepoSource.pubmed_search import PubMedBiopython
import drugRepoSource.NN_model as drugbank_nn


# for debug
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 6000)
pd.set_option('display.max_colwidth', -1)
np.set_printoptions(linewidth=300)


class SearchMultipleTerms:
    def __init__(self, terms):
        self.search_terms = terms
        self.get_abstract_n = 10

    def search_pubmed(self):
        drug_abstract_all = pd.DataFrame()
        for search_term in self.search_terms:
            article_pd = PubMedBiopython(search_term).search_pubmed()
            print(search_term)
            print(article_pd.shape)

            sentences = article_pd.abstract.tolist()
            sentences_combine = " ".join(sentences[:self.get_abstract_n])   # take first 10 abstracts.
            term_abstract = pd.Series({"Drug": search_term, "Abstract": sentences_combine})

            drug_abstract_all = drug_abstract_all.append(term_abstract, ignore_index=True)

        return drug_abstract_all

    def pre_process(self):
        drug_abstract_all = self.search_pubmed()

        sentences = drug_abstract_all.Abstract.tolist()
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(sentences)
        word_index = tokenizer.word_index

        vocab_size = len(word_index)
        print()
        print("vocab_size", vocab_size)

        sequences = tokenizer.texts_to_sequences(sentences)

        padded = pad_sequences(sequences, maxlen=4000, padding="post", truncating="post")

        # print(padded.shape)

        return padded


class DeepModel:
    def __init__(self, input_data, labels):
        self.input_data = input_data
        self.labels = labels
        self.training_sample = len(labels)
        self.dev_portion = 0.3

        self.embedding_dim = 100

    def divide_train_dev_test(self):
        # Split training data into train and dev.

        # print('\n\n\n')
        split = int(self.dev_portion * self.training_sample)   # 0.3 is dev_portion, 20 is training samples (number of drugs)
        # print(split)
        dev_data = self.input_data[0:split]
        training_data = self.input_data[split:self.training_sample]

        labels = self.labels

        dev_labels = labels[0:split]
        dev_labels = np.array(dev_labels)
        training_labels = labels[split:self.training_sample]
        training_labels = np.array(training_labels)

        # print(training_data.shape)
        # print(dev_data.shape)
        # print(len(training_labels))
        # print(len(dev_labels))

        return training_data, training_labels, dev_data, dev_labels

    def model_build(self):
        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Embedding(input_dim=10000+1, output_dim=100, input_length=4000))
        model.add(tf.keras.layers.Dropout(0.1))
        model.add(tf.keras.layers.Conv1D(64, 5, activation="relu"))
        model.add(tf.keras.layers.MaxPooling1D(pool_size=4))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)))
        model.add(tf.keras.layers.Dense(64, activation="relu"))
        model.add(tf.keras.layers.Dropout(0.1))

        # multi-label classification with class_n labels.
        # model.add(tf.keras.layers.Dense(class_n, activation="sigmoid"))
        class_n = len(self.labels[0])
        model.add(tf.keras.layers.Dense(class_n, activation="softmax"))
        # model.add(tf.keras.layers.Dense(1, activation="sigmoid"))

        # metric_use = tf.keras.metrics.BinaryAccuracy()   # ???????????????????
        # metric_use = tf.keras.metrics.Accuracy()   # ???????????????????
        # model.compile(loss="binary_crossentropy", optimizer="adam", metrics=['accuracy'])
        model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=['accuracy'])
        # model.compile(loss="binary_crossentropy", optimizer="adam", metrics=[metric_use])
        print(model.summary())
        return model

    def model_run(self):
        training_sequences, training_labels, dev_sequences, dev_labels = self.divide_train_dev_test()
        model = self.model_build()

        num_epochs = 10
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
    drug_info_file = "../../drug_info_all.txt"
    drug_info_data = drugbank_nn.ReadDrugInfo(drug_info_file).read_clean()
    # print(drug_info_data.shape)
    drug_info_data = drug_info_data[:20]

    corpus = drugbank_nn.DeepModel(drug_info_data).make_label()
    print("corpus shape", corpus.shape)

    search_terms = drug_info_data.Name.tolist()
    abstract_all_padded = SearchMultipleTerms(search_terms).pre_process()

    labels = corpus.label.tolist()
    history = DeepModel(abstract_all_padded, labels).model_run()
    print(history)
    DeepModel.plot_history(history)


if __name__ == '__main__':
    main()
