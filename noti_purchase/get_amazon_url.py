from bs4 import BeautifulSoup
import requests

def serch_amazon(serch_word):
    #引数の中に空白があった時、空白を+に置き換える
    words = serch_word.split(" ")
    serch_words = words[0]
    for i in range(1, len(words)):
        serch_words = serch_words + "+" + words[i]

    #スクレイピングするサイトのURLを作成
    url = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=" + serch_words + "&rh=i%3Aaps%2Ck%3A" + serch_words

    #表示
    print(url)

serch_amazon("ティッシュ")
