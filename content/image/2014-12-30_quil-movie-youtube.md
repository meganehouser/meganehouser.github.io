Title: Quil -> Movie -> Youtube
Tags: quil, processing, YouTube
Summary: Quilで作成したSketchから動画を作成し、YouTubeにアップロードしてみた。

写真とQuil(Processing)を組み合わせたものに興味があり、試しに動画化、YouTubeにアップロードしてみた。

## 1. Quilのスケッチからフレームごとの画像を作成する

今回、動画を作ったコード。
<script src="https://gist.github.com/meganehouser/0507cbb86075878a5ed4.js"></script>

ポイントはdraw関数内の以下の部分。
```clojure
; -- 略 -- 
(q/save-frame "frames/####.jpg")))
```

save-frameで現在のフレームを保存する。

## 2. フレームごとの画像を動画に変換する

Processingに付属しているツール、MovieMakerを使用した。

スケッチはQuilで書いてるのに片手落ちだが、手軽だからよしとする。

MovieMakerで画像を保存したフォルダを指定すればよい。

## 3. YouTube にアップロードする
<iframe width="640" height="390" src="//www.youtube.com/embed/o4CmVlCiasU" frameborder="0" allowfullscreen></iframe>


最初はVineにアップロードしようとしたが、VineのAPIは非公開、かつVineにPCから動画をアップロードできるVineClientは不審な通信をしてるらしいので無難にYouTubeにしといた。

* 参考<br>
[PCからVine投稿できるChrome機能拡張に不審な通信【Vineユーザー検索のミニ動画JP】](view-source:http://minidoga.jp/blog/20140327.html)

