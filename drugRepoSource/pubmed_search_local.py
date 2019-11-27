from Bio import Entrez
import time
import pandas as pd
import numpy as np
import subprocess
import shlex
import io
import sys
import os


# for debug
# pd.set_option('display.max_rows', 500)
# pd.set_option('display.max_columns', 500)
# pd.set_option('display.width', 6000)
# pd.set_option('display.max_colwidth', -1)
# np.set_printoptions(linewidth=300)


class PubmedLocal:
    def __init__(self, pubmed_local_path, query_term, retmax=10, past_years=30):
        self.pubmed_local_path = pubmed_local_path
        self.retmax = retmax
        self.past_years = past_years
        self.past_days = self.past_years * 365
        self.query_term = query_term

    @staticmethod
    def read_shell(command, shell=False, **kwargs):
        """
        Takes a shell command as a string and reads the result into a Pandas DataFrame.

        Additional keyword arguments are passed through to pandas.read_csv.

        :param command: a shell command that returns tabular data
        :type command: str
        :param shell: passed to subprocess.Popen
        :type shell: bool

        :return: a pandas dataframe
        :rtype: :class:`pandas.dataframe`
        """
        proc = subprocess.Popen(command,
                                shell=shell,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        output, error = proc.communicate()

        if proc.returncode == 0:
            with io.StringIO(output.decode()) as buffer:
                return pd.read_csv(buffer, **kwargs, engine='python')
        else:
            message = ("Shell command returned non-zero exit status: {0}\n\n"
                       "Command was:\n{1}\n\n"
                       "Standard error was:\n{2}")
            raise IOError(message.format(proc.returncode, command, error.decode()))



    def command_list(self):
        cmd_list = ["esearch", "-db", "pubmed", "-days", str(self.past_days), "-query", "\"", self.query_term, "\"",
                    "|", "efetch", "-format", "uid", "-start", "0", "-stop", str(self.retmax),
                    "|", "fetch-pubmed", "-path", self.pubmed_local_path,
                    "|", "xtract", "-pattern", "PubmedArticle",
                    "-element",
                    "MedlineCitation/PMID"]
        return cmd_list

    def fetch_local_abstract(self):
        cmd_list = self.command_list()
        cmd_list.append("Abstract/AbstractText")
        cmd_raw = " ".join(cmd_list)
        shell_out = self.read_shell(cmd_raw, shell=True, header=None, sep="--------")  # sep is to make sure 1 column
        return shell_out

    def fetch_local_title(self):
        cmd_list = self.command_list()
        cmd_list.append("ArticleTitle")
        cmd_raw = " ".join(cmd_list)
        shell_out = self.read_shell(cmd_raw, shell=True, header=None, sep="--------")  # sep is to make sure 1 column
        return shell_out

    def fetch_combine(self):
        pubmed_abstract = self.fetch_local_abstract()
        pubmed_abstract.columns = ['pmid_abstract']

        pubmed_title = self.fetch_local_title()
        pubmed_title.columns = ["pmid_title"]

        pubmed_title["pmid"] = [item.split("\t")[0] for item in pubmed_title["pmid_title"]]
        pubmed_title["title"] = [" ".join(item.split("\t")[1:]) for item in pubmed_title["pmid_title"]]

        pubmed_abstract["pmid"] = [item.split("\t")[0] for item in pubmed_abstract["pmid_abstract"]]
        pubmed_abstract["abstract"] = [" ".join(item.split("\t")[1:]) for item in pubmed_abstract["pmid_abstract"]]

        pubmed_output = pd.merge(left=pubmed_title, right=pubmed_abstract, how='inner', on="pmid")
        pubmed_output = pubmed_output[["pmid", "title", "abstract"]]

        return pubmed_output

    def run(self):
        try:
            pubmed_out = self.fetch_combine()
            print(pubmed_out.shape)
            return pubmed_out
        except:
            print("no pubmed output")
            return pd.DataFrame()  # return empty dataframe.


def main():
    os.chdir("../test/")

    query_term = "breast cancer [TIAB] cold [TIAB]"
    retmax = 200000
    past_years = 30
    pubmed_local_path = "/Volumes/pubmedlocal"
    pubmed_output = PubmedLocal(pubmed_local_path, query_term, retmax, past_years).run()

    # print(pubmed_output)
    print(pubmed_output.shape)


if __name__ == '__main__':
    main()
