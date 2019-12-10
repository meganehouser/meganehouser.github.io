Title: Rustのターミナル操作crateいろいろ
Tags: rust, advent calendar
Summary: Rustその2 Advent Calendar 2019の記事です。

この記事は[Rustその2 Advent Calendar 2019](https://qiita.com/advent-calendar/2019/rust2)の11日目の記事です。

いろいろなターミナル操作系のcrateがあるので試してみました、という記事です。

### 目次

- [はじめに](#preface)
- [nucurses-rs](#ncurses-rs)
- [pancurses](#pancurses)
- [rustbox](#rustbox)
- [crossterm](#crossterm)
- [termion](#termion)
- [cursive](#cursive)
- [tui-rs](#tui-rs)
- [まとめ](#conclusion)


<h2 id="preface">はじめに</h2>

映画「マトリックス」に影響を受けまくった世代なので[cmatrix](https://github.com/abishekvashok/cmatrix)、[unimatrix](https://github.com/will8211/unimatrix)みたいなターミナルで緑色の文字が振ってくるコマンドをRustで移植しました。

作ったコマンド「[rustmatrix](https://github.com/meganehouser/rustmatrix)」の画面
![rustmatrix](https://user-images.githubusercontent.com/1280199/67680821-6d5f0100-f9cf-11e9-8989-d88684ff1dfc.png)

ターミナルを操作するcrateは当初cursiveを使っていたのですが、CPU使用率が40%を超えてしまいました。cursiveは毎フレームで描画を行なってアニメーションする用途には向いていないようです。

そこで他のターミナル操作系のcrateで書き直すことにしたのですが、結構いろんなcrateがあってよくわからなかったので調べてみました。

各情報とサンプルプログラムを掲載しています。サンプルプログラムはHello Worldだけだと簡単すぎるので、`m`キーをクリックしたら画面中央に"Merry Christmas"と表示するものです。

Star数やLatest versionは2019/12/10での状態です。

<h2 id="nucurses-rs">ncurses-rs</h2>
割と昔からあるncursesの薄いラッパーです。
ドキュメントは書かれていませんが、ncursesの方で検索すると使い方がいくらでも出てくるので困ることはありません。

| key | value |
| -- | -- |
| repository |[jeaye/ncurses-rs](https://github.com/jeaye/ncurses-rs) |
| Star | 473 |
| crates.io | [https://crates.io/crates/ncurses](https://crates.io/crates/ncurses) |
| Latest version | 5.99.0 (Feb 25, 2019)  |
| docs.rs | [ncurses - Rust](https://docs.rs/ncurses/5.99.0/ncurses/) |

```rust
use ncurses::*;

const MESSAGE: &str = "Merry Christmas !!";

fn main() {
    let window = initscr();
    start_color();
    use_default_colors();
    init_pair(1, COLOR_BLUE, -1);
    addstr("Hello world !!");
    refresh();
    keypad(window, true);
    noecho();
    curs_set(CURSOR_VISIBILITY::CURSOR_INVISIBLE);

    loop {
        match getch() {
             109 => {
                let y = getmaxy(window) / 2;
                let x = getmaxx(window) / 2 - (MESSAGE.len() / 2) as i32;
                clear();
                color_set(1);
                mvaddstr(y, x, MESSAGE);
            }
            KEY_DC => break,
            _ => (),
        }
    }
    endwin();
}
```

C言語のライブラリの薄いラッパーのため、構造体+メソッドでの抽象化などは行われておらず、フラットに命令を呼んでいく形式になります。



<h2 id="pancurses">pancurses</h2>
pancursesはLinuxとWindows両方をサポートしつつ、cursesをより使いやすく、かつ移植性を保つために十分にcursesに近いインターフェースを提供することを目的としたcrateです。

Linuxではncurses-rs、Windowsではpdcurses-sysに依存しています。

| key | value |
| -- | -- |
| repository |[ihalila/pancurses](https://github.com/ihalila/pancurses) |
| Star | 204 |
| crates.io | [https://crates.io/crates/pancurses](https://crates.io/crates/pancurses) |
| Latest version | 0.16.1(Dec 26, 2018) |
| docs.rs | [pancurses - Rust](https://docs.rs/pancurses/0.16.1/pancurses/) |

```rust
use pancurses::*;

const MESSAGE: &str = "Merry Christmas !!";

fn main() {
    let window = initscr();
    start_color();
    use_default_colors();
    init_pair(1, COLOR_BLUE, -1);
    window.printw("Hello world !!");
    window.refresh();
    window.keypad(true);
    noecho();
    curs_set(0);

    loop {
        match window.getch() {
            Some(Input::Character('m')) => {
                let y = window.get_max_y() / 2;
                let x = window.get_max_x() / 2 - (MESSAGE.len() / 2) as i32;
                window.clear();
                window.color_set(1);
                window.mvaddstr(y, x, MESSAGE);
            }
            Some(Input::KeyDC) => break,
            _ => (),
        }
    }
    endwin();
}
```

initscrがwindow返して、その後はwindowのメソッドを呼ぶようになっており、生のncursesよりも使いやすく抽象化されていることがわかります。

<h2 id="rustbox">rustbox</h2>

| key | value |
| -- | -- |
| repository | [gchp/rustbox](https://github.com/gchp/rustbox) |
| Star | 391 |
| crates.io | [https://crates.io/crates/rustbox](https://crates.io/crates/rustbox) |
| Latest version | 0.11.0 Mar 31, 2018 |
| docs.rs | [rustbox - Rust](https://docs.rs/rustbox/0.11.0/rustbox/) |

Rustboxは[termobox](https://github.com/nsf/termbox)のRust実装です。READMEでは、現在はCライブラリのラッパーで将来的にRustのみの実装に置き換える計画だと書かれています。

しかし、2018年5月以降、新しいリリースはされていないようです。


```rust
use rustbox::*;

const MESSAGE: &str = "Merry Christmas !!";

fn main() {
    let rustbox = RustBox::init(Default::default()).unwrap();
    rustbox.clear();
    rustbox.print(0, 0, rustbox::RB_NORMAL, Color::White, Color::Default,  "Hello world !!");
    rustbox.present();

    loop {
        match rustbox.poll_event(false) {
            Ok(rustbox::Event::KeyEvent(key)) => {
                match key {
                    Key::Char('m') => {
                        let x = rustbox.width() / 2 - (MESSAGE.len() / 2);
                        let y = rustbox.height() / 2;
                        rustbox.clear();
                        rustbox.print(x, y, rustbox::RB_BOLD, Color::Blue, Color::Default, MESSAGE);
                        rustbox.present();
                    },
                    Key::Ctrl('c') => break,
                    _ => {},
                }
            },
            _ => {},
        }
    }
}
```

ncurses-rsやpancursesよりもシンプルで使い勝手がよいインターフェースとなっています。

<h2 id="crossterm">crossterm</h2>

crosstermはWindows, UNIX両方をサポートするクロスプラットフォームなターミナル操作ライブラリです。

READMEでは、1.0リリースの準備として最新バージョンでインターフェースを大きく変更していることが記載されており、この後のリリース0.14でも破壊的な変更が予定されているようです([0.13から0.14へのアップグレード](https://github.com/crossterm-rs/crossterm/wiki/Upgrade-from-0.13-to-0.14))

| key | value |
| -- | -- |
| repository | [crossterm-rs/crossterm](https://github.com/crossterm-rs/crossterm) |
| Star | 475 |
| crates.io | [https://crates.io/crates/crossterm](https://crates.io/crates/crossterm) |
| Latest version | 0.13.3(Nov 8, 2019) |
| docs.rs | [crossterm - Rust](https://docs.rs/crossterm/0.13.3/crossterm/) |

```rust
use crossterm::*;
use std::io::{stdout, Write};
use crossterm::screen::RawScreen;

const MESSAGE: &str = "Merry Christmas !!";

fn main() {
    let _screen = RawScreen::into_raw_mode().unwrap();
    let input = input::input();
    let mut sync_stdin = input.read_sync();

    execute!(
        stdout(),
        cursor::Hide,
        terminal::Clear(terminal::ClearType::All)
    ).unwrap();

    execute!(
        stdout(),
        style::SetForegroundColor(style::Color::White),
        cursor::MoveTo(0, 0),
        Output("Hello world !!"),
        style::ResetColor
    ).unwrap();

    let (width, height) = terminal::size().unwrap();
    let x = width / 2 - (MESSAGE.len() / 2) as u16;
    let y = height / 2;

    loop {
        let event = sync_stdin.next();
        match event {
            Some(input::InputEvent::Keyboard(k)) => {
                match k {
                    input::KeyEvent::Char('m') => {
                        let styled = style::style("Merry Christmas !!")
                            .with(style::Color::Blue)
                            .attribute(style::Attribute::Bold);
                        execute!(
                                stdout(),
                                terminal::Clear(terminal::ClearType::All),
                                cursor::MoveTo(x, y),
                                style::PrintStyledContent(styled)
                            ).unwrap();
                    },
                    input::KeyEvent::Ctrl('c') => break,
                    _ => {},
                }
            },
            _ => {},
        }
    }

    execute!(
        stdout(),
        cursor::Show
    ).unwrap();
}
```

ターミナル操作コマンドを並べて`execute!`で一度に実行するコマンドAPIが特徴的です。
ドキュメントにはコマンドAPIには以下のメリットがあると記載されています。

- よりよい性能
- フラッシュするタイミングを完全に制御可能
- ANSIエスケープコマンドが実行される場所を完全に制御可能
- より簡単で優れたAPI

また、上記サンプルコードでは`SyncReader`を使用していますが、非同期版の`AsyncReader`が用意されていることも特徴です。

<h2 id="termion">termion</h2>

termionはピュアRust, 他の低レベルハンドリング用のライブラリに依存しない、ターミナル操作crateです。

Rust製のUNIXライクなOSであるRedoxのプロジェクト配下でメンテされています。


| key | value |
| -- | -- |
| repository | [redox-os/termion](https://github.com/redox-os/termion) |
| Star | 1.1k |
| crates.io | [https://crates.io/crates/termion](https://crates.io/crates/termion) |
| Latest version | 1.5.4(Nov 30, 2019) |
| docs.rs | [termion - Rust](https://docs.rs/termion/1.5.4/termion/) |

```rust
use termion::*;
use std::io::{Write, stdout, stdin};
use termion::input::TermRead;
use termion::raw::IntoRawMode;

const MESSAGE: &str = "Merry Christmas !!";

fn main() {
    let stdin = stdin();
    let mut stdout = stdout().into_raw_mode().unwrap();
    write!(stdout, "{}{}", clear::All, cursor::Hide).unwrap();
    write!(stdout, "{}Hello world !!", cursor::Goto(1, 1)).unwrap();
    stdout.flush().unwrap();

    for c in stdin.keys() {
        match c {
            Ok(event::Key::Char('m')) => {
                if let Ok((width, height)) = terminal_size() {
                    let x = width / 2 - (MESSAGE.len() / 2) as u16;
                    let y = height / 2;
                    write!(stdout, "{}{}{}{}{}{}",
                           clear::All,
                           cursor::Goto(x, y),
                           color::Fg(color::Blue),
                           style::Bold,
                           MESSAGE,
                           style::Reset,
                    ).unwrap();
                    stdout.flush().unwrap();
                }
            },
            Ok(event::Key::Ctrl('c')) => break,
            _ => {},
        }
    }

    write!(stdout, "{}", termion::cursor::Show).unwrap();
}
```

crosstermのように複数のコマンドを一度に実行する形式ですが、標準出力に制御コードを書き込むというのがよりむき出しとなった見た目です。


<h2 id="cursive">cursive</h2>

今まで紹介したcrateが単純なターミナル操作に特化したcrateであったのに対して、ここから紹介するcursiveとtui-rsはよりリッチなTUIを実現するcrateです。

どちらもWidgetを組み合わせて複雑な画面のアプリケーションを作り込んでいくことができます。

cursiveとtui-rsのどちらを使えばいいかは以下のドキュメントがあります。

[Cursive vs tui‐rs · gyscos/cursive Wiki](https://github.com/gyscos/cursive/wiki/Cursive-vs-tui%E2%80%90rs)

cursiveはncurses-rs, pancurses, termion, crossterm, BearLibTerminal.rsからbackendを選択することができます。

| key | value |
| -- | -- |
| repository | [gyscos/cursive](https://github.com/gyscos/Cursive) |
| Star | 1.4k |
| crates.io | [https://crates.io/crates/cursive](https://crates.io/crates/cursive) |
| Latest version | 0.13.0 (Aug 17, 2019) |
| docs.rs | [cursive - Rust](https://docs.rs/cursive/0.13.0/cursive/) |

```rust
use cursive::*;

const MESSAGE: &str = "Merry Christmas !!";

enum State {
    HelloWorld,
    MerryChristmas,
}

struct StateContainer {
    state: State,
}

impl StateContainer {
    fn new() -> StateContainer{
        StateContainer { state: State::HelloWorld }
    }
}

fn main() {
    let mut siv = Cursive::default();
    let mut theme = theme::Theme::default();
    theme
        .palette
        .set_color("view", theme::Color::TerminalDefault);
    theme
        .palette
        .set_color("foreground", theme::Color::from_256colors(15));
    theme
        .palette
        .set_color("background", theme::Color::TerminalDefault);
    siv.set_theme(theme);

    let mut state = StateContainer::new();
    let mut canvas = views::Canvas::new(state);
   canvas.set_required_size(|_, constraint| {constraint});
    canvas.set_on_event(|state, event| {
        if event == event::Event::Char('m') {
            state.state = State::MerryChristmas;
        }
        event::EventResult::Ignored
    });
    canvas.set_draw(|state, printer| {
        match state.state {
            State::HelloWorld => {
                printer.print((0, 0), "Hello world !!");
            }
            State::MerryChristmas => {
                let x = printer.size.x / 2 - (MESSAGE.len() / 2);
                let y = printer.size.y / 2;
                let mut style = theme::Style::default();
                style.effects.insert(theme::Effect::Bold);
                style.color = Some(theme::ColorStyle::from(theme::Color::from_256colors(12)));
                printer.with_style(style, |p| {
                    p.print((x, y), MESSAGE);
                });
            }
        };
    });
    siv.add_fullscreen_layer(canvas);
    siv.run();
} 
```

組み込みのWidgetやサードパーティのWidgetで対応できない場合は、独自のWidgetを定義します。

上記サンプルコードでは、インラインで独自の挙動を設定できる組み込みWidgetのCanvasを使用しています。


<h2 id="tui-rs">tui-rs</h2>

tui-rsは少し前に話題になった[spotify-rs](https://github.com/Rigellute/spotify-tui)でも使用されているcrateです。

tui-rsはtermion, rustbox, crossterm, pancursesからbackendを選択することができます。

| key | value |
| -- | -- |
| repository | [fdehau/tui-rs](https://github.com/fdehau/tui-rs) |
| Star | 2.1k |
| crates.io | [https://crates.io/crates/tui](https://crates.io/crates/tui) |
| Latest version | 0.7.0 (Nov 29, 2019) |
| docs.rs | [tui 0.7.0 - Docs.rs](https://docs.rs/crate/tui/0.7.0) |


```rust
use std::io;
use termion;
use termion::input::TermRead;
use termion::raw::IntoRawMode;
use tui::widgets::Widget;
use tui::*;

const MESSAGE: &str = "Merry Christmas !!";

struct Label<'a> {
    x: u16,
    y: u16,
    text: &'a str,
    style: style::Style,
}

impl<'a> Default for Label<'a> {
    fn default() -> Label<'a> {
        Label {
            x: 0,
            y: 0,
            text: "",
            style: style::Style::default(),
        }
    }
}

impl<'a> Label<'a> {
    fn text(&mut self, text: &'a str) -> &mut Label<'a> {
        self.text = text;
        self
    }
    fn position(&mut self, x: u16, y: u16) -> &mut Label<'a> {
        self.x = x;
        self.y = y;
        self
    }
    fn style(&mut self, style: style::Style) -> &mut Label<'a> {
        self.style = style;
        self
    }
}

impl<'a> Widget for Label<'a> {
    fn draw(&mut self, area: layout::Rect, buf: &mut buffer::Buffer) {
        buf.set_string(
            area.left() + self.x,
            area.top() + self.y,
            self.text,
            self.style,
        );
    }
}

fn main() {
    let stdout = io::stdout().into_raw_mode().unwrap();
    let stdout = termion::screen::AlternateScreen::from(stdout);
    let backend = backend::TermionBackend::new(stdout);
    let mut terminal = Terminal::new(backend).unwrap();
    terminal.hide_cursor();
    terminal
        .draw(|mut f| {
            let size = f.size();
            Label::default().text("Hello World !!").render(&mut f, size);
        })
        .unwrap();

    let stdin = io::stdin();
    for c in stdin.keys() {
        match c {
            Ok(termion::event::Key::Char('m')) => {
                terminal.clear();
                terminal
                    .draw(|mut f| {
                        let size = f.size();
                        let x = size.width / 2 - (MESSAGE.len() / 2) as u16;
                        let y = size.height / 2;
                        let style = style::Style::default().fg(style::Color::Blue);
                        Label::default()
                            .text(MESSAGE)
                            .position(x, y)
                            .style(style)
                            .render(&mut f, size);
                    })
                    .unwrap();
            }
            Ok(termion::event::Key::Ctrl('c')) => break,
            _ => {}
        }
    }
}
```

tui-rsは入力はハンドルしないため、termionなどのbackendの仕組みをそのまま使用します。


<h2 id="conclusion">まとめ</h2>

長いものに巻かれろということでStar数の多いtermionで実装し直したところ、CPU使用率は8%まで下がりました！

