# -*- coding: utf-8 -*-
import sys
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal, QRect
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox, QLabel

from document_retrieval import IRWikipedia, IRMesinPencari
from pemroses_teks import PemrosesTeks
from similarity import Similarity


# Form implementation generated from reading ui file 'main_qt.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


class Thread(QThread):
    _signal_status = pyqtSignal(str)
    _signal_pbar = pyqtSignal(int)
    _signal_hasil = pyqtSignal(list)
    _params = []

    def __init__(self, params):
        super(Thread, self).__init__()
        self._params = params

    def __del__(self):
        self.wait()

    def run(self):
        teks = self._params[0]
        top_wiki = self._params[1]
        min_kal = self._params[2]
        max_kal = self._params[3]
        max_hsl = self._params[4]
        no_mp = self._params[5]
        no_metode = self._params[6]

        """ kueri dan dokumen """
        pt = PemrosesTeks()
        kueri = pt.pemrosesan_kueri(teks)

        self._signal_status.emit('Ambil data dari Wikipedia... (online)')
        self._signal_pbar.emit(25)
        wp = IRWikipedia()
        teks_wp = wp.teks_wikipedia(kueri, top_wiki)

        self._signal_status.emit('Ambil data dari Mesin Pencari... (online)')
        self._signal_pbar.emit(50)
        mp = IRMesinPencari()
        teks_mp = mp.teks_mesin_pencari(kueri, no_mp)

        self._signal_status.emit('Pemrosesan teks...')
        self._signal_pbar.emit(75)
        time.sleep(3)
        teks_gabung = pt.gabung_teks(teks_wp, teks_mp)
        kalimat = pt.penghilang_derau(teks_gabung)
        kalimat = pt.tokenisasi_kalimat(kalimat)
        kalimat = pt.filter_kalimat(kalimat, min_kal, max_kal)

        """ similarity """
        self._signal_status.emit('Hitung nilai kemiripan...')
        self._signal_pbar.emit(90)
        time.sleep(3)
        sim = Similarity()
        match no_metode:
            case 0:
                hasil_sim = sim.cosine_similarity_tf_idf(kalimat, teks.lower(), max_hsl)
            case 1:
                hasil_sim = sim.bm_25(kalimat, kueri.lower(), "BM25", max_hsl)
            case 2:
                hasil_sim = sim.bm_25(kalimat, kueri.lower(), "BM25L", max_hsl)
            case 3:
                hasil_sim = sim.bm_25(kalimat, kueri.lower(), "BM25+", max_hsl)

        # ===================

        self._signal_pbar.emit(99)
        self._signal_status.emit('Idle')
        self._signal_hasil.emit(hasil_sim)


class Ui_FMain(object):
    def setupUi(self, FMain):
        FMain.setObjectName("FMain")
        FMain.resize(477, 535)
        self.centralwidget = QtWidgets.QWidget(FMain)
        self.centralwidget.setObjectName("centralwidget")
        self.Tab = QtWidgets.QTabWidget(self.centralwidget)
        self.Tab.setGeometry(QtCore.QRect(9, 10, 461, 471))
        self.Tab.setObjectName("Tab")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(12, 20, 171, 16))
        self.label.setObjectName("label")
        self.LE_kalimat_tanya = QtWidgets.QLineEdit(self.tab)
        self.LE_kalimat_tanya.setGeometry(QtCore.QRect(10, 40, 431, 28))
        self.LE_kalimat_tanya.setText("")
        # self.LE_kalimat_tanya.setText("siapa nama presiden indonesia pertama")
        self.LE_kalimat_tanya.setClearButtonEnabled(True)
        self.LE_kalimat_tanya.setObjectName("LE_kalimat_tanya")
        self.groupBox = QtWidgets.QGroupBox(self.tab)
        self.groupBox.setGeometry(QtCore.QRect(10, 80, 431, 261))
        self.groupBox.setObjectName("groupBox")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(20, 46, 101, 16))
        self.label_8.setObjectName("label_8")
        self.CB_mesin_pencari = QtWidgets.QComboBox(self.groupBox)
        self.CB_mesin_pencari.setGeometry(QtCore.QRect(19, 61, 211, 28))
        self.CB_mesin_pencari.setObjectName("CB_mesin_pencari")
        self.CB_mesin_pencari.addItem("")
        self.CB_mesin_pencari.addItem("")
        self.CB_mesin_pencari.addItem("")
        self.CB_mesin_pencari_2 = QtWidgets.QComboBox(self.groupBox)
        self.CB_mesin_pencari_2.setGeometry(QtCore.QRect(19, 135, 211, 28))
        self.CB_mesin_pencari_2.setObjectName("CB_mesin_pencari_2")
        self.CB_mesin_pencari_2.addItem("")
        self.CB_mesin_pencari_2.addItem("")
        self.CB_mesin_pencari_2.addItem("")
        self.CB_mesin_pencari_2.addItem("")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(20, 120, 141, 16))
        self.label_10.setObjectName("label_10")
        self.LE_min_kalimat = QtWidgets.QLineEdit(self.groupBox)
        self.LE_min_kalimat.setGeometry(QtCore.QRect(260, 65, 151, 28))
        self.LE_min_kalimat.setMaxLength(5)
        self.LE_min_kalimat.setClearButtonEnabled(True)
        self.LE_min_kalimat.setObjectName("LE_min_kalimat")
        self.LE_max_hasil = QtWidgets.QLineEdit(self.groupBox)
        self.LE_max_hasil.setGeometry(QtCore.QRect(260, 205, 151, 28))
        self.LE_max_hasil.setMaxLength(5)
        self.LE_max_hasil.setClearButtonEnabled(True)
        self.LE_max_hasil.setObjectName("LE_max_hasil")
        self.LE_max_kalimat = QtWidgets.QLineEdit(self.groupBox)
        self.LE_max_kalimat.setGeometry(QtCore.QRect(260, 135, 151, 28))
        self.LE_max_kalimat.setMaxLength(5)
        self.LE_max_kalimat.setClearButtonEnabled(True)
        self.LE_max_kalimat.setObjectName("LE_max_kalimat")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(261, 50, 151, 16))
        self.label_9.setObjectName("label_9")
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setGeometry(QtCore.QRect(261, 120, 161, 16))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(261, 190, 141, 16))
        self.label_12.setObjectName("label_12")
        self.LE_top_wiki = QtWidgets.QLineEdit(self.groupBox)
        self.LE_top_wiki.setGeometry(QtCore.QRect(20, 205, 151, 28))
        self.LE_top_wiki.setMaxLength(5)
        self.LE_top_wiki.setClearButtonEnabled(True)
        self.LE_top_wiki.setObjectName("LE_top_wiki")
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setGeometry(QtCore.QRect(21, 190, 141, 16))
        self.label_13.setObjectName("label_13")
        self.B_proses = QtWidgets.QPushButton(self.tab)
        self.B_proses.setGeometry(QtCore.QRect(10, 366, 171, 30))
        self.B_proses.setObjectName("B_proses")
        self.ProgressBar = QtWidgets.QProgressBar(self.tab)
        self.ProgressBar.setGeometry(QtCore.QRect(205, 370, 231, 23))
        self.ProgressBar.setProperty("value", 0)
        self.ProgressBar.setObjectName("ProgressBar")
        self.L_status = QtWidgets.QLabel(self.tab)
        self.L_status.setGeometry(QtCore.QRect(61, 410, 371, 20))
        self.L_status.setObjectName("L_status")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(10, 410, 51, 20))
        self.label_3.setObjectName("label_3")
        self.Tab.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.TE_hasil = QtWidgets.QTextEdit(self.tab_3)
        self.TE_hasil.setGeometry(QtCore.QRect(10, 10, 431, 381))
        self.TE_hasil.setReadOnly(True)
        self.TE_hasil.setObjectName("TE_hasil")
        self.B_salin = QtWidgets.QPushButton(self.tab_3)
        self.B_salin.setGeometry(QtCore.QRect(10, 398, 84, 30))
        self.B_salin.setObjectName("B_salin")
        self.Tab.addTab(self.tab_3, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.TE_info = QtWidgets.QTextEdit(self.tab_2)
        self.TE_info.setGeometry(QtCore.QRect(10, 10, 431, 411))
        self.TE_info.setReadOnly(True)
        self.TE_info.setObjectName("TE_info")
        self.Tab.addTab(self.tab_2, "")
        self.B_keluar = QtWidgets.QPushButton(self.centralwidget)
        self.B_keluar.setObjectName(u"B_keluar")
        self.B_keluar.setGeometry(QRect(386, 495, 84, 30))
        self.B_manual = QtWidgets.QPushButton(self.centralwidget)
        self.B_manual.setObjectName(u"B_manual")
        self.B_manual.setGeometry(QRect(296, 495, 84, 30))
        self.B_reset = QtWidgets.QPushButton(self.centralwidget)
        self.B_reset.setObjectName(u"B_reset")
        self.B_reset.setGeometry(QRect(206, 495, 84, 30))
        self.L_aird = QtWidgets.QLabel(self.centralwidget)
        self.L_aird.setObjectName(u"L_aird")
        self.L_aird.setGeometry(QRect(10, 490, 111, 41))
        self.L_aird.setPixmap(QPixmap(u"aird.png"))
        self.L_aird.setScaledContents(True)
        self.L_unsri = QtWidgets.QLabel(self.centralwidget)
        self.L_unsri.setObjectName(u"L_unsri")
        self.L_unsri.setGeometry(QRect(130, 490, 41, 41))
        self.L_unsri.setPixmap(QPixmap(u"unsri.png"))
        self.L_unsri.setScaledContents(True)

        FMain.setCentralWidget(self.centralwidget)

        self.retranslateUi(FMain)
        self.Tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(FMain)
        FMain.setTabOrder(self.Tab, self.LE_kalimat_tanya)
        FMain.setTabOrder(self.LE_kalimat_tanya, self.CB_mesin_pencari)
        FMain.setTabOrder(self.CB_mesin_pencari, self.CB_mesin_pencari_2)
        FMain.setTabOrder(self.CB_mesin_pencari_2, self.LE_top_wiki)
        FMain.setTabOrder(self.LE_top_wiki, self.LE_min_kalimat)
        FMain.setTabOrder(self.LE_min_kalimat, self.LE_max_kalimat)
        FMain.setTabOrder(self.LE_max_kalimat, self.LE_max_hasil)
        FMain.setTabOrder(self.LE_max_hasil, self.B_proses)
        FMain.setTabOrder(self.B_proses, self.B_reset)
        FMain.setTabOrder(self.B_reset, self.B_manual)
        FMain.setTabOrder(self.B_manual, self.B_keluar)
        FMain.setTabOrder(self.B_keluar, self.TE_hasil)
        FMain.setTabOrder(self.TE_hasil, self.B_salin)
        FMain.setTabOrder(self.B_salin, self.TE_info)

        ## DEKLARASI FUNGSI EVENT ####################################################################

        self.B_proses.clicked.connect(self.proses_klik)
        self.B_salin.clicked.connect(self.salin_klik)

        self.B_reset.clicked.connect(self.reset_klik)
        self.B_manual.clicked.connect(self.manual_klik)
        self.B_keluar.clicked.connect(self.keluar_klik)

    ###############################################################################################

    def retranslateUi(self, FMain):
        _translate = QtCore.QCoreApplication.translate
        FMain.setWindowTitle(_translate("FMain", "Seleksi Dokumen OD-IQAS"))
        self.label.setText(_translate("FMain", "Masukan Kalimat Tanya:"))
        self.groupBox.setTitle(_translate("FMain", "Konfigurasi:"))
        self.label_8.setText(_translate("FMain", "Mesin Pencari:"))
        self.CB_mesin_pencari.setItemText(0, _translate("FMain", "Wikipedia + Google"))
        self.CB_mesin_pencari.setItemText(1, _translate("FMain", "Wikipedia + Bing"))
        self.CB_mesin_pencari.setItemText(2, _translate("FMain", "Wikipedia + Ask"))
        self.CB_mesin_pencari_2.setItemText(0, _translate("FMain", "Cosine Similarity"))
        self.CB_mesin_pencari_2.setItemText(1, _translate("FMain", "Okapi BM25"))
        self.CB_mesin_pencari_2.setItemText(2, _translate("FMain", "Okapi BM25L"))
        self.CB_mesin_pencari_2.setItemText(3, _translate("FMain", "Okapi BM25+"))
        self.label_10.setText(_translate("FMain", "Metode Similaritas"))
        self.LE_min_kalimat.setText(_translate("FMain", "5"))
        self.LE_max_hasil.setText(_translate("FMain", "50"))
        self.LE_max_kalimat.setText(_translate("FMain", "20"))
        self.label_9.setText(_translate("FMain", "Panjang Kalimat Minimal:"))
        self.label_11.setText(_translate("FMain", "Panjang Kalimat Maksimal:"))
        self.label_12.setText(_translate("FMain", "Jumlah Kalimat Hasil:"))
        self.LE_top_wiki.setText(_translate("FMain", "10"))
        self.label_13.setText(_translate("FMain", "Jumlah Halaman Wiki:"))
        self.B_proses.setText(_translate("FMain", "Proses Seleksi Dokumen"))
        self.L_status.setText(_translate("FMain", "Idle"))
        self.label_3.setText(_translate("FMain", "STATUS:"))
        self.Tab.setTabText(self.Tab.indexOf(self.tab), _translate("FMain", "Seleksi Dokumen"))
        self.B_salin.setText(_translate("FMain", "Salin"))
        self.Tab.setTabText(self.Tab.indexOf(self.tab_3), _translate("FMain", "Hasil Kalimat Seleksi"))
        self.Tab.setTabText(self.Tab.indexOf(self.tab_2), _translate("FMain", "Info"))
        self.B_keluar.setText(_translate("FMain", "Keluar"))
        self.B_manual.setText(_translate("FMain", "Manual"))
        self.B_reset.setText(_translate("FMain", "Reset"))
        self.L_aird.setText("")
        self.L_unsri.setText("")

        self.TE_info.setHtml(_translate("FMain",
                                        u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                        "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                        "p, li { white-space: pre-wrap; }\n"
                                        "</style></head><body style=\" font-family:'Bahnschrift'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">APLIKASI SELEKSI DOKUMEN OD-IQAS</span></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-weight:600;\"><br /></p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-bloc"
                                        "k-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">Pengembang:</span></p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Alvi Syahrini Utami</p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Novi Yusliani</p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Anggina Primanita</p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Abdiansah</p>\n"
                                        "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-"
                                        "indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">AIRD - UNSRI</span></p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Artificial Intelligence Research &amp; Development - Universitas Sriwijaya</p>\n"
                                        "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright @ 2022</p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">A. TENTANG APLIKASI</span></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; m"
                                        "argin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Aplikasi ini adalah alat bantu untuk penelitian di bidang <span style=\" font-weight:600;\">OD-IQAS</span> atau <span style=\" font-style:italic;\">Open Domain Indonesian Question Answering System</span>. Ada tiga komponen utama penyusun IQAS, yaitu: <span style=\" font-style:italic;\">Question Analysis</span>, <span style=\" font-style:italic;\">Document Analysis</span>, dan <span style=\" font-style:italic;\">Answer Analysis</span>. Aplikasi ini dapat digunakan di komponen <span style=\" font-style:italic;\">Document Analysis</span> untuk mengambil data teks di Internet berdasarkan pertanyaan pengguna. Luaran aplikasi adalah sekumpulan kalimat yang &quot;dianggap&quot; relevan dengan pertanyaan pengguna, yang selanjutnya bisa digunakan untuk proses ta"
                                        "hap selanjutnya.</p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">B. SPESIFIKASI TEKNIS</span></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Sumber Data:</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - Wikipedia</p>\n"
                                        "<p style=\" margin-top:0px; margin-b"
                                        "ottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - Google</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - Bing</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - Ask</p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Teknik Similaritas:</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - Cosine Similarity (TF-IDF)</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - BM25</p>\n"
                                        "<p style=\" margin"
                                        "-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - BM25L</p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">      - BM25+</p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Python 3.0</p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\""
                                        " font-weight:600;\">C. LISENSI APLIKASI</span></p>\n"
                                        "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">MIT License</p>\n"
                                        "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Copyright 2022 AIRD-UNSRI</p>\n"
                                        "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0;"
                                        " text-indent:0px;\">Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the &quot;Software&quot;), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:</p>\n"
                                        "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.</p>\n"
                                        "<p align=\"justify\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left"
                                        ":0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
                                        "<p align=\"justify\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">THE SOFTWARE IS PROVIDED &quot;AS IS&quot;, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.</p></body></html>",
                                        None))

    ### DEFINISI FUNGSI EVENT ####################################################################

    def isian_kosong(self):
        if self.LE_kalimat_tanya.text() != '' and self.LE_top_wiki.text() != '' and self.LE_min_kalimat.text() != '' and self.LE_max_kalimat.text() != '' and self.LE_max_hasil.text() != '':
            return False
        else:
            QMessageBox.warning(self, "Kesalahan", "Isian masih ada yang kosong, periksa kembali!", QMessageBox.Ok)
            return True

    def proses_klik(self):
        if not self.isian_kosong():
            params = []
            teks = self.LE_kalimat_tanya.text()
            top_wiki = int(self.LE_top_wiki.text())
            min_kal = int(self.LE_min_kalimat.text())
            max_kal = int(self.LE_max_kalimat.text())
            max_hsl = int(self.LE_max_hasil.text())
            no_mp = self.CB_mesin_pencari.currentIndex()
            no_metode = self.CB_mesin_pencari_2.currentIndex()
            params.append(teks)
            params.append(top_wiki)
            params.append(min_kal)
            params.append(max_kal)
            params.append(max_hsl)
            params.append(no_mp)
            params.append(no_metode)
            # print(params)

            self.thread = Thread(params)
            self.thread._signal_status.connect(self.signal_accept_status)
            self.thread._signal_pbar.connect(self.signal_accept_pbar)
            self.thread._signal_hasil.connect(self.signal_accept_hasil)
            self.thread.start()
            self.B_proses.setEnabled(False)
            self.TE_hasil.clear()
        else:
            self.TE_hasil.append('no')

    def signal_accept_status(self, msg):
        self.L_status.setText(str(msg))
        if self.B_proses.isEnabled():
            self.L_status.setText('Idle')

    def signal_accept_pbar(self, msg):
        self.ProgressBar.setValue(int(msg))
        if self.ProgressBar.value() == 99:
            self.ProgressBar.setValue(0)
            self.B_proses.setEnabled(True)
            QMessageBox.information(None, 'Informasi', 'Proses selesai, silakan lihat hasilnya')
            self.Tab.setCurrentIndex(1)

    def signal_accept_hasil(self, msg):
        for i, d in enumerate(msg):
            s = "{}. {} (sim: {:.2f})\n".format(i + 1, d[1], d[0])
            self.TE_hasil.append(s)

    def salin_klik(self):
        self.TE_hasil.selectAll()
        self.TE_hasil.copy()

    def reset_klik(self):
        self.LE_kalimat_tanya.clear()
        self.LE_kalimat_tanya.setFocus()
        self.CB_mesin_pencari.setCurrentIndex(0)
        self.CB_mesin_pencari_2.setCurrentIndex(0)
        self.LE_top_wiki.setText('10')
        self.LE_min_kalimat.setText('5')
        self.LE_max_kalimat.setText('20')
        self.LE_max_hasil.setText('50')
        self.TE_hasil.clear()

    def manual_klik(self):
        print('manual')

    def keluar_klik(self):
        sys.exit()
