##################################
# Read in DrugBank xml file
##################################

import json
import xml
import pandas as pd
import numpy as np
import tensorflow as tf

class PreProcesDrugBank:
    def __init__(self, drugbank_file):
        self.drugbank_file = drugbank_file

    def read_in_xml(self):
        tf.keras.layers.Conv1D()
        pd.read_exce