Title: カジュアルF#
Tags: fsharp
Summary: この記事では、F#をカジュアルに使い始める方法について説明したい。 

社内Advent Calendar用に書いた記事

### 目次

* [お前誰よ](#whoareyou)
* [概要](#about)
* [F#とは](#intro)
* [導入方法](#install)
* [REPL F#はじめの一歩](#repl)
* [F#スクリプト 次の一歩](#script)
    * [例1: ファイルをダウンロードする](#download)
    * [例2: 他の.NETライブラリの読み込み](#refdll)
    * [例3: 簡易的なWebサーバ](#webserver)
    * [例4: 複雑なフォルダ構造を作成する](#folder)
* [まとめ](#conclusion)

***

<h1 id='whoareyou'>お前誰よ</h1>

* 職種: SE
* お仕事: Word, Excel, たまにC#

プライベートではPythonとかClojureとか

<h1 id='about'>概要</h1>

F#は.NET Frameworkの第一級言語だが、いきなりC#のポジションを置き換えようとすると大変。
F#は、REPLやスクリプト実行をサポートし、C#での開発をサポートする用途にも使える。
この記事では、F#をカジュアルに使い始める方法について説明したい。

<h1 id='intro'>F#とは</h1>

* OCamlの影響を色濃く受けた、.NET Framework向けの言語。
* 手続型、オブジェクト指向、関数型に対応した強い静的型付けのマルチパラダイムプログラミング言語。
* Visual Studio 2010 から標準搭載されている。


<h1 id='install'>導入方法</h1>

* 今回はVisual Studio 2013 Community Editionをインストールした。
  * その他の導入方法は [Use F# on Windows | The F# Software Foundation](http://fsharp.org/use/windows/)を参照。
* Visual StudioのF#サポート機能がリッチになるので[Visual F# Power Tools](http://fsprojects.github.io/VisualFSharpPowerTools/)も入れておこう。

<h1 id='repl'>REPL F#はじめの一歩</h1>

今時の言語はREPLが必ずと言っていいほど付いてくる。
もちろんF#にも！

C#には今のところ公式なREPLがないが、F#のREPLを使って.NET Frameworkのクラスの挙動を即座に確認することができる。

## REPL の使い方
Visaul Studio 2013 をインストールするとF#が以下のフォルダにインストールされている。
> C:\Program Files (x86)\Microsoft SDKs\F#\3.1\Framework\v4.0

パスを通しておこう。
F# のREPLはこのフォルダ内のfsi.exeが本体。

例えば、DateTime型のフォーマット書式ってこれで合ってったっけ？って思ったら、fsiをおもむろに起動して以下のように確認すればいい。

```
> open System;;
> DateTime.Now.ToString("HH:mm:ss");;
val it: string = "14:10:12"
> #q;; // REPLの終了
```

1行目のopenは名前空間のインポート。C#でいうusingに相当する。
入力した部分を実行するには、行末に";;"を入力してEnterする。

正規表現を試してみるのにも便利だろう。

```
> open System.Text.RegularExpressions;;
> let isMatch pattern input =
-   let rgx = new Regex(pattern)
-   rgx.IsMatch(input);; // 関数を定義

val isMatch : pattern:string -> input:string -> bool

> isMatch "^\d{3}\-\d{4}$" "111-4444";; // 定義した関数を呼び出してみる
val it : bool = true
```

この例ではアドホックな関数を定義して使用している。
let は識別子を、値または関数と関連付ける（束縛する）。

```fsharp
let value = "hello world" // 値を束縛する場合
let add v1 v2 = v1 + v2   // 関数を束縛する場合
```


<h1 id='script'>F#スクリプト 次の一歩</h1>

F#も通常はプロジェクトを作成してビルドしてexeなりdllを作るが、fsiを使えばスクリプトとして実行できる。

拡張子.fsxでファイルを作成し、Visual Studioにドラッグアンドドロップすれば、インテリセンス付きでスクリプトの編集が開始できる。

いくつかF#の例を見ながら、F#の特徴的な機能を確認してみよう。

<h2 id='download'>例1: ファイルのダウンロード</h2>

例えば、コマンドラインからファイルをダウンロードしたい場合

```fsharp
// wget.fsx
// Usage
//  > fsi wget.fsx http://example.com/sample.zip
open System.Linq

let wc = new WebClient()

fsi.CommandLineArgs.[1]
|> fun url -> url, url.Split('/').Last()
|> wc.DownloadFile
```

例外処理もオプション指定もないが、実質5行で書くことができた。

記号"|>"はパイプラインと呼ばれる組み込み演算子。左辺の値を右辺の関数の引数として渡すもの
(この例ではパイプラインの前で改行しているので左辺は1行上の値に当たる）。
関数をメソッドチェーンのようにつなげて書けるため、処理の流れが視覚的に分かりやすい。

実装は以下のように自分でも書けるので、機能を追加したパイプラインも容易に書ける。

```fsharp
let (|>) x f = f x
```

1個目のパイプラインの右辺にある"fun url -> url..." の部分は匿名関数。
匿名関数の書式は以下となる。

```
fun 引数 -> 処理
```


<h2 id='refdll'>例2: 他の.NETライブラリの読み込み</h2>

F#から自作のライブラリやサードパーティのライブラリをアドホックに呼び出してみたいときも、スクリプトなら気軽だ！

例えばOpenCvSharpを使用して、Webカメラで自分の顔を撮りたくなったら以下のスクリプトの出番だ。

```fsharp
#r "OpenCvSharp.dll"
open OpenCvSharp

let capture = Cv.CreateCameraCapture(CaptureDevice.Any)
try
    ignore <| Cv.QueryFrame(capture) // 1フレーム目は捨てる
    let frame = Cv.QueryFrame(capture)
    frame.SaveImage("me.bmp")
finally
    capture.Dispose()
```

冒頭の#r で.NETアセンブリのパスを指定して読み込ませることで、スクリプト内から使用できる。

スクリプト内に波括弧がないことに気付いたかもしれない。
F#では軽量構文と冗語構文が用意されており、デフォルトでは軽量構文となっている。
軽量構文ではスコープはインデントで表現される。

<h2 id='webserver'>例3: 簡易的なWebサーバ</h2>

python3だと以下のコマンドでポート8000でWebサーバが起動する。

```
python -m http.server
```

F# のスクリプトで簡易的に実装してみよう。

```fsharp
// httpserver.fsx
// usage
//  > fsi httpserver.fsx

open System.Net
open System.Text
open System.IO

let currentDir = System.Environment.CurrentDirectory
let lstnr = new HttpListener()
lstnr.Prefixes.Add "http://localhost:8000/"
lstnr.Start()
async{
    while true do
        let! context = Async.FromBeginEnd(lstnr.BeginGetContext, lstnr.EndGetContext)
        let req, res = context.Request, context.Response
        let filePath = Path.Combine(currentDir, req.RawUrl.TrimStart('/').Replace('/', '\\'))

        async{
            match File.Exists(filePath) with
            | true -> let bytes = File.ReadAllBytes(filePath)
                      res.OutputStream.Write(bytes, 0, bytes.Length)
                      res.Close()
            | false -> res.StatusCode <- 404
                       res.Close()
        } |> Async.Start
} |> Async.RunSynchronously
```

ここでのポイントは"async{ ... }"。
コンピュテーション式という機能を使用している。
コンピュテーション式はletやforといったビルトインのキーワードや制御フローを独自に再定義できる。
式内では再定義したルールに従って処理が実行される。

asyncは組み込みのコンピュテーション式で、非同期処理を書くためのもの。
定型的な処理や複雑な処理をコンピュテーション式の定義に実装することによって、式内の処理はシンプルに書ける。

"match.."はmatch式というC#でいうところのswitch文のようなもの。
スクリプトではmatch式を使って、ファイル存在有無で処理を振り分けている。

```
match 式 with
| 式の値パターン1 -> 戻り値の式1
| 式の値パターン2 -> 戻り値の式2
| ...
```

<h2 id='folder'>例4: 複雑なフォルダ構造を作成する</h2>

複雑なフォルダ・ファイル構造を作成したい場合。


```fsharp
open System.IO

type Entry =
| File of string
| Dir of string * Entry list

let data =
    Dir("root",
        [
            Dir("1st", [File("1-1.txt"); File("1-2.txt")])
            Dir("2nd", [File("2-1.txt")])
        ])

let makeDir name = Directory.CreateDirectory(name) |> ignore
let makeFile name = File.Create(name) |> fun f -> f.Close()
let combine str1 str2 = Path.Combine(str1, str2)

let rec make cd entry =
    match entry with
    | Dir(name, rest) -> let cd = combine cd name
                         makeDir cd
                         List.iter(make cd) rest
    | File(name) -> makeFile <| combine cd name
```

冒頭のtype宣言は判別共用体というもの。

```fsharp
type Entry =
| File of string
| Dir of string * Entry list
```

この例ではファイルシステム要素を判別共用体として定義している。

以下の内容をデータ構造として素直に表現している。視覚的にも分かりやすい。
* ファイルシステム要素(Entry)は、ファイル(File)またはディレクトリ(Dir)である
* ファイルは文字列型の値(ファイル名)を持つ
* ディレクトリは文字列型の値(ディレクトリ名)と、ファイルシステム要素を複数持つ

後半の関数定義で使用している"rec"キーワードは再帰関数を定義する際に必要。

再帰関数内のmatch式は、パターンマッチを使用して判別共用体から実際の値を取り出して、処理で使用している。


<h1 id='conclusion'>まとめ</h1>

F#はREPLやスクリプトとしてカジュアルに使用できる！

個人的には、仕事で開発する場合はC#が多く、F#はREPLやスクリプトで以下のような補助的なタスクに使用している。

* REPLで.NET Frameworkのクラスの挙動を確認
* スクリプトで作成中のC#アプリケーションまたはライブラリをアドホックに呼び出す
* スクリプトでテストデータを生成する

Q: それってPowerShellでもよくない？
<div style="font-size:40px">A: F#の方が楽しいから</div>
F#はLinuxでもMacでも書けるよ。<br>
あとF#の強力な抽象化の機能と、シンプルに書ける言語表現力は魅力だよ。

### 言い訳
（駆け足で紹介したので説明不足や厳密にいうと不正確な部分もあると思います。
疑問、指摘などあればコメントお願いします。）
