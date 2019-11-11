import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class PlotHistory:
    def __init__(self, history):
        self.history = history

    def plot_history(self):
        # -----------------------------------------------------------
        # Retrieve a list of list results on training and test data
        # sets for each training epoch
        # -----------------------------------------------------------
        acc = self.history.history['acc']
        val_acc = self.history.history['val_acc']
        loss = self.history.history['loss']
        val_loss = self.history.history['val_loss']

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
