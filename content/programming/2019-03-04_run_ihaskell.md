Title: MacでIHaskellを動かす
Tags: Haskell

Jupyter notebookをHaskellで動かそうと[gibiansky/IHaskell: A Haskell kernel for IPython.](https://github.com/gibiansky/IHaskell)をREADMEを見ながらインストールしたが動作せず。動くようになったのでメモ。

# 環境
| 項目 | 値 |
| ---- | --- |
| OS | macOS Mojave 10.14.3 |
| Stack | 1.9.3 |
| GHC | 8.6.3 |

# 手順
README通りに進める。
1. 依存するパッケージをインストール
```
brew install zeromq libmagic cairo pkg-config pango
```
python3とHaskell-stackはインストール済みだったので外した。

2. gitリポジトリをクローン
```
git clone https://github.com/gibiansky/IHaskell
cd IHaskell
```

3. 依存するPythonパッケージをインストール
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install requirements.txt
```
ipythonのインストールでエラーになる。必要なバージョンのprompt-toolkitが他のパッケージのせいで入れられないため。
入れるパッケージのバージョンを調整する必要がある。

4. Haskellでビルド
```
stack install --fast
ihaskell install --stack
```

5. jupyter notebok起動
```
stack exec jupyter -- notebook
```

Cellを実行しても戻り値が帰ってこない。
ConsoleにWarningログが出ている。

[python - Jupyter notebook: No connection to server because websocket connection fails - Stack Overflow](https://stackoverflow.com/questions/54963043/jupyter-notebook-no-connection-to-server-because-websocket-connection-fails)

最近リリースされたtornado 6.0がインストールされてしまっていて、非互換でこけているらしい。
と、いうわけでtornadoは5系がインストールされる必要がある。

# 対処
Pythonでインストールするパッケージのバージョンを調整。なんとか動いた。

動く状態のrequirements.txtは以下。これを3.でpip installする時に使えば良い。

<script src="https://gist.github.com/meganehouser/32d8a93e3d8b13cbceb6a6f2eb339f1d.js"></script>
