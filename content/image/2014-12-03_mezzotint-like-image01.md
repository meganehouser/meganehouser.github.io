Title: 銅版画のようなイメージを作りたい その1
Tags: mezzotint, quil, processing
Summary: 浜口陽三の多色刷りのメゾチントが好きだ。なんとかしてProcessingでメゾチント風味を表現できないか。

浜口陽三の多色刷りのメゾチントが好きだ。なんとかしてProcessingでメゾチント風味を表現できないか。

### メゾチントの手法

1. 版の面全体に縦横斜めに無数の線を刻む。(目立て)
   (目の細かさで濃淡の表現が可能)
2. 目を金属のへら(バーニッシャー、スクレーパー)で削って絵を描く。
   (目を残した部分にインクが残り、色が載る)
3. 多色刷りの場合は1. と 2.を色数分作る


### 試してみたこと

目立てを縦横斜めのstroke-weightが0.1のlineで再現。lineはランダムで消したりずらしたりしている。

メゾチントの質感は出ていないがおもしろい感じになった。

次は濃淡をどのように表現するか。

<a href="https://www.flickr.com/photos/125573348@N07/15751621509" title="hanga-like by megane houser, on Flickr"><img src="https://farm8.staticflickr.com/7467/15751621509_fc19d782c9.jpg" width="357" height="500" alt="hanga-like"></a>

```clojure
(ns hanga.core
  (:require [quil.core :as q]))

(def canvas-len 300)
(defn c-red [] (q/color 172 46 43 100))
(defn c-green [] (q/color 48, 100, 84 100))
(defn c-blue [] (q/color 40, 48, 90 100))
(def colors [c-green c-blue c-red])
(defn back [] (q/color 9, 13, 11))

(def dark [0.2 0.7])
(def middle [0.3 0.7])
(def light [0.4  0.6])

(defn rand-bool 
  ([] (if (= (rand-int 2) 0) true false))
  ([p] (if (< (rand) p) true false)))

(defn gauss-rand []
  (* (q/random-gaussian) 1.5))

(defn rand-line [x1 y1 x2 y2 rough]
  (if (rand-bool rough)
    (let [x1 (+ (gauss-rand) x1)
          x2 (+ (gauss-rand) x2)
          y1 (+ (gauss-rand) y1)
          y2 (+ (gauss-rand) y2)]
      (q/line x1 y1 x2 y2))))

(defn sort-side [w h]
  (if (> w h) [:w :h] [:h :w]))

(defn square [x y width height [r1 r2] rotate]
  (q/stroke-weight 0.1)
  (q/with-translation [x y]
    (q/with-rotation [(if rotate (- (/ q/PI 4)) 0)]
      (doseq [i (range 0 width r1)]
        (rand-line i 0 i height r2))

      (doseq [i (range 0 height r1)]
        (rand-line 0 i width i r2))
      
      (let [size {:w width :h height}
            [long-side short-side] (sort-side width height)]
        (doseq [i (range 0 (short-side size) r1)]
          (rand-line i 0 0 i r2)
          (rand-line (- width i) 0 width i r2)
          (rand-line 0 (- height i) i height r2)
          (rand-line width (- height i) (- width i) height r2))
        (doseq [i (range 0 (- (long-side size) (short-side size)) r1)]
          (if (= long-side :w)
            (do
              (rand-line i 0 (+ height i) height r2)
              (rand-line (+ height i) 0 i height r2))
            (do
              (rand-line 0 i width (+ width i) r2)
              (rand-line 0 (+ width i) width i r2))))))))
  

(defn odd [n] (= (rem n 2) 1))

(defn bg []
  (q/stroke (back))
  (let [unit (/ (q/height) 5)]
    (doseq [i (range 5)]
      (square 0 (* unit i) (q/width) unit (if (odd i) middle dark) false))))


(defn setup []
  (q/smooth)
  (q/background 255)
  (q/stroke 0)
  (bg)

  (doseq [i (range 3)]
    (q/stroke ((nth colors i)))
    (let [w (+ (rand-int 300) 100)
          h (+ (rand-int 300) 100)
          x (- (+ (/ (q/width) 2) (- (rand-int 200) 100)) (/ w 2))
          y (- (+ (/ (q/height) 2) (- (rand-int 300) 150)) (/ h 2))]
    (square x y w h dark (rand-bool)))))

(defn mouse-pressed []
  (q/save "image.jpg"))

(defn start-sketch []
  (q/sketch
    :title "hanga"
    :size [500 700]
    :setup setup
    :mouse-pressed mouse-pressed
    :features [:exit-on-close]))

(defn -main [& args]
  (start-sketch))
```
