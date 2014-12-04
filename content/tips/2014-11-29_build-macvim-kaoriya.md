Title: macvim-kaoriyaをソースからビルド
Tags: vim macvim
Summary: Python2を無効化、Python3を有効化してビルドしてみた。


普段はMacVim-Kaoriyaを配布されているdmgからインストールしていて使用している。

配布されているdmgでは、Python2/Python3とも有効かされているが、jedi-vimがどうしてもPython2.7で実行されてしまうので、Python3のコード編集時に補完がうまくいかない。

Python2を無効化、Python3を有効化してビルドしてみた。

* 環境
    * Mac OS X 10.9.5
    * macvim-kaoriya 7.4 

## 1. cmigemoをインストール
```
$ brew install cmigemo
```

## 2. libiconvのビルド・インストール

libiconvを'-arch i386 -arch x86_64'でビルド・インストールする

```
$ wget http://ftp.gnu.org/pub/gnu/libiconv/libiconv-1.14.tar.gz
$ tar xzf libiconv-1.14.tar.gz
$ cd libiconv-1.14
$ CFLAGS='-arch i386 -arch x86_64' CCFLAGS='-arch i386 -arch x86_64' CXXFLAGS='-arch i386 -arch x86_64' ./configure
$ make
$ sudo make install
```

## 3. macvim-kaoriyaのソースを取得
```
$ git clone git://github.com/splhack/macvim.git
$ cd macvim
```

## 4. poファイルをビルドする
macvim/src/po ディレクトリでmakeを実行

## 5. ビルド用のShell Scriptを作成・実行する

解凍したmacvim-kaoriyaの直下に以下のシェルスクリプトを作る。
mac_install.sh

```
#! /bin/sh

cd src
CC=clang

LIBS="-lmigemo" LDFLAGS=-L/usr/local/lib ./configure --enable-python3interp --enable-luainterp --with-lua-prefix=/opt/local LUA_PREFIX=/opt/local -enable-multibyte --with-features=huge --enable-cscope --enable-migemo

make
```

## 5. 出来上がったMacVimをインストール

インストールして適当にMacVim3とかalias付けて使ってます。


# 参考
* [MacVim-KaoriYaのビルド方法](https://code.google.com/p/macvim-kaoriya/wiki/Building?tm=4)
* [Building · b4winckler/macvim Wiki](https://github.com/b4winckler/macvim/wiki/Building#how-to-build-macvim)
* [Compile vim 7.3 in Mac OS X 10.6.6](https://blog.wwwjfy.net/2011/03/02/compile-vim-7-3-in-mac-os-x-10-6-6/)
* [Macvimを自分でコンパイルした(mac) - なんか書いていこうぜー.com](http://muryoimpl.com/blog/2013/06/27/compile-macvim/)
