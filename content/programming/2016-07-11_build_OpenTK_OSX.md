Title: OSXでOpenTKをビルドする
Tags: FSharp, OpenTK, OpenGL
Summary: OpenTKのNugetパッケージはソース不明

F#でProcessingのように簡単なAPIでビュジュアライゼーションできるツールを探していたけど良さそうなものがなかったので作ってみることにした。

Processingのソースが参考にできるので描画にはProcessingでも使われているOpenGLを使うことにした。
OpenGLのラッパーを書くのもだるいので、既存の.NET Framework用のラッパーであるOpenTKを使うことにした。

OpenTKはNuGet公式ソースでパッケージが配布され、6月に更新版がリリースされいるのだが、手元のMacBook Airで動かないし、公式サイトのリファレンスと名前空間やenum名などが変わっている。

どうやら公式のソースからビルドしたものではないらしい。
（[Mono/OpenTK](https://github.com/mono/opentk)が同じようにOpenTK.Graphics.OpenGK4名前空間がなくなったりしているので、これがソースかもしれないが不明）

公式サイトのリリースも2014年で止まっているが、githubでの更新は続いているので、ソースからビルドすることにした。

以下、ソースからのビルドのメモ。
(環境はMacBook Air Mid-2012, El Capitan)

MonoとNuGetがインストールされていない場合は、インストールしておく。

```
$ wget https://github.com/opentk/opentk/archive/develop.zip
$ unzip develop.zip
$ cd opentk-develop
$ mono nuget restore OpenTK.sln
$ xbuild OpenTK.sln

```

GLWidgetはビルドエラーになるけどOpenTK.dllはビルドできているので問題ない。
OpenTK.dllをコピーしてプロジェクトに参照追加する。

以下はOpenGLの[opengl-tutorialの2](http://www.opengl-tutorial.org/jp/beginners-tutorials/tutorial-2-the-first-triangle/)をOpenTKで実装した例。

```fsharp
open System
open System.IO
open OpenTK
open OpenTK.Graphics
open OpenTK.Graphics.OpenGL4

[<AutoOpen>]
module Shaders =
    let loadShaders(vFile: string, fFile: string) =
        let programId = GL.CreateProgram()

        let vertexShaderId = GL.CreateShader(ShaderType.VertexShader)
        GL.ShaderSource(vertexShaderId, File.ReadAllText(vFile))
        GL.CompileShader(vertexShaderId)
        GL.AttachShader(programId, vertexShaderId)

        let fragmentShaderId = GL.CreateShader(ShaderType.FragmentShader) 
        GL.ShaderSource(fragmentShaderId, File.ReadAllText(fFile))
        GL.CompileShader(fragmentShaderId)
        GL.AttachShader(programId, fragmentShaderId)

        GL.LinkProgram(programId)
        let attributeCount = GL.GetProgram(programId, GetProgramParameterName.ActiveAttributes)
        let uniformCount = GL.GetProgram(programId, GetProgramParameterName.ActiveUniforms)
        GL.DeleteShader(vertexShaderId)
        GL.DeleteShader(fragmentShaderId)
        programId


type MyWindow() = 
    inherit GameWindow(800, 600, GraphicsMode.Default, "opengl-tutorial02", GameWindowFlags.Default, DisplayDevice.Default, 4, 1, GraphicsContextFlags.Default)
    let initEvent = new Event<EventArgs>()

    member gl.OnInit = initEvent.Publish

    override gl.OnLoad(e: EventArgs) =
        base.OnLoad(e)
        initEvent.Trigger(e)
        gl.SwapBuffers()
        
module Main =
    [<EntryPoint>]
    let main _ = 
        use window = new MyWindow()
        window.OnInit
        |> Observable.subscribe(fun _ ->
            let programId = loadShaders( "SimpleVertexShader.vertexshader", "SimpleFragmentShader.fragmentshader" )
            GL.ClearColor(0.f, 0.f, 0.4f, 0.f)
            GL.UseProgram(programId)
            let arr: uint32 = GL.GenVertexArrays(1)
            GL.BindVertexArray(arr) 

            let mutable data = [| -1.f; -1.f; 0.f; 
                                   1.f; -1.f; 0.f; 
                                   0.f;  1.f; 0.f |] 
            let buffer: uint32 = GL.GenBuffers(1)
            GL.BindBuffer(BufferTarget.ArrayBuffer, buffer)
            let size = data.Length * sizeof<float32>
            GL.BufferData<float32>(BufferTarget.ArrayBuffer, IntPtr(size), data, BufferUsageHint.StaticDraw)

            GL.Clear(ClearBufferMask.ColorBufferBit ||| ClearBufferMask.DepthBufferBit)
            GL.EnableVertexAttribArray(0)
            GL.BindBuffer(BufferTarget.ArrayBuffer, buffer)
            GL.VertexAttribPointer(0, 3, VertexAttribPointerType.Float, false, 0, 0)
            GL.DrawArrays(PrimitiveType.Triangles, 0, 3)
            GL.DisableVertexAttribArray(0)
        )
            
        window.Run(30.0)
        0
```

