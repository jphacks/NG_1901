from bs4 import BeautifulSoup
import requests

def search_amazon(search_word):
    #引数の中に空白があった時、空白を+に置き換える
    words = search_word.split(" ")
    search_words = words[0]
    for i in range(1, len(words)):
        search_words = search_words + "+" + words[i]

    #スクレイピングするサイトのURLを作成
    url = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=" + search_words + "&rh=i%3Aaps%2Ck%3A" + search_words

     #作成したURLからHTMLを取得
    response = requests.get(url).text
    #BeautifulSoupの初期化
    soup = BeautifulSoup(response, 'html.parser')
    #どこの部分を取得するか指定
    items = soup.find_all('li', {"class":"s-result-item"})

    #いくつかの商品を同時に取得しているので商品ごとに商品名と値段とURLを取得
    for item in items:

            #商品名付近のHTML取得
            name = item.h2

            #商品名の情報も値段の情報も含まないHTMLがあってそのままだとエラーが起きたので、Noneになる部分は除外
            if name != None and price != None:
                    #商品名取得
                    nameTitle = name.string
                    #商品のURL取得
                    item_url = item.a.get("href")
                    print(nameTitle)
                    print(item_url)

    #表示
    # print(url)
    return url
