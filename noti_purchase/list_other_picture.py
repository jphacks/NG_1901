import requests
import re
from bs4 import BeautifulSoup

#関数serch_pictureの引数に消耗品を入力して実行すると、その消耗品が映った画像のURLが１つ出力されます
def serch_picture(serch_word):

    url = "https://search.nifty.com/imagesearch/search?select=1&q=%s&ss=up"
    keyword = serch_word
    r = requests.get(url%(keyword))
    soup = BeautifulSoup(r.text,'lxml')
    imgs = soup.find_all('img',src=re.compile('^https://msp.c.yimg.jp/yjimage'))

    #条件により検索ワードに近い画像が20個くらいに絞られています
    #countにより無理やり一個めの要素だけ出力しています
    count = 0
    for img in imgs:
        if count == 1:
            break
        print(img['src'])
        count = count+1
