import numpy as np
import tensorflow as tf

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


class DeepModel:
    def __init__(self, input_data_text, labels):
        self.input_data_text = input_data_text
        self.labels = labels
        self.dev_portion = 0.3
        self.embedding_dim = 100

    def pre_process(self):
        drug_abstract_all = self.input_data_text
        # print("drug_abstract_all shape is ", drug_abstract_all.shape)
        abstracts_len = [len(item) for item in drug_abstract_all.Abstract]
        padding_length = np.max(abstracts_len)
        # print("padding_length is ", padding_length)

        sentences = drug_abstract_all.Abstract.tolist()
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(sentences)

        # This will be used to get back the text from sequence.
        # word_index = tokenizer.word_index
        # vocab_size = len(word_index)
        # print()
        # print("vocab_size", vocab_size)

        sequences = tokenizer.texts_to_sequences(sentences)

        padded = pad_sequences(sequences, maxlen=padding_length, padding="post", truncating="post")

        return padded

    def divide_train_dev_test(self):
        padded = self.pre_process()
        # Split training data into train and dev.
        sample_n = padded.shape[0]
        split = int(self.dev_portion * sample_n)   # 0.3 is dev_portion, 20 is training samples (number of drugs)
        dev_data = padded[0:split]
        training_data = padded[split:sample_n]

        labels = self.labels

        dev_labels = labels[0:split]
        dev_labels = np.array(dev_labels)
        training_labels = labels[split:sample_n]
        training_labels = np.array(training_labels)

        return training_data, training_labels, dev_data, dev_labels

    def model_build(self, vocab_size, padding_length):

        class_n = len(self.labels[0])
        print("padding_length is ", padding_length)
        print('vocab_size is ', vocab_size)

        model = tf.keras.Sequential()
        model.add(tf.keras.layers.Embedding(input_dim=vocab_size+1, output_dim=self.embedding_dim, input_length=padding_length))
        # model.add(tf.keras.layers.Dropout(0.1))
        # model.add(tf.keras.layers.Conv1D(64, 5, activation="relu"))
        model.add(tf.keras.layers.Conv1D(class_n, 5, activation="relu"))
        model.add(tf.keras.layers.MaxPooling1D(pool_size=4))
        # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(class_n * 1, return_sequences=False)))

        # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)))
        # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(class_n*3, return_sequences=True)))

        # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)))
        # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(class_n*2, return_sequences=True)))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(int(class_n/2), return_sequences=True)))
        model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(class_n)))
        # model.add(tf.keras.layers.Dense(64, activation="relu"))
        # model.add(tf.keras.layers.Dropout(0.1))

        # model.add(tf.keras.layers.Flatten)
        # multi-label classification with class_n labels.
        # model.add(tf.keras.layers.Dense(class_n, activation="sigmoid"))
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

        # Get vocabulary size
        vocab_size = np.max([np.max(training_sequences), np.max(dev_sequences)])
        # Get padding length
        padding_length = len(training_sequences[0])
        # print('model run has padding length ', padding_length)

        model = self.model_build(vocab_size=vocab_size, padding_length=padding_length)

        num_epochs = 10
        history = model.fit(training_sequences, training_labels, epochs=num_epochs,
                            validation_data=(dev_sequences, dev_labels), verbose=2)
        print("Training done.")
        return history
