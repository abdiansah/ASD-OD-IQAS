import re
import nltk

class PemrosesTeks:
    """ Kelas untuk alat bantu pemrosesan teks """

    def pemrosesan_kueri(self, kueri):
        pola = r"\bapa\b|\bsiapa\b|\bdimana\b|\bdi mana\b|\bkapan\b"

        kueri = kueri.lower()
        kueri = re.sub(pola, "", kueri)
        kueri = re.sub(r"[\s]+", " ", kueri)
        kueri = kueri.strip()

        return kueri

    def penghilang_derau(self, teks):
        teks = re.sub(r'[^a-zA-Z0-9\n\s.,-]', '', teks)  # hapus non alfanumerik
        teks = ' '.join(teks.split())                   # hapus spasi \t dan karakter whitespace laiinya (jangan gunakan regex!)

        return teks

    def tokenisasi_kalimat(self, teks):
        kalimat = nltk.sent_tokenize(teks)
        # tokenisasi = nltk.data.load("/home/abdiansah/nltk_data/tokenizers/punkt/PY3/indonesian.pickle")
        # dokumen = tokenisasi.tokenize(teks)
        kalimat = [d.strip() for d in kalimat]

        return kalimat

    def filter_kalimat(self, kalimat, jml_min_kata=5, jml_maks_kata=1000): # PARAMETER UNTUK PANJANG KATA
        kalimat_filter = []

        for k in kalimat:
            if (len(k.split()) >= jml_min_kata) and (len(k.split()) <= jml_maks_kata):
                kalimat_filter.append(k.lower()) # LOWER-CASE

        kalimat_filter = set(kalimat_filter)

        return  kalimat_filter

    def gabung_teks(self, teks1, teks2):
        teks = teks1 + ". \n" + teks2

        return teks

    def tampilkan_kalimat(self, kalimat):
        for i, k in enumerate(kalimat):
            print(i + 1, k)