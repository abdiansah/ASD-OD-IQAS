from rank_bm25 import BM25Okapi, BM25L, BM25Plus
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Similarity:
    """ fungsi-fungsi similarity """

    def cosine_similarity_tf_idf(self, dok_kalimat, kueri, top_n=10):
        docTFIDF = TfidfVectorizer().fit_transform(dok_kalimat)
        queryTFIDF = TfidfVectorizer().fit(dok_kalimat)
        queryTFIDF = queryTFIDF.transform([kueri])

        sim = cosine_similarity(queryTFIDF, docTFIDF).flatten() # tidak ada paramter untuk cosine
        data_sim = []
        for i, k in enumerate(dok_kalimat):
            data_sim.append((sim[i], k))
        data_sim = sorted(data_sim, reverse=True)
        if len(data_sim) >= top_n:
            data_sim = data_sim[:top_n]
        return data_sim

    def bm_25(self, dok_kalimat, kueri, tipe="BM25", top_n=10):
        tokenisasi_korpus = [d.split(" ") for d in dok_kalimat]
        tokenized_kueri = kueri.split(" ")
        match tipe:
            case "BM25":
                bm25 = BM25Okapi(tokenisasi_korpus) # pelajari parameter bm25
            case "BM25L":
                bm25 = BM25L(tokenisasi_korpus)
            case "BM25+":
                bm25 = BM25Plus(tokenisasi_korpus)
            case _:
                bm25 = BM25Okapi(tokenisasi_korpus)

        sim = bm25.get_scores(tokenized_kueri)
        data_sim = []
        for i, k in enumerate(dok_kalimat):
            data_sim.append((sim[i], k))
        data_sim = sorted(data_sim, reverse=True)
        if len(data_sim) >= top_n:
            data_sim = data_sim[:top_n]
        return data_sim

    def demo(self):
        kueri = "nama abdiansah"
        dok_kalimat = ["nama saya abdiansah", "abdiansah nama saya lahir di pagar alam", "saya abdiansah", "ok bento"]
        print("kueri\t: ", kueri)
        print("dokumen\t: ", dok_kalimat)
        print("\r")

        print("Hasil Cosine Similarity:")
        data_cs = self.cosine_similarity_tf_idf(dok_kalimat, kueri)
        for i, d in enumerate(data_cs):
            print("{}. {:.2f}\t: {}".format(i + 1, d[0], d[1]))

        print("\r")

        print("Hasil BM25:")
        data_bm25 = self.bm_25(dok_kalimat, kueri, "BM25")
        for i, d in enumerate(data_bm25):
            print("{}. {:.2f}\t: {}".format(i + 1, d[0], d[1]))

        print("\r")

        # print("Hasil BM25L:")
        # data_bm25 = self.bm_25(dok_kalimat, kueri, "BM25L")
        # for i, d in enumerate(data_bm25):
        #     print("{}. {:.2f}\t: {}".format(i + 1, d[0], d[1]))
        #
        # print("\r")
        #
        # print("Hasil BM25+:")
        # data_bm25 = self.bm_25(dok_kalimat, kueri, "BM25+")
        # for i, d in enumerate(data_bm25):
        #     print("{}. {:.2f}\t: {}".format(i + 1, d[0], d[1]))

# sim = Similarity()
# sim.demo()