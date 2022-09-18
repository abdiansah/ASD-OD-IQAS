import urllib.request
import requests
import wikipedia
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pemroses_teks import  PemrosesTeks

class IRWikipedia:
    """ Kelas untuk mengambil teks dari Wikipedia"""

    def __init__(self):
        pass

    def teks_wikipedia(self, kueri, wiki_top_n=1): # PARAMETER UNTUK WIKIPEDIA
        teks = "--tidak ada teks--"
        wikipedia.set_lang("id")
        halaman = wikipedia.search(kueri, wiki_top_n) # top_n: jumlah halaman wiki
        if halaman != []:
            teks = ""
            for h in halaman:
                wp = wikipedia.page(h)
                # teks = teks + ". \n" + wp.content
                teks = PemrosesTeks.gabung_teks(self, teks, wp.content)
                # print(wp.html())
                # print(wp.original_title)
                # print(wp.links[0:10])
                # print(wp.summary)
                # print(wp.content)
            return teks
        else:
            print("Tidak ada halaman Wikipedia yang relevan dengan kueri!")
            return teks


class IRMesinPencari:
    """ Kelas untuk mengambil teks dari Mesin Pencari"""

    # url = "https://id.search.yahoo.com/search?p=soekarno"
    # request = urllib.request.Request(url)
    # request.add_header('User-Agent',
    #                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36')
    # raw_response = urllib.request.urlopen(request).read()

    GOOGLE = 1
    YAHOO = 2
    BING = 3
    ASK = 4

    def __init__(self):
        pass

    def ambil_urls(self, url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)

    def urls_mesin_pencari(self, nama_mesin_pencari, kueri):
        kueri = urllib.parse.quote_plus(kueri)

        match nama_mesin_pencari:
            case self.GOOGLE:
                response = self.ambil_urls("https://www.google.co.uk/search?q=" + kueri)
            case self.YAHOO:
                response = self.ambil_urls("https://id.search.yahoo.com/search?p=" + kueri)
            case self.BING:
                response = self.ambil_urls("https://www.bing.com/search?q=" + kueri)
            case self.ASK:
                response = self.ambil_urls("https://www.ask.com/web?q=" + kueri)
            case _:
                pass

        links = list(response.html.absolute_links)
        try:
            file = open("daftar_domain.txt", "r")
            remove_domains = tuple(file.read().split())
            # print(daftar_domain)
        except FileNotFoundError:
            print("File remove_domain.txt tidak ditemukan!")
            remove_domains = tuple()

        for url in links[:]:
            if url.startswith(remove_domains):
                links.remove(url)

        return links

    def ambil_teks_url(self, url):
        teks = "--tidak ada teks--"
        try:
            with urllib.request.urlopen(url) as f:
                html = f.read().decode(errors='replace') ### mencegah error unicode
                soup = BeautifulSoup(html, "lxml")
                teks = soup.get_text()
            return teks
        except urllib.error.URLError as e:
            print(e.reason)
            return teks

    def teks_mesin_pencari(self, kueri, no_mesin_pencari=0):

        match no_mesin_pencari:
            case 0: urls = self.urls_mesin_pencari(self.GOOGLE, kueri)
            case 1: urls = self.urls_mesin_pencari(self.BING, kueri)
            case 2: urls  = self.urls_mesin_pencari(self.ASK, kueri)
            case 3: urls  = self.urls_mesin_pencari(self.YAHOO, kueri)
            case 4: # gabungan semua mesin pencari
                url_google = self.urls_mesin_pencari(self.GOOGLE, kueri)
                url_bing = self.urls_mesin_pencari(self.BING, kueri)
                url_ask = self.urls_mesin_pencari(self.ASK, kueri)
                url_yahoo = self.urls_mesin_pencari(self.YAHOO, kueri)
                urls = url_google + url_bing
                # urls = url_google + url_bing + url_ask + url_yahoo
                # print("jumlah total url: ", len(urls))
                # filter url duplikat
                urls = set(urls)
                # print("jumlah total url hasil filter: ", len(urls))

        dokumen = [self.ambil_teks_url(u) for u in urls]
        teks = ""
        for d in dokumen:
            # teks = teks + ". \n" + t
            teks = PemrosesTeks.gabung_teks(self, teks, d)

        return teks

