# Runpodを使う。
2026-11-17
Runpodとは、GPUを貸してくれるところです。CPUではなく、GPUを借りることができます。
時間いくらで料金が発生します。

ローカルでモデルを動かしたいけど、GPUがない人が使います。
ここでは、VSCODEから、使用するまでをざっと流します。
~~(ざっと、流して書けるようになるまでに、1カ月位はかかってますが。)~~

実行するモデルは、qwen2.5-coder:14b です。
~~使用するGPUは、RTX3090(24GB VRAM) なので、モデルはこれくらいかなと。~~
使用するGPUは、RTX A6000(48GB VRAM)を使います。VRAMは、48GBですが、「RTX 4090(24GB VRAM)」よりも安いので。

## GPUを選んで起動まで。
2026.11では、「Community Cloud」の選択がない。
~~「Community Cloud」を選択します。（安く済ませるので）~~

GPUは、RTX A6000(48GB VRAM)を選択する。
~~「NVIDIA previous generation」の「RTX 3090」を選択します。（お手頃なので）~~

Container diskの容量は、デフォルトで50GBなので、増やす必要はない。
~~Pod template：「Runpod Pytorch 2.4.0」を選択、「Edit」で、Container disk: 40GB。Volume disk: 40GBに増やす。~~

「PyTorch - 2.13.0」の右側にある、「Set overrides」をクリックする。（「Exporse TCP ports」がこっちに移った）
~~Expose TCP ports:「22, 11434」（11434を追加する。）~~
「Edit template overrides」で下記を設定
「Start jupyter notebook」をOFFする。（使わないので）
「Expose TCP ports:「11434」（22の下の行に、11434を追加する。「22」と「11434」の2行にする）
「Set ovverides」をクリックする(ダイアログを閉じる)。
~~「Deploy On-Demand」をクリックする。~~
（Podが作成されるまで待ちます。）

作成が完了したら、「Connect」のタブの中の「Direct TCP ports」を確認します。２行表示されるはず。
SSH → xxxxxxx → :22 （1行目）
XXXXX → :11434 （2行目：追加した、11434があることを確認する。時々、出てこない時があるので）

## Ollamaのインストールから起動
さきほどの「Connect」タブの、「SSH」（No support for SCP & SFTP)の部分「コピー」を押します(Copied!がでればOK)。
Windowsで、コマンドプロンプトを表示して、右クリックします。
sshのコマンドがペーストされればOK.Enterを押します。

--RUNPOD.IO--
Enjoy your Pod 

OLLAMAのインストールから起動を行います。
（AIが教えてくれます。2026.11.17現在）

```
# 必要なパッケージの更新とインストール
apt update && apt install -y curl lshw
# Ollamaのインストール
curl -fsSL https://ollama.com/install.sh | sh
# Ollamaサーバーの起動(バックグラウンドでOllamaのサーバープロセスを立ち上げます。)
OLLAMA_HOST=0.0.0.0 ollama serve &
```


確認は、SSHで下記で確認する。

 curl http://127.0.0.1:11434/api/tags
~~[GIN] 2026/06/08 - 23:59:38 | 200 |     271.684µs |       127.0.0.1 | GET      "/api/tags" ~~
[GIN] 2026/11/17 - 01:51:40 | 200 | 670.285µs |       127.0.0.1 | GET      "/api/tags"
{"models":[]} 

"models":[]、空になっていますが、まだ動かしていないのでOKです。
既にモデルまで実行しているときは、ここにモデル名が表示されます。

## モデル pull/run

ollama pull qwen2.5-coder:14b
（2026.07は、ollama pull qwen3-coder:30b-a3b-q4_K_M みたいだけど、このGPUでは重いので）

ollama run qwen2.5-coder:14b 
（下記のように">>>"のプロンプトがでるので、こんにちは。と入力して、Enterを押します。）
>>> こんにちは。
（10秒から20秒位）こんにちは！お元気ですか？何かお手伝いできることがありますか？
（のような、レスポンスが返ってくればOK）
>>> /bye 
（/bye で終了する。サーバー側はこれで確認OK）
exitで、runpodとの接続も切断する。（runpod側は、実行したままになる。）

Windowsからの確認  
コマンドプロンプトから、  
 curl http://127.0.0.1:11434/api/tags  
さっきの、Runpodの画面の「→:11434」の左側の部分をhttp://の後ろに入れます。  
curl http://38.147.83.14:35066/api/tags
レスポンスが返ってくればOK。レスポンスは、下記のようなものです。
（動かしたモデルの名前、2027.11の例では"qwen2.5-coder:14b"が返ってくればOK。）
{"models":{"name":"qwen2.5-coder:14b", ...}  
これで、Windowsからも接続できることが確認できました。
あとは、VSCodeの設定。

