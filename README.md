version v.2.0β
# SCS (Sratch Cloud System)
これはscratch projectと外部での通信を可能にするためのサーバープログラムです。

# Setup
git cloneします。
```bash
git clone https://github.com/098orin/SCS.git
```

プロジェクトのルート下に`value.py`というファイルを作成します。
```py
username = "your_username"   # string
password = "your_password"   # string
path = "your_path" # string このrepositoryの絶対path
datadir = "data_directory_path" # string, "/SCS_data"の絶対パス
project_id = [your_project_ids]   # 数字で普通にプロジェクトidを書いてください。
project_client = [your_project_client]   # Scratchの場合は"sc", Turbowarpの場合は"tw"
project_privilege = [project_privileges]   # 信頼できるprojectは"high", 普通のは"low", 例外あり

password_project = project_id # 後述する手順に従う。project_idを数字で入力。
private_key = 0x`your_Curve448_private_key`  # 後述する手順に従う。`python password_manager.py gen` で生成。秘密鍵をここに書く。
public_key = 0x`your_Curve448_public_key` # 後述する手順に従う。
```
`project_なんたら`はそれぞれのリストの内容の順番を合わせてください。

最初に`setup.py`を動かす必要があった気がしないでもないです。もし動かなかったらこれを実行してみてください。

# Run
実行にはpython3.8以上が必要です。それ以外は必要ありません。管理者権限があるとなお良いです。
一応すべてのOSで動くように作っていますが、動作確認はWindowsとLinuxのみです。

Windows, macOS, Linux
```bash
cd SCS
python _server.py
```

できれば
```bash
cd SCS
sudo python _server.py
```
のほうが好ましいです。権限Ｅｒｒｏｒで動かないかもしれません。もし動かなかったら教えてください。

# Scratch
Scarcth側のprojectのdocumentは
https://ja.scratch-wiki.info/wiki/%E5%88%A9%E7%94%A8%E8%80%85:Mario-098/ScratchCloudSystem
を参照してください。
なお、パスワードを使用した通信暗号化機能を使用したい場合は、project_privilegesを"password"に設定したprojectが必要です。"url(未定)"をremixしてください。

## password登録
1. 秘密鍵と公開鍵を生成します。
```bash
python password_manager.py gen
```
2. `value.py`で変数`private_key`を宣言。生成した秘密鍵を入力する。なお、`0x`を先頭につけて16進数として定義する。
3. `value.py`で変数`public_key`を宣言。生成した秘密鍵を入力する。なお、`0x`を先頭につけて16進数として定義する。
4. https://scratch.mit.edu/projects/-未定- をremixして、変数：Public_key に生成した公開鍵を入力して共有。
5. `value.py`で変数`password_project`を宣言。remixしてできたプロジェクトのidを入力する。

# 今後の更新予定（TODO）
* 通信暗号化（password）