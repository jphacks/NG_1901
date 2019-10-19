from bs4 import BeautifulSoup
import requests

#アマゾンで検索したい言葉とページ数を引数に取る関数　検索結果の「商品名」と「値段」「URL」をCSVにまとめて保存してくれる
def serch_amazon(serch_word, get_pages):
        #引数の中に空白があったとき、空白を+に置き換える
        words = serch_word.split(" ")
        serch_words = words[0]
        for i in range(1, len(words)):
                serch_words = serch_words + "+" + words[i]

        #スクレイピングするサイトのURLを作成
        url = "https://www.amazon.co.jp/s/ref=nb_sb_noss_2?__mk_ja_JP=カタカナ&url=search-alias%3Daps&field-keywords=" + serch_words + "&rh=i%3Aaps%2Ck%3A" + serch_words

        #リストを作成
        columns = ["Name",  "Price", "Url"]

        #次のページに行く際にこのURLが必要
        amazon = "https://www.amazon.co.jp"

        #ページ番号
        page = 1

        #ページ数が足りないときはエラーではなく、そのページ以降はないことを知らせてくれる
        try:
                #「 get_pages」のページ分だけ繰り返す
                while page < get_pages + 1:

                        #何ページ目を取得している最中なのか表示
                        print(page,"ページを取得中.....")

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
                                #商品の値段付近のHTML取得
                                price = item.find("span", {"class":"a-size-base"})
                                #商品名の情報も値段の情報も含まないHTMLがあってそのままだとエラーが起きたので、Noneになる部分は除外
                                if name != None and price != None:
                                        #商品名取得
                                        nameTitle = name.string
                                        #商品の値段取得
                                        priceText = price.string
                                        #商品のURL取得
                                        item_url = item.a.get("href")

                        #ページの下の方の「次のページ」のURLを取得
                        NextUrl = soup.find('span', {"class":"pagnRA"})
                        #Url = NextUrl.a.get("href")

                        #そのままでは次のページに行けないのでちゃんとしたものに変更
                        #url = amazon + Url

                        #次のページに行くので変数pageの値を1大きくする
                        page += 1

        except:
                #取得しようと思ったページ数まで到達する前に終わったらそのページ以降はなかったと出力
                print(page+1 + "以降のページはなかった")

        finally:
                #終わったことを出力
                print(url)
                print(item_url)
                print("finish")

serch_amazon("ティッシュ", 1)
