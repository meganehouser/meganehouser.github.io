Title: Meguro.LYAFGG#4 開催しました
Tags: Haskell, Meguro.LYAFGG
Summary: 2019/06/20に、んむてさんと第四回すごいH本の原書を読む会を開催しました！

[んむて(@nnm_tech)さん | Twitter](https://twitter.com/nnm_tech)と第四回すごいH本の原書を読む会を開催しました！

[Meguro.LYAHFGG #4 - connpass](https://megurolyahfgg.connpass.com/event/133793/)

- 今回も開催場所はラクスルさんの会議室をお借りしました。ありがとうございました。

**第五回から参加したい方、輪読担当やりたい方大歓迎です**

## 実施内容
### 読んだ内容
以下、第三回目のノートです。

- 3章Types and TypeclassesのType variablesから3章の最後までやりました。
<script src="https://gist.github.com/meganehouser/decbc69c10d3a368495061393f0fb8cf.js"></script>

Haskell以外で出た話題を以下に書き留めます。

- 他の言語では==, +, -, *, /などの演算子はどのように実現しているか。
  - Python, C#,C++などのオブジェクト指向言語ではメソッドの糖衣構文として実現されている
  - そのため、それらの演算子をオーバーロードすると演算子の挙動を変更できる


### LT
今回は私が、今世間を騒がせているパイプライン演算子について説明しました。
以下、資料

#### F#のパイプライン演算子
```fsharp
    let add x y = x + y           // add : x:int -> y: int -> int
    let mul x y = x * y           // mul : x:int -> y: int -> int
    let display = printfn "number is %d" // display : int -> unit
    
    display(mul 2 (add 5 10))
    
    10 |> add 5 |> mul 2 |> display
    
    let (|>) arg f = f arg
```

- F#では中置演算子が定義可能、カリー化が標準組み込みされているのでパイプライン演算子が、標準の言語仕様内で実装可能
- Elixirは中置演算子が定義不可、カリー化もされないので、マクロによるAST変換により実現

#### Rubyのパイプライン演算子
```ruby
    class A
      def initialize(n)
    	  @n = n
      end 
    
      def add(n)
        @n = @n + n
        self
      end
    
    	def mul(n)
    	  @n = @n * n
        self
      end
    
      def display
        puts "number is " + @n.to_s
      end
    end
    
    A.new(10).add(5).mul(2).display()
    
    A |> new 10 |> add 5 |> mul 2 |> display
```

- Rubyのパイプライン演算子はF#ともElixirとも異なる
- 単にメソッドチェーンがパイプライン演算子で書き換えられるだけなので有効なユースケースがあるか

#### Haskellでのパイプライン演算子

```haskell
    add x y = x + y
    mul x y = x * y
    display n = putStrLn ("number is " ++ show n)
    
    display(mul 2 (add 5 10))
    display $ mul 2 $ add 5 $ 10  -- ($) :: (a -> b) -> a -> b
    
    import Data.Function
    10 & add 5 & mul 2 & display -- (&) :: a -> (a -> b) -> b
    
    (|>) arg f = f arg
    10 |> add 5 |> mul 2 |> display
```

#### 元ネタ
[パイプライン演算子の歴史 - まめめも](https://mametter.hatenablog.com/entry/2019/06/15/192311)

[第一引数版パイプライン演算子 - Qiita](https://qiita.com/cedretaber/items/6a3831367439f64756ab)

### LTで参加者から出てきた話題
- ECMAScriptにもパイプライン演算子のプロポーザルが上がっている
    - [tc39/proposal-pipeline-operator: A proposal for adding the simple-but-useful pipeline operator to JavaScript.](https://github.com/tc39/proposal-pipeline-operator)
     - 現在Stage1
         - [proposals/stage-1-proposals.md at master · tc39/proposals](https://github.com/tc39/proposals/blob/master/stage-1-proposals.md)
- JavaScriptで関数型っぽく書く
    - [Composing Software: An Introduction – JavaScript Scene – Medium](https://medium.com/javascript-scene/composing-software-an-introduction-27b72500d6ea)
- C++のパイプライン演算子ではなくパイプラインの話
    - http://www.open-std.org/jtc1/sc22/wg21/docs/papers/2018/p1261r0.pdf
- Rubyでコンビネータ
    - [yield_selfを使ったリファクタリング - Qiita](https://qiita.com/irohiroki/items/b4a3653b3ddf2e357a9d)