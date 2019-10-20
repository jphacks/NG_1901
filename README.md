# noti

<p align="center">
<a href="https://vimeo.com/367522065"><img src="pic/noti_icon_720.png" width="500"></a>
</p>

## 製品概要
### Life × Tech

#### 『通知のある生活』

消耗品の残量と在庫を教えてくれるデバイス。在庫がなくならない生活を提供します。

### 背景（製品開発のきっかけ、課題等）
生活に欠かせない消耗品、つい買うのを忘れて切らしてしまうことがある。「使いたい時に無い」を無くしたい。そこで私たちは、消耗品の残量と在庫を教えてくれるサービスがあれば、そのような状況をなくせるのでは無いかと考え、このデバイスを作成した。

また、消耗品に限らず、様々な使い方を期待できる。例えば、ポストにこのデバイスを置くことで、投函されたタイミングで通知が来る、一人暮らしのおじいちゃんの家に置くことで生存確認ができるなどアイデア次第でいろいろ可能になります。


### 製品説明（具体的な製品の説明）
|noti本体|登録用QRコード|設置例|
|---|---|---|
|![](pic/noti_hard.jpg)|![](pic/noti_QR.jpg)|![](pic/noti_tissue.jpg)|


#### 操作方法

まずはじめにnotiに記載されているQRコードを読み込んで友達追加します。  
<br>
<img src="pic/UI.png" width="300">  
notiには3つのメニューがあります。  
* 登録  
notiの登録をします。本体ボタンを長押しすると連携を開始します。  
LINE画面上でnotiに管理させる対象を選択します。※選択肢が足りない場合は手動設定が可能  
* リスト  
notiで管理している情報を一覧で表示します。  
* インフォメーション  
困りごとを解決できます。  


### システム構成図
![](pic/system.jpg)


### 特長

#### 1. 在庫が無くなったらその場で注文
残量が減ってきたことを通知するだけでなく、在庫が一定数を下回るとAmazonで注文ができる。LINEから直接注文ができるので、買いに行く手間やAmazonアプリを開く手間がいらない。

#### 2. 誰もが使ってるLINEで通知
LINEを利用して、デバイスの登録から残量・在庫のお知らせまで全てを行う。別途専用アプリケーションをうインストールすることがないので、LINEが入っていればどのデバイスでも通知を受け取ることが可能。

#### 3. 消耗品だけじゃない！？
notiの焦点は消耗品に当てていますが、使い方次第でいろんなことに使えます。基本の機能としては、センサが反応した回数で通知するので、ポストであったり、玄関であったり使い方はあなた次第！！！

### 解決出来ること
この製品を利用することで、たびたびおこる「使いたい時に無い」という状況をなくすことができます。また在庫がLINEから確認できるため、何が何個あって買う必要があるのかがすぐにわかります。日々の暮らしをスマートに、そして快適に過ごすことができるでしょう。

### 今後の展望
ラズパイを使ったのでモノ自体が大きくなった。


## 開発内容・開発技術
### 活用した技術
#### API・データ
* SQLite3
* LINEBot

#### フレームワーク・ライブラリ・モジュール
* Flask
* Heroku

#### デバイス
* RaspberryPi3 Model b
* 人感センサー
* 超音波センサー
* スマートフォン

### 研究内容・事前開発プロダクト（任意）
#### 研究内容
* モノの構造や仕様の最適化
* 各種センサを活用した実システム制御とコンピュータシミュレーションの統合

#### 事前開発プロダクト
* LINEBotやRaspberryPi関連の環境構築


### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* 複数のセンサを活用して、ティッシュやハンドソープなどを取る動作など，人や物の動きを検出できるハードウェア
* LINEを利用して、デバイスの登録から残量・在庫の通知やAmazonへの注文まですべて行うシステム
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください（任意）
