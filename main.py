import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication

import main_qt
from passage_retrieval import PassageRetrieval
from similarity import Similarity


class ExampleApp(QtWidgets.QMainWindow, main_qt.Ui_FMain):
    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)


def main():
    """" aplikasi utama """

    app = QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()

def main2():

    """ objek passage retrieval (pr) dan similaritas (sim) """
    pr = PassageRetrieval()
    sim = Similarity()
    # sim.demo()

    """ parameter default untuk PassageRetrieval """
    wiki_top_n = 10
    jml_min_kalimat = 5
    jml_maks_kalimat = 20 #1000

    """ parameter default untuk Similarity """
    top_n = 10 # maks_hasil

    """ kueri dan dokumen """
    kueri = "siapa nama presiden indonesia pertama"
    dok_kalimat = pr.ambil_teks_online(kueri, wiki_top_n, jml_min_kalimat, jml_maks_kalimat)

    """ hitung similaritas dokumen dan kueri """
    data_cs = sim.cosine_similarity_tf_idf(dok_kalimat, kueri.lower(), top_n)
    # data_bm25 = sim.bm_25(dok_kalimat, kueri.lower(), "BM25", top_n)

    """ cetak hasil similaritas, diurutkan berdasarkan peringkat tertinggi """
    print("Kueri\t:", kueri)
    print("\r")
    for i, d in enumerate(data_cs):
    # for i, d in enumerate(data_bm25):
        print("{}.\t {:.2f}\t: {}".format(i + 1, d[0], d[1]))


if __name__ == '__main__':
    main()
